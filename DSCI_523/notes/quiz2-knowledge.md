# DSCI 523 Quiz 2：R 整洁控制流、函数与测试复习

## 1. 范围证据与材料边界

- 当前学年课程 README 列出 Quiz 2 占课程总评 **30%**，window 为 **2026-09-29–10-02**。本复习稿按当前已发布的 **Lecture 5–8** 及对应练习整理；Lecture 7–8 不再是未确认范围。
- 当前最终材料的主题依次为：Lecture 5 tidy control flow，Lecture 6 functions and testing，Lecture 7 mapping and nested data frames，Lecture 8 tidy evaluation。下文保留 Lecture 5–6 的详细内容，并补足 Lecture 7–8 的核心概念、代码形状与易错点。
- Lecture 6 与 Lecture 7/8 中标出的 **Optional / Optional–Advanced** 内容会明确标注；标为 optional 不等于核心要求，但需要能识别其用途和基本形状。对应 Worksheet 7–8 的练习用于核对最终材料边界。
- 只使用当前学年发布的 `official/current/` 材料；不以历史 `official/public/` 材料填补范围，也不把 optional 内容写成必考核心。

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

## 6. Lecture 7：anonymous functions、mapping 与 nested data frames

### 6.1 匿名函数与 `map()`

匿名函数没有绑定到名字，直接作为 `.f` 传给 `map()`。完整写法是
`function(x) expression`；短写法用 purrr 的公式 lambda：`~ expression`，其中
`.x` 表示当前元素，`.y` 表示第二个输入的当前元素。

```r
map_dbl(mtcars, function(column) mean(column, na.rm = TRUE))
map_dbl(mtcars, ~ mean(.x, na.rm = TRUE))
```

两种写法都要先确认 `.x` 的每个元素和结果的类型/长度。`~ .x + 1` 不是把整个
data frame 加 1，而是对 map 正在遍历的每个元素操作。需要使用多个表达式或清楚的
参数名时，优先用 `function(item) { ... }`，不要为了短而隐藏逻辑。

### 6.2 `map2()`、`pmap()` 与输出形状

`map2(.x, .y, .f)` 同时遍历两个等长输入，把每一对元素传给 `.f`；`pmap(.l, .f)`
遍历一个 list of inputs，每次把同一位置的多个元素传给函数。两者都保留
`map()` 的输出后缀规则：

```r
map2_dbl(x, y, ~ .x * .y)
pmap_dbl(list(x, y, z), function(a, b, c) a + b + c)
```

使用 `map2_dbl()`/`pmap_dbl()` 时，每次调用必须返回长度为 1 的 double；若结果
是任意形状则用 `map2()`/`pmap()`。输入长度、每个位置的对应关系，以及缺失值规则
都应先写清楚。`map2()`/`pmap()` 在 Worksheet 或讲义中标为 **Optional** 时，
知道它们分别对应“两路”和“多路”同步 mapping 即可，不要把 optional API 当作
替代所有基础 `map*` 题的理由。

### 6.3 nested data frame、list-column、`nest()`、`unnest()`

一个 tibble 的列可以是 list-column：该列每一行保存一个向量、模型或 tibble，
所以不同 row 的元素可以有不同长度。`nest()` 把同一组的多行收进一个 list-column，
外层表保留分组 key；`unnest()` 把 list-column 中的内容展开回多行/多列。

```r
nested <- gapminder |>
  group_by(continent) |>
  nest()

results <- nested |>
  mutate(
    avg_life_exp = map_dbl(data, ~ mean(.x$lifeExp, na.rm = TRUE))
  )

long_again <- nested |> unnest(data)
```

典型流程是 `group_by(key) |> nest()` → 对 `data` list-column 使用
`mutate()` + `map()`/`map_dbl()` → 保留 key 和结果，必要时 `unnest()`。不要把
list-column 误当成普通 atomic vector；先检查 `names()`, `map()` 后每项的 class/shape，
再决定用 `map_*`、`unnest()` 或 `unnest_wider()`。若函数每次返回 tibble，常用
`map()` 保留嵌套结果，确认结构后才展开；展开可能增加行数，必须复核 key 是否重复。

---

## 7. Lecture 8：tidy evaluation、data masking 与可复用函数

### 7.1 data masking 与 tidy evaluation

在 `dplyr` 的 data-masking 语境中，`mutate()`, `filter()`, `summarise()` 等表达式
可以直接写列名，例如 `filter(df, mass > 10)`；列名优先于函数外层环境中的同名对象。
这让交互式代码简洁，但在写“把列作为参数”的函数时，必须区分：

1. **data-masked expression**：调用者写 `my_summary(df, mass)`，参数不是普通
   字符串，而是要在数据上下文中捕获和重新注入的表达式；
2. **字符串列名**：调用者传 `"mass"`，可以用 `.data[[col]]` 明确取列；
3. **环境变量**：用 `.env$threshold` 明确表示来自函数环境的值，避免和列名混淆。

```r
summarise_mean <- function(data, col) {
  col <- enquo(col)
  data |> summarise(value = mean(!!col, na.rm = TRUE))
}

summarise_mean_chr <- function(data, col) {
  stopifnot(is.character(col), length(col) == 1, col %in% names(data))
  data |> summarise(value = mean(.data[[col]], na.rm = TRUE))
}
```

