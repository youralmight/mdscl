# DSCI 523 Quiz 1：R 数据操作知识复习

## 已确认范围与作答条件

- **范围：Lecture 1–4。**当前 section-001 的 Lecture 4 明确说明：所有 lecture notes 中**未标为 optional**的内容都可考。Quiz 1 占课程总评 **30%**，日期为 **2026-09-15–18**。
- **通用 MDS quiz logistics：**每次 quiz 为 **50 分钟**、在 **PrairieLearn (PL)** 交付；学生在给定 window 内经 **PrairieTest (PT)** 预约偏好的时段，到 **ORCA** 机房现场以 asynchronous format 作答。带学生卡 check-in，并记住 CWL 密码以登录 PL。[MDS Quiz Guidelines](https://ubc-mds.github.io/resources_pages/quiz_guidelines/)
- **代码题：**全部自动评分；语法错误得 0；代码题通常无部分分。应只粘贴产生答案的代码。除非题目另有要求，使用讲义中的 **tidyverse** 方法；用 base R 会失分。workspace 加载需 2–3 分钟，保持打开；包已安装但须在 workspace 用 `library()` 加载。若题目读取文件，文件不在 workspace，按其与代码同目录来写；可用补全、建议和 help。答案框中的包已加载，**不要**粘贴 `library()`；粘贴后保存。

---

## 1. 从文件到可用的表

### 先看文件，再选 reader，再检查结果

目标是把矩形数据正确读成数据框/tibble，而不是只让代码运行。

| 文件实际形状 | 函数与关键参数 | 返回/陷阱 |
|---|---|---|
| 有表头、逗号分隔、无 row names 的 CSV | `readr::read_csv("file.csv")` | 返回 tibble；这是标准 CSV 的首选。|
| 任意纯文本分隔符（例如 TSV） | `readr::read_delim(path, delim = "\t")` | 必须指定 `delim`；没有表头时用 `col_names = FALSE`，否则第一条观测会被错当列名；也可把字符向量传给 `col_names` 来命名列。|
| 文件开头有 metadata | `read_csv(path, skip = 2)` | `skip` 跳过开头行；`n_max` 限制读取的**数据行数**。|
| `.xlsx` | `readxl::read_excel(path, sheet = ...)` | `readxl` 要单独 `library(readxl)`；多 sheet 时以名称或序号指定 `sheet`。URL 的 Excel 先 `download.file()`，再 `read_excel()`。|
| 写 CSV | `readr::write_csv(data, "out.csv")` | 写列名、不写 row names、逗号分隔；返回的主要效果是写出文件。|

`read_csv()` / `read_delim()` 的第一个参数也可为直接指向表格数据的 URL。非语法列名（例如含空格）可用反引号引用：`` `Mother tongue` ``；少数列可 `rename(new = old)`，大量列名可用 `janitor::clean_names()`。

**导入检查：**查看分隔符、表头、metadata、预期列数与类型；读后查看结果。格式“看起来像 Excel”不表示它是 CSV，`.xlsx` 不能用 `read_csv()`。

### 赋值、对象名称与可读代码

- `x <- value` 把名字 `x` 绑定到值；MDS 要求以 `<-` 做对象赋值。`=` 也能赋值，但在函数调用中通常是**命名参数**：`median(x = 1:10)` 不会在全局创建 `x`，而 `median(x <- 1:10)` 会。
- `==` 是比较相等，产生逻辑值；不要把它和赋值混淆。对象名可含字母、数字、`.`、`_`，但不能以数字或 `_` 开头，也不能是 `if`、`for` 等保留字。
- 先让 pipe 在控制台输出并确认正确，再在最前面加 `result <-`；避免把尚未调通的一长串管道直接赋值而隐藏问题。
- 按 tidyverse style：有意义的名字、合理缩进、每个 pipe 步骤一行；可读性是课程 learning objective。

---

## 2. 单表的选择、过滤、计算与形状

`dplyr` 动词以数据框为第一个参数，返回数据框/tibble；在 data-masking 语境中直接写列名，不写 `df$col`。

```r
result <- flights |>
  filter(carrier %in% c("AC", "WS"), delay > 0) |>
  mutate(delay_hours = delay / 60) |>
  select(carrier, delay_hours) |>
  arrange(desc(delay_hours))
```

`|>` 把左边对象作为右边函数的**第一个参数**；`%>%` 是 tidyverse/magrittr 的旧式 pipe，当前 Lecture 1 使用 `|>`。每一步都接收前一步的返回值。

| 要做的事 | 形式 | 返回行为与判断规则 |
|---|---|---|
| 选列 | `select(df, col1, col2)`、`select(df, first:last)` | 保留所有行，只留下所选列；冒号是列位置范围。|
| 筛行 | `filter(df, condition1, condition2)` | 保留所有条件均为 `TRUE` 的行；逗号等价于“且”。若任一条件为 `NA`，该行不会被保留。|
| 多个候选值 | `filter(df, x %in% c("A", "B"))` | `%in%` 对 `x` 的每个元素判断是否在右侧集合中，返回同长度 logical vector；比一串 `x == "A" \| x == "B"` 清楚。|
| “或” | `filter(df, x > 80 \| year == 2026)` | `\|` 是逐元素 OR；`&` 是逐元素 AND。不要用只看第一个元素的 `\|\|` / `&&` 来筛列。|
| 加/改列 | `mutate(df, new = old * 2, old = round(old))` | 保留原列并新增列，或以同名覆盖现有列；同一次 `mutate` 可逗号分隔多个表达式。|
| 排序 | `arrange(df, x, desc(y))` | 按 `x` 升序，再按 `y` 降序；`desc()` 只改变排序方向。|
| 按位置取行 | `slice(df, 1)` | 返回指定行，仍是数据框/tibble。先排序再 `slice(1)` 可取极值所在行。|
| 从表取一列向量 | `pull(df, col)` | 移除表格结构，返回该列向量；例如最终答案要求 character vector length 1 时，常在 `slice()` 后用它。|

### Tidy data 与 pivot 的决策

Tidy data 的三个条件：**一行一个 observation；一列一个 variable；一个 cell 一个 value。**“什么是 observation/variable”由正在回答的统计问题决定。优点是单表动词、可视化和分析可一致地按列工作；代价是比展示型宽表长，供人浏览时不一定最紧凑。

- **列名里藏着变量值**（例如 `1999`, `2000` 是 year）→ `pivot_longer()`：把多列合成 key/value 两列。

  ```r
  wide |> pivot_longer(`1999`:`2000`,
                       names_to = "year", values_to = "cases")
  # 或把 country 留作 identifier：pivot_longer(-country, ...)
  ```

  `cols` 使用 `select()` 风格；`names_to` 是原列名进入的新列，`values_to` 是原 cell 值进入的新列。`everything()` 可选全部列。

- **同一观测分散在多行，某列的值应成为变量名** → `pivot_wider()`：

  ```r
  long |> pivot_wider(names_from = type, values_from = count)
  ```

  `names_from` 提供新列名，`values_from` 提供填入这些新列的值；其余列共同定义一条观测。pivot 前先说明哪一行才是一条 observation；否则即使代码运行，形状也可能不符合问题。

---

## 3. R 的值、类型、结构和索引

### 对象模型与检查

- R 没有独立 scalar；单个值是长度为 1 的 vector。atomic vector 的元素有顺序且须同一类型：`logical` (`TRUE/FALSE`)、`integer` (`1L`)、`double`/numeric (`1`, `1.5`)、`character` (`"a"`)；混合时会强制为能容纳所有值的共同类型（例如 `c(1, "a")` 为 character）。
- `factor` 是带有有限 **levels** 的分类向量；它看似 character，但 level 顺序会影响统计与图形。
- `list()` 可含不同类型、不同长度或嵌套对象。matrix 是同一类型元素的二维向量，用 `[row, column]` 索引；data frame 是特殊 list：每个元素是列向量，所有列等长；行是 observation，列是 variable。
- tibble 是 data frame 子类：默认只打印前 10 行；以二维形式 `df[, 1]` 数字取一列时，base data frame 会简化成向量，tibble 则保留 tibble；`df[1]` 在两者中都保留一列的表格结构。需要时明确 `as_tibble(df)`。

```r
x <- c(1L, 2L)
typeof(x)       # 底层类型，如 "integer"
class(x)        # 类；factor/data.frame/tibble 特别重要
str(x)          # 紧凑结构：类型、长度、内容；适合检查复杂对象
is.integer(x)   # 判断，返回 TRUE/FALSE
as.double(x)    # 强制转换；可能丢失信息，先确认是否合理
```

名称不是值本身：`y <- x` 让两个名字起初指向同一值；修改 `y` 时 R 采用 **copy-on-modify**，因此 `x` 不变。大型 data frame 中改一列只须复制该列，改一行会改到每列、成本更高。

### `[`、`[[`、`$`：先决定要保留还是去掉一层结构

| 对象/操作 | 例子 | 返回 |
|---|---|---|
| vector 用 `[` | `v[2:4]`, `v[-1]`, `v[1]` | 所选元素构成的同类 vector；R 从 **1** 开始计数。|
| list 用 `[` | `lst[1]` | 长度 1 的 **list**（保留一层结构）。|
| list/data frame 用 `[[` | `lst[[1]]`, `df[["mass"]]` | 一个元素/一列本身，去掉一层 list/data-frame 结构。可嵌套：`lst[[6]][[3]]`。|
| data frame 用 `[` | `df[1:5, c("conc", "uptake")]`, `df[1]` | 指定行、列的 data frame；`df[1]` 是一列 data frame。|
| `$` | `df$mass`, `lst$name` | 按名字取单个元素/列，返回底层向量/对象。|

`df[df$cyl == 6, ]` 用 logical vector 选行，是 base-R `filter` 的等价思路；但 Quiz 的数据操作题默认要 tidyverse，除非题目明确要求 base R。

### 向量化计算与逻辑

`+ - * / ^` 和比较 `== != < <= > >=` 逐元素运行并返回相应 numeric 或 logical vector；短向量可 recycling（长度不整除会警告），所以先检查长度。`&`、`|`、`!` 也是逐元素；`&&`、`||` 仅看第一个元素。`NA` 是缺失而非普通值，逻辑/数值运算可能传播 `NA`。

---

## 4. 日期、字符串和分类变量：先把列变成正确的类型

### 日期与时间（`lubridate`）

解析函数名就是输入顺序；`ymd`、`mdy`、`dmy` 接收 character 或未加引号的数字，返回 `Date`。加时间单位的 helper 返回 date-time；`tz` 可使日期变为带时区的 date-time。

```r
d <- ymd("2017-01-31")
dt <- ymd_hms("2017-01-31 20:11:59")
mdy_hm("01/31/2017 08:01")

dates |> mutate(date = make_date(year, month, day))
# make_datetime(year, month, day, hour, minute, second)

year(dt); month(dt); mday(dt); yday(dt)
wday(dt, label = TRUE, abbr = FALSE)  # "Friday"，不是 "Fri"
```

`today()` 给今天的 Date。`interval(start, end)` 创建区间；`date %within% interval` 给逐元素 logical vector，适合 `filter(holiday_date %within% term)`。先把 character 列解析为 Date/date-time 再比较；字符串的字典顺序不等于可靠的日期语义。

### 字符串与 regex（`stringr`）

`str_*` 函数向量化：输入长度为 *n* 的 character vector，通常输出 *n* 个结果。常用 pattern 是普通文字或 regex：`^` 锚定开头、`$` 锚定结尾、`.` 匹配任意字符；R 字符串中的 regex 反斜杠须写成 `"\\"`。

| 目的 | 形式 | 返回/陷阱 |
|---|---|---|
| 检测/筛行 | `str_detect(x, "^Al")`; `filter(df, str_detect(col, "tan$"))` | 每个元素一个 logical；用 `str_detect()` 做部分匹配，`==` 只做完全相等。|
| 保留匹配元素 | `str_subset(x, "fruit")` | character vector。|
| 拆分 | `str_split(x, " ")` | 因每项片段数可不同，返回 list；`str_split_fixed(x, " ", n = 2)` 返回固定列数的 character matrix。|
| 长度/位置子串 | `str_length(x)`；`str_sub(x, 1, 3)` | 前者是每个字符串的字符数，不是 vector 长度；`str_sub(x, 1, 3) <- "AAA"` 可按位置改写。|
| 拼接 | `str_c(a, b, sep = "-")`; `str_c(x, collapse = "-")` | 前者逐元素拼等长向量；`collapse` 把整个向量变为一个 string。|
| 替换 | `str_replace(x, pattern, replacement)` | 每个元素替换第一个匹配；嵌进 `mutate(col = str_replace(col, ...))` 才更新表中该列。|

`tidyr::separate()` 把 data-frame 的一列按分隔符拆成多列；`unite()` 反向合并列。Lecture 3 明确标记为 optional 的 `str_extract*` 和 capture groups 不计入已确认范围。

### Factors：分类的值与显示/分析顺序

在完成文本清理后，才把真正的分类列转 factor：`mutate(tzone = factor(tzone))`。检查 factor 用 `class()`/`str()`、`levels()`、`nlevels()`。过滤行不会自动删除已不存在的 level：

```r
small |> mutate(country = forcats::fct_drop(country))
```

| 目的 | 函数 | 关键行为 |
|---|---|---|
| 按出现频率排序 | `fct_infreq(f)` | 最常见 level 在前；`fct_rev()` 可反转。|
| 按另一个变量排序 | `fct_reorder(f, x, .fun = median)` | 每个 level 按 `x` 的汇总值排序；默认 `median`，可给 `min` 等函数。|
| 指定 level 前置 | `fct_relevel(f, "Asia", "Africa")` | 按明确顺序移动指定 levels。|

factor level 的顺序会改变图例、柱状图和统计分析的参照/顺序；不要把 factor 当普通 character 后再做大量字符串处理。

---

## 5. 两张表：先问“保留谁的行、要不要带右表列？”

Join 通过一个或多个 key 匹配；默认同名 key 会被使用，名称不同则显式声明：

```r
left_join(x, y, by = c("countries" = "country"))
```

`x` 是左/主表，顺序有意义。若 key 在任一表重复，匹配会产生所有组合，行数可能增加；**join 后数行并检查 key 的唯一性**，不能只因得到一张表就认为正确。

| 需求 | 函数 | 行与列的返回 |
|---|---|---|
| 保留 `x` 的全部行，并查入 `y` 的列 | `left_join(x, y)` | mutating join；`x` 中无匹配仍保留，`y` 的列为 `NA`。|
| 只保留两表都有 key 的 `x` 行，并带两表列 | `inner_join(x, y)` | mutating join；没有匹配的两侧行均不在结果。|
| 保留两表所有行和列 | `full_join(x, y)` | mutating join；未匹配侧的列为 `NA`。|
| 只判断 `x` 有无匹配，不带 `y` 列 | `semi_join(x, y)` | filtering join；保留有匹配的 `x` 行，且不会因 `y` 的重复 key 复制 `x` 行。|
| 找 `x` 中没有匹配的行 | `anti_join(x, y)` | filtering join；只返回 `x` 的列。|

`bind_rows()` 是纵向堆表：先检查变量是否对应、类型是否兼容。`bind_cols()` 是按行位置横向拼列，必须由分析者保证行已对齐；通常优先使用有 key 的 join，避免静默错配。

---

## 6. Base R 控制流：分支与逐项重复

这些是明确要求使用 base R 的部分；不要以 `dplyr::filter()` 代替 `if`，也不要用 `if` 处理一整列 logical vector。

```r
if (measure > threshold) {
  print("Over the limit")
} else if (measure < threshold) {
  print("Under the limit")
} else {
  print("Exactly at threshold")
}

for (number in sequence) {
  print(number ^ 2)
}

for (i in seq_along(sequence)) {
  print(sequence[i] ^ 2)
}
```

- `if (condition)` 的 condition 必须是单个 logical；可只有 `if`，也可有任意多个 `else if` 和一个可选 `else`。多行代码块用 `{}`。
- `for (item in vector)` 让 `item` 依次取 vector 的值。需要位置时用 `seq_along(vector)`，再以 `vector[i]` 取值。
- **空向量陷阱：**`seq_along(character(0))` 为空，循环不运行；不要用 `1:length(x)`，因为 `length(x) == 0` 时它生成 `1:0`，会错误迭代。

---

## 考前判断顺序

1. 题目要求的最终**类型**是什么：tibble/data frame、vector、Date、factor，还是打印出的值？
2. 单表任务先选 `filter`/`select`/`mutate`/`arrange`；形状问题先定义 observation，再选 pivot。
3. 两表任务先写清保留哪张表的哪些行，再选 join；检查重复 key 和行数。
4. 字符/日期/分类问题先做类型转换，避免用看似能运行的错误类型操作。
5. 粘贴前检查对象名、逗号、引号、括号和完整 pipe；自动评分下语法正确是最低前提。

## [未确认] 项目

- 课程材料给出 2026-09-15–18 的 Quiz 1 日期 window，但当前仓库未给出各学生可预约的具体 ORCA 时段或地点；以确认后的 MDS quizzes calendar / PT reservation 为准。
- Lecture 4 learning objectives 提到比较 set operations；但当前 section-001 Lecture 4 同时明确说 **“we do not test set operations”**。本笔记以明确的 logistics 为准，未把 set operations 列为已确认可考内容；若教师另有公告，应以该公告更新。
- 当前 Lecture 4 logistics 指向 course coordinators 的 cheat-sheet guidelines，但仓库中未给出 Quiz 1 是否允许、提供还是要求学生自制 cheatsheet，及其资源权限；本知识笔记不推断这些课程特定条件。

## 主要来源（均为当前学年材料）

- `official/current/DSCI_523_r-prog_students/README.md`（Quiz 权重/日期、课程规则）与 `lec_learning_objectives.md`。
- `jupyter-book/lecture-notes/01-intro-to-r-via-tidyverse.ipynb` 至 `04-two-table-joins-and-base-control-flow.ipynb`。
- `section-001/lecture-4-skeleton.ipynb`（Quiz 1 范围、自动评分与 workspace logistics）。
- [MDS Quiz Guidelines](https://ubc-mds.github.io/resources_pages/quiz_guidelines/)（50 分钟、PL、PT、ORCA 的通用 quiz logistics）。
- `release/worksheet1`–`worksheet4`、`release/lab1`–`lab2`，以及 `section-002` 的 lecture 1–3 example problems（当前练习如何应用上述概念）。
