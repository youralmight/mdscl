# DSCI 523 Quiz 2：R 整洁控制流、函数与测试复习

## 1. 范围证据与材料边界

- 当前学年课程 README 只明确列出 Quiz 2 占课程总评 **30%**，window 为 **2026-09-29–10-02**；没有给出 Quiz 2 的 lecture 范围、题型、practice quiz 或专门 scope sheet。
- 当前 `official/current/` 没有 Quiz 2 公告。当前已发布、且紧接 Quiz 1 之后的材料包括 Lecture 5–6 讲义、Lecture 5 课前 skeleton、Worksheet 5–6、Lab 3 和 section-002 的 Lecture 5–6 example problems。因此本复习稿以 **Lecture 5–6 及这些已发布练习中的非 optional 内容**为已发布复习边界。
- **[未确认]** Lecture 7–8 是否属于 Quiz 2。虽然 current tree 里已有 `07-mapping-and-nested-data-frames.ipynb` 与 `08-lecture-tidy-evaluation.ipynb`，但本地没有把它们列为 Quiz 2 范围的说明，也没有对应已发布的 Worksheet 7–8 / Lab 4 练习作为边界证据；本稿不把 Lecture 7–8 当作已确认范围。若教师之后明确公布范围，应按公告补充。
- Lecture 6 把 `...` 标作 **Optional – Advanced**；Worksheet 5 的练习 5–6、Worksheet 6 的练习 2/4/5、Lab 3 的练习 5–6 也标成 optional、challenging 或未计分。本文会标明状态，不把这些内容伪装成已确认核心范围；但其中反复出现的基础概念仍作为理解材料保留。
- 只使用 `official/current/` 的当前学年材料；没有用 `official/public/` 历史材料填补范围空白。

---

## 2. Tidy control flow：先处理值，再按组计算

### 2.1 `group_by()`、`summarise()`、`mutate()` 的形状

`group_by(data, key1, key2)` 给数据加上分组标记；它本身通常不减少行数。多个 key 的组合各自成为一个组。

```r
gapminder |>
  group_by(continent, year) |>
  summarise(mean_life_exp = mean(lifeExp))
```

- `summarise()` 对每个组计算摘要，通常输出**每组一行**；分组 key 会留在结果中。
- `n()` 在当前组中计数，不需要列名。
- `group_by()` + `mutate()` 在每组内计算，但通常保留原来的每一行。例如每个国家相对该国第一条记录：

```r
gapminder |>
  group_by(country) |>
  mutate(life_exp_gain = lifeExp - first(lifeExp)) |>
  ungroup()
```

- 需要普通的全表操作时显式 `ungroup()`，避免后续步骤继续按组运行。
- 做题前先说清楚“最终一行代表什么”：每个 engine、每个 continent-year，还是原始的一条 observation。

典型汇总：

```r
planes |>
  group_by(engine) |>
  summarise(
    avg_seats = mean(seats, na.rm = TRUE),
    planes = n()
  )
```

### 2.2 缺失值：删除、替换，还是在计算时忽略

R 的许多统计函数遇到任意 `NA` 就返回 `NA`。缺失值的处理必须由问题决定：

```r
penguins |> drop_na(body_mass_g)  # 只删除 body_mass_g 缺失的行
penguins |> drop_na()             # 任一列缺失就删除整行

penguins |>
  group_by(species) |>
  summarise(max_bill = max(bill_length_mm, na.rm = TRUE))
```

- `drop_na(x:y)` 只根据列 `x` 到 `y` 判断；不要误用没有参数的 `drop_na()`。
- `na.rm = TRUE` 属于真正执行统计的函数，如 `mean()`、`max()`、`median()`；不是写给 `summarise()` 的全局参数。
- 先确认“缺失是否应删除”。盲目 `na.rm = TRUE` 会改变样本含义。
- 检查缺失应使用 `is.na(x)` 或 `!is.na(x)`，不要写 `x == NA`；与 `NA` 比较的结果仍是 `NA`，不是 `TRUE`/`FALSE`。

### 2.3 `case_when()`：有选择地替换值

`case_when()` 适合在 `mutate()` 中按行选择新值。每个分支形如 `条件 ~ 结果`：

```r
fixed <- fix_me |>
  mutate(
    province = case_when(
      province == "Alberta" ~ "AB",
      province == "British Columbia" ~ "BC",
      TRUE ~ province
    )
  )
```