`enquo(col)` 把调用者传来的 data-masked 表达式捕获成 quosure；`!!col`（bang-bang）
在构造的新 tidy expression 中把它 unquote/evaluate。它们成对出现：先 capture，
再 inject。若函数参数只需要一个普通字符串，直接使用 `.data[[col]]`，不要无故
混用 quosure。

### 7.2 `{{ }}`、动态名字 `:=` 与 `...`

`{{ col }}` 是函数中常用的 embrace 简写：在接收列表达式的参数时，它等价于
capture + injection 的常见组合，适合直接转交给 dplyr：

```r
mean_by <- function(data, group, value) {
  data |>
    group_by({{ group }}) |>
    summarise(mean_value = mean({{ value }}, na.rm = TRUE), .groups = "drop")
}
```

当新列名来自参数或表达式时，在 `mutate()`/`summarise()` 中用 `:=` 而不是普通
`=`，例如 `summarise("{name}_mean" := mean({{ value }}, na.rm = TRUE))`。名字
插值和列表达式是两个问题：`{{ value }}` 注入要计算的列，`"{name}_mean" :=`
计算要创建的名字。

函数中的 `...` 可以把多个列表达式或额外参数向下传给 tidyverse 函数；例如
`summarise(.data, ..., .groups = "drop")` 允许调用者提供多个摘要。设计这种接口
时要说明 `...` 的含义，避免把不支持的参数静默吞掉。Lecture 8 中标作 **Optional**
的更复杂 tidy-eval/可变参数变体，先掌握 `{{ }}`、`.data[[ ]]`、`.env` 和
`:=` 的基本读法，再按题目要求使用。

### 7.3 defensive validation：让 tidy-eval 函数失败得清楚

可复用函数在进入 tidyverse 动词前应检查 contract：输入是否为 data frame/tibble，
字符串列名是否长度 1 且存在，数值参数是否为合法长度/范围，所选列是否为适合
统计的类型。违反 contract 用 `stop()`（或明确的 `cli` error），不要让深层
`dplyr` 错误或静默 `NA` 代替检查。

```r
summarise_mean_chr <- function(data, col) {
  if (!is.data.frame(data)) stop("data must be a data frame")
  if (!is.character(col) || length(col) != 1 || is.na(col) ||
      !col %in% names(data)) {
    stop("col must be one existing column name")
  }
  if (!is.numeric(data[[col]])) stop("col must be numeric")
  data |> summarise(value = mean(.data[[col]], na.rm = TRUE))
}
```

检查完仍要验证结果形状（每组一行、列名、类型和是否保留分组）。不要把
`enquo()`/`!!` 当作字符串列名的替代；先确定调用者接口，再选择 capture/injection
或 `.data[[ ]]`。

---

## 8. 常见题面与易错对照

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

## 9. 考前作答检查

1. 先写清最终形状：每组一行、原行数保留、list、typed vector、tibble，还是单个值。
2. 分组题确认 group keys、`summarise()`/`mutate()`、`n()`、`first()` 与 `na.rm`。
3. 清理题确认 factor/character 类型、`case_when()` 默认分支、`is.na()` 和 `drop_na()` 的列范围。
4. map 题确认 `.x`、`.f`、输出后缀及 `...` 传参；不要把 list 当向量。
5. 函数题确认参数/defaults、最后表达式返回值、输入检查、错误行为和边界测试。
6. 测试题确认 expectation 与 specification 匹配；数值容差要有理由。
7. 代码题最后检查括号、逗号、列名、对象名、参数和返回类型；不要依赖上一次运行残留的全局变量。

## 主要来源（均为当前学年本地材料）

- `official/current/DSCI_523_r-prog_students/README.md`：Lecture 主题、Quiz 2 日期/权重与课程政策。
- `official/current/DSCI_523_r-prog_students/lec_learning_objectives.md`：Lecture 5–8 learning objectives 与 optional 标记。
- `official/current/DSCI_523_r-prog_students/jupyter-book/lecture-notes/07-mapping-and-nested-data-frames.ipynb`：匿名函数、`map2()`/`pmap()`、nested data frames、list-columns、`nest()`、`map()` 与 `unnest()`。
- `official/current/DSCI_523_r-prog_students/jupyter-book/lecture-notes/08-lecture-tidy-evaluation.ipynb`：data masking、tidy evaluation、`enquo()`/`!!`、`{{ }}`、`:=`、`...` 与可复用函数的 validation。
- `official/current/DSCI_523_r-prog_students/section-001/lecture-5-skeleton-pre.ipynb`：`is.na()`、`group_by()`/`summarise()` 的形状与分组顺序提醒。
- `official/current/DSCI_523_r-prog_students/section-002/lecture5-example-problems.md` 与 `lecture6-example-problems.Rmd`：按组汇总与从 specification 到测试再到函数实现的示例。
- `official/current/DSCI_523_r-prog_students/release/worksheet5/worksheet5.Rmd`：`case_when()`、按列/全表 `drop_na()`、分组汇总与 map 练习。
- `official/current/DSCI_523_r-prog_students/release/worksheet6/worksheet6.Rmd`：函数、数值/错误测试、roxygen2 与 package scavenger hunt。
- `official/current/DSCI_523_r-prog_students/release/worksheet7/worksheet7.Rmd` 与 `release/worksheet8/worksheet8.Rmd`：Lecture 7–8 的最终练习、代码形状与 optional 标记。
- `DSCI_523/notes/resources.md`、`DSCI_523/notes/messages.md`：本地资源索引与课程公告索引。