- `TRUE ~ 原列` 是默认分支，保留未匹配值；没有默认分支时，未匹配值会变成 `NA`。
- 所有结果必须是兼容类型。
- Lecture 5 中 `gapminder$country` 和 `continent` 是 factor；若要用字符值替换，先用 `as.character()`，再用 `case_when()`。
- 只改变目标列；做完检查唯一值、行数和其他列是否不变。

### 2.4 分组题的固定思路

1. 确定最终 observation 与输出行数。
2. 用 `group_by()` 指定一组或多组 key。
3. 要每组一行，用 `summarise()`；要保留原行，用分组 `mutate()`。
4. 决定 `drop_na()`、`na.rm = TRUE` 或 `case_when()` 的缺失规则。
5. 最后 `select()`、`arrange()`，并检查列名、类型、行数和是否仍处于 grouped 状态。

---

## 3. `purrr::map*`：对每个元素应用同一个函数

### 3.1 functional 与基本形状

functional 接受函数作为输入，对一组元素重复应用它。`purrr::map(.x, .f, ...)` 读作“对 `.x` 的每个元素应用 `.f`”。

```r
library(purrr)

map(mtcars, median)                         # list
map_dbl(mtcars, median, na.rm = TRUE)       # double vector
map_lgl(mixed_bag, is.numeric)              # logical vector
map_chr(x, function(item) paste0("id-", item))
map_df(mtcars, median)                      # tibble；课堂使用的名称
```

| 目标输出 | 函数 | 必须满足 |
|---|---|---|
| 任意形状 | `map()` | 结果保留为 list |
| 一个 double | `map_dbl()` | 每次结果是长度 1 的数值 |
| 一个 integer | `map_int()` | 每次结果是长度 1 的整数 |
| 一个逻辑值 | `map_lgl()` | 每次结果是长度 1 的 `TRUE`/`FALSE` |
| 一个字符串 | `map_chr()` | 每次结果是长度 1 的 character |
| 合并为 tibble | `map_df()` | 每次结果能合并成行/列 |

- `.f` 可以是已有函数（如 `median`、`is.numeric`），也可以是匿名函数。
- `...` 把额外参数传给每次 `.f` 调用，例如 `map_dbl(x, median, na.rm = TRUE)`。
- `map()` 的输出即使每一项看起来是数字，也仍是 list；需要向量时选择正确的类型后缀。
- 若题目指定 `map*`，不要用 `across()` 替代；`across()` 是另一个抽象。

### 3.2 `for` 与 `map*` 的对应关系

`for` 循环当然可以迭代，但通常需要手动：

1. 预分配输出空间；
2. 决定正确的迭代次数；
3. 维护索引并把结果放到正确位置。

`map*` 把迭代和输出类型写进接口。改写前先确定：遍历的是向量、list 还是 data frame 的列；每次函数应返回什么类型和长度；缺失值参数是否要通过 `...` 传递。

Lab 3 的 `mixed_bag` 题：先用 `map_lgl(mixed_bag, is.numeric)` 得到顶层元素的逻辑向量，再用 `sum(result) == length(mixed_bag)` 判断是否全部满足。题目明确不要求检查第五个嵌套 list 内部。

---

## 4. 在 R 中定义函数：参数、返回值和作用域

### 4.1 函数基本结构

```r
add <- function(x, y) {
  x + y
}

add(5, 10)
```

- 形式是 `name <- function(parameters) { body }`。
- 函数是 R 中的一等对象：可以绑定到名字、传给 `map`，也可以从脚本或 package 导入。
- 默认情况下，函数最后一个表达式就是返回值；`return(value)` 可以提前结束。
- 默认参数只有在调用者省略该参数时才使用。

```r
repeat_string <- function(x, n = 2) {
  out <- ""
  for (i in seq_len(n)) out <- paste0(out, x)
  out
}

mpg_to_kml <- function(mpg) {
  if (!is.numeric(mpg)) stop("mpg must be numeric")
  mpg * 0.425144
}
```

先写 specification：参数类型、允许长度、返回类型、错误条件和边界行为；再写最小实现。

### 4.2 惰性求值与 `...`

R 的函数参数是惰性求值：只有函数体实际访问某个参数时才会对它求值。因此，函数体完全不用到的参数，即使调用时没有可计算的值，也可能不报错；这和 Python 先求值所有实参不同。

`...` 表示可变数量的额外参数。Lecture 6 将手动读取 `...` 标为 **Optional – Advanced**，示例用 `list(...)` 把它们取出来。`purrr::map*` 中则经常用 `...` 把 `na.rm = TRUE` 等参数传给 `.f`。没有明确需求时不要给函数加含义模糊的 `...` 接口。

### 4.3 词法作用域与 environments

Lecture 6 重点示范：

1. **Name masking：**函数内部定义的名字遮蔽外部同名对象；函数内没有该名字时，R 沿 enclosing environments 向上查找。
2. **Dynamic lookup：**外部名字在函数运行时查找，而不是在函数创建时冻结；运行前改变全局对象可能改变函数结果。
3. **A fresh start：**每次调用创建新的执行环境；上次调用的局部变量不会自动保留下来。

```r
x <- 15
g <- function() x + 1
g()       # 16
x <- 20
g()       # 21：运行时查找 x
```

因此，函数最好把依赖作为显式参数传入，避免依赖会被外部改写的全局对象。`pkg::fun()` 调用单个 package 函数而不 attach 整个 package；`library(pkg)` 会把 package 接到 search path 上。

---

## 5. 测试、TDD、异常与代码组织

### 5.1 `testthat` expectations

```r
library(testthat)

test_that("conversion works", {
  expect_equal(mpg_to_kml(1), 0.425144)
  expect_equal(mpg_to_kml(2), 0.850288)
})

test_that("invalid input errors", {
  expect_error(mpg_to_kml("A"))
  expect_error(mpg_to_kml(list(1, 2)))
  expect_error(mpg_to_kml(data.frame(x = 1)))
})
```

| 要断言的行为 | expectation |
|---|---|
| 值、类型、属性都完全相同 | `expect_identical(x, y)` |
| 数值或对象近似相等 | `expect_equal(x, y, tolerance = ...)` |
| 近似相等但不强调属性 | `expect_equivalent(x, y)` |
| 结果为真/假 | `expect_true(x)` / `expect_false(x)` |
| 应报错 | `expect_error(expr)` |
| 应产生 warning | `expect_warning(expr)` |
| 应打印指定输出 | `expect_output(expr, ...)` |

浮点结果有合理的舍入误差时才设置有意义的 `tolerance`；不要为了让测试通过而无限放宽容差。

### 5.2 Test-driven development

TDD 的最小循环：

1. 先按正常用例、边界和错误输入写可执行的 specification；
2. 写最小函数使测试通过；
3. 增加新发现的边界测试并重跑，确保修改没有破坏旧行为。

失败测试是关于实现或 specification 的证据，不是应该盲目删掉的障碍。Lab 3 的 `cat_char()` 示例先写正常拼接、空向量、长度不同、相同向量、错误类型和缺少参数的测试，再实现函数。

### 5.3 Defensive programming 与 exception handling

函数入口应尽早检查输入，并用可定位的信息失败：

```r
fahr_to_celsius <- function(temp) {
  if (!is.numeric(temp)) {
    stop("temp must be numeric")
  }
  (temp - 32) * 5 / 9
}
```

- `stop()` 抛出 error，适合违反函数 contract 的输入；用 `expect_error()` 测试。
- `warning()` 报告可继续运行但值得注意的情况；用 `expect_warning()` 测试。
- `try({ ... })` 让当前错误后继续执行后续代码；它不是把错误输入变成有效输入的替代方案。
- 不要把错误输入悄悄转成 `NA`，除非 specification 明确要求。

### 5.4 roxygen2、`source()` 与 package

函数定义前可以写 roxygen2 风格的 contract：

```r
#' Convert miles per gallon to kilometres per litre.
#'
#' @param mpg numeric vector in miles per gallon
#' @return numeric vector in kilometres per litre
#' @examples
#' mpg_to_kml(1)
mpg_to_kml <- function(mpg) mpg * 0.425144
```

至少写清 description、每个 `@param`、`@return` 和 `@examples`；注释描述 contract，不逐行复述代码。Worksheet 6 还示范了 `@export`。

- `source("src/kelvin_to_celsius.R")` 把另一个 R script 中定义的函数载入当前分析。
- package 把可复用代码、文档和测试组织成可安装的接口；安装后可以 `library(package)` 或 `package::function()`。
- package 的价值包括跨项目复用、稳定接口和文档化，不是隐藏代码。
- 代码质量检查：名称、缩进和 pipe 是否表达意图；函数是否只做一个清楚的任务；是否重复计算或无必要嵌套；输入、输出、错误行为能否独立测试。

### 5.5 Lab 3 的样本方差题（非 optional）

Lab 3 要求从头实现样本方差，不调用 `var()`。对数值向量 `x`，先求 `mean(x)`，再计算：

`sum((x - mean(x))^2) / (length(x) - 1)`

函数应返回长度为 1 的数值，并用 defensive programming 拒绝 list、data frame 等错误输入；用 `testthat` 覆盖可手算的正常值、边界和错误输入。Lab 3 另有 standard error 的 challenging 练习，公式为 `sd / sqrt(n)`，不作为已确认核心范围。

---

## 6. 常见题面与易错对照

| 题目线索 | 优先想到 | 常见错误 |
|---|---|---|
| “每个 engine/continent 分别……” | `group_by()` + `summarise()` | 忘记分组，整张表只得到一个数字 |
| “保留每一行，同时加入组内值” | grouped `mutate()` | 用 `summarise()`，行数塌缩 |
| 汇总列有 `NA` | 先决定 `drop_na()` 或在统计函数内 `na.rm = TRUE` | 以为 `summarise()` 自动忽略缺失 |
| 检查缺失 | `is.na(x)` | 写 `x == NA` |
| 只改少数类别 | `mutate()` + `case_when()` + `TRUE ~ old_col` | 未匹配值变 `NA`；factor 直接替换字符失败 |
| 删除指定列的缺失 | `drop_na(target)` | 错用 `drop_na()`，删掉更多行 |
| 对 list 或 data frame 每项应用函数 | `map*`，按输出类型选后缀 | 把 `map()` 的 list 误当 numeric vector |
| 函数要拒绝字符/list/data frame | `is.numeric()` + `stop()` + `expect_error()` | 返回 `NA`，掩盖错误 |
| 浮点结果几乎相等 | `expect_equal(..., tolerance = ...)` | 用 `expect_identical()` 造成无意义失败 |
| 需要额外参数 | `...`；在 map 中传 `na.rm` | 没确认 contract 就造模糊接口 |
| 需要从另一个 R 文件取得函数 | `source(path)` | 依赖 console 中残留的隐藏对象 |

---

## 7. 考前作答检查

1. 先写清最终形状：每组一行、原行数保留、list、typed vector、tibble，还是单个值。
2. 分组题确认 group keys、`summarise()`/`mutate()`、`n()`、`first()` 与 `na.rm`。
3. 清理题确认 factor/character 类型、`case_when()` 默认分支、`is.na()` 和 `drop_na()` 的列范围。
4. map 题确认 `.x`、`.f`、输出后缀及 `...` 传参；不要把 list 当向量。
5. 函数题确认参数/defaults、最后表达式返回值、输入检查、错误行为和边界测试。
6. 测试题确认 expectation 与 specification 匹配；数值容差要有理由。
7. 代码题最后检查括号、逗号、列名、对象名、参数和返回类型；不要依赖上一次运行残留的全局变量。

## 主要来源（均为当前学年本地材料）

- `official/current/DSCI_523_r-prog_students/README.md`：Lecture 主题、Quiz 2 日期/权重与课程政策。
- `official/current/DSCI_523_r-prog_students/lec_learning_objectives.md`：Lecture 5–6 learning objectives；Lecture 7–8 仅作为未确认边界证据。
- `official/current/DSCI_523_r-prog_students/jupyter-book/lecture-notes/05-tidy-control-flow.ipynb`：`case_when()`、`drop_na()`、分组汇总、分组 `mutate()` 与 `purrr::map*`。
- `official/current/DSCI_523_r-prog_students/jupyter-book/lecture-notes/06-lecture-functions-and-testing.ipynb`：函数、默认参数、惰性求值、作用域、`testthat`、TDD、异常、roxygen2、`source()` 与 package。
- `official/current/DSCI_523_r-prog_students/section-001/lecture-5-skeleton-pre.ipynb`：`is.na()`、`group_by()`/`summarise()` 的形状与分组顺序提醒。
- `official/current/DSCI_523_r-prog_students/section-002/lecture5-example-problems.md` 与 `lecture6-example-problems.Rmd`：按组汇总与从 specification 到测试再到函数实现的示例。
- `official/current/DSCI_523_r-prog_students/release/worksheet5/worksheet5.Rmd`：`case_when()`、按列/全表 `drop_na()`、分组汇总与 map 练习。
- `official/current/DSCI_523_r-prog_students/release/worksheet6/worksheet6.Rmd`：函数、数值/错误测试、roxygen2 与 package scavenger hunt。
- `official/current/DSCI_523_r-prog_students/release/lab3/lab3.Rmd`：tidy control flow、`map*`、函数抽象、TDD、异常与样本方差题。
- `DSCI_523/notes/resources.md`、`DSCI_523/notes/messages.md`：本地资源索引与课程公告索引；没有额外 Quiz 2 scope 公告。
