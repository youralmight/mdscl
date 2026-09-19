# DSCI 511 Lab 3：中文题面

本文整理当前提交 `lab3.ipynb` 的题面、数据结构和明确的硬性要求；不包含解题方法、代码或答案。

## 总览

Lab 3 标题为 **Working with DataFrames**。前两题使用加拿大 2016 年人口普查语言数据；后两部分使用 Our World in Data（OWID）的国家年度指标数据，练习读取文件、清理列、索引、筛选、宽长表转换与写出 CSV。

## 数据

### 1. 加拿大语言数据

每行表示一个城市或地区中的一种语言。五个城市文件，以及 `region_lang.csv`，使用下列六个核心字段：

| 字段 | 含义 |
|---|---|
| `category` | 语言类别，例如官方语言、原住民语言、非官方且非原住民语言 |
| `language` | 具体语言或语言组 |
| `mother_tongue` | 该语言为母语的人数 |
| `most_at_home` | 最常在家使用该语言的人数 |
| `most_at_work` | 最常在工作场所使用该语言的人数 |
| `lang_known` | 知道该语言的人数 |

`region_lang.csv` 是全国多个 CMA 合在一起的总表；五份城市文件分别是其中 Vancouver、Abbotsford - Mission、Edmonton、Victoria、Kelowna 这五个 CMA 的单独切片，核心语言字段相同，但单城市文件没有 `region` 列。Exercise 1 要求分别从指定来源读取这五份切片；Exercise 2 则单独指定读取总表 `region_lang.csv`，在全国 CMA 之间比较。总表最左边还有一个未命名的行号列。

Exercise 1 的五份城市数据来源如下：

| 文件 | 必须保存为 | 来源与格式 |
|---|---|---|
| `vancouver_lang.csv` | `vancouver` | 本仓库 `data/` 中的 CSV |
| `abbotsford_lang.xlsx` | `abbotsford` | 本仓库 `data/` 中的 Excel |
| `edmonton_lang.xlsx` | `edmonton` | 题目给出的远程 Excel URL |
| `victoria_lang.csv` | `victoria` | 题目给出的远程 TSV URL；变量名虽写 CSV，实际为 tab-separated 文件 |
| `kelowna_lang.csv` | `kelowna` | 本仓库 `data/` 中的 CSV |

题目说明：若任何语言数据文件没有列名，必须在 Python 中补上列名。

### 2. 全球 GDP 与 Gini 数据

两份 OWID 原始 CSV 都是长格式：每行是一组国家—年份观测。

| 文件 | 原始字段 | 数据形状与用途 |
|---|---|---|
| `gdp-per-capita/gdp-per-capita-worldbank.csv` | `Entity`、`Code`、`Year`、`GDP per capita, PPP (constant 2021 international $)` | 国家/地区、ISO 代码、年份与人均 GDP；`Code` 缺失的记录是如 `World`、收入组等非国家汇总项 |
| `economic-inequality-gini-index/economic-inequality-gini-index.csv` | `Entity`、`Code`、`Year`、`Gini coefficient`、`990179-annotations` | 国家/地区、ISO 代码、年份、Gini 指数，以及大多为空的注释列 |

题目强调，原始长表中“缺失某国某年”常常表现为该国家—年份的**整行不存在**，而不是一个已存在单元格为 `NaN`。将数据转成国家 × 年份的宽表后，这些缺口才会显示为 `NaN`。

## Exercise 1：读取城市语言数据

分别读取上表五份城市数据，并建立指定名称的 DataFrame：

- 1.1：`vancouver`
- 1.2：`abbotsford`
- 1.3：`edmonton`；题目预留变量 `url`
- 1.4：`victoria`；题目预留变量 `url`，并已给出读取时使用 tab 分隔符的框架
- 1.5：`kelowna`

这些小题由可见 autograder 测试评分。必须使用上述变量名。

## Exercise 2：找出西班牙语人数第二的地区

读取 `data/region_lang.csv`，找出加拿大 census metropolitan area 中，**最常在家说西班牙语**的人数排名第二的地区。

将地区名称作为字符串保存为 `spanish2`。题目只要求最终地区名，不要求保留中间结果的特定变量名。

## Exercise 3：清理全球指标数据

题目说明这是练习 Lectures 5–6 核心 Pandas 技能的部分。

### 3.1 清理 GDP 数据

基于原始 GDP 文件建立新的干净 DataFrame：

- 删除 `Code` 是空字符串或 NA 的行，只保留有国家代码的记录；
- 把 `Entity` 改名为 `country`，`Year` 改名为 `year`；
- 将人均 GDP 数值列改名为 `gdp_per_capita`；
- 最终只返回、且按此顺序排列：`country`、`year`、`gdp_per_capita`；
- 清理后 DataFrame 必须命名为 `df_gdp_clean`；过滤后的中间 DataFrame 使用 `df_gdp_countries`。

特殊要求：题面明确说不要手写 GDP 数值列的长列名；应从 `df.columns` 中识别该列。

### 3.2 清理 Gini 数据

基于原始 Gini 文件建立新的干净 DataFrame：

- 删除 `Code` 是空字符串或 NA 的行，只保留有国家代码的记录；
- 把 `Entity` 改名为 `country`，`Year` 改名为 `year`；
- 将真正的 Gini 数值列改名为 `gini_index`；
- 最终只返回、且按此顺序排列：`country`、`year`、`gini_index`；
- 清理后 DataFrame 必须命名为 `df_gini_clean`；过滤后的中间 DataFrame 使用 `df_gini_countries`。

特殊要求：该文件除了 `Entity`、`Code`、`Year` 与指标列外，还有注释列。因此不能只把“不是前三列的任意列”当成数值列；代码必须能区分实际指标列与注释列。

## Exercise 4：处理清理后的全球数据

在这一部分中，`cleaned_frames` 字典固定包含：

```text
"gdp"  -> df_gdp_clean
"gini" -> df_gini_clean
```

### 4.1 缺失值

使用 GDP 数据，并把 `country_to_check` 设为 `"Kosovo"`：

1. 建立 `years_for_country`：其中包含 Kosovo 所有有记录年份的 pandas Series；
2. 求整个 GDP 数据集的最小与最大年份，分别保存为 `overall_min_year` 与 `overall_max_year`；
3. 比较全数据集的年份跨度与 Kosovo 的实际记录年份数；
4. 回答：在这些单独的清理后长表上，`.dropna()` 或 `.fillna()` 是否有用、为什么，以及在哪一步缺失会成为可见问题。

特殊要求：`years_for_country` 必须是 `pandas.Series`。题目提示使用 `.loc[]` 按国家筛选，但这一点是提示，不是强制方法。

### 4.2 索引与列操作

在 GDP 数据上完成四件事：

1. 用 `.loc` 选出 Canada 的全部记录，并按年份排序，保存为 `canada_gdp`；
2. 用 `.iloc` 取前 5 行与后 5 行，分别保存为 `gdp_first_5`、`gdp_last_5`；
3. 计算整个数据集的人均 GDP 平均值和最大值，保存为 `mean_gdp`、`max_gdp`；
4. 按 `gdp_per_capita` 降序排列，显示前 10 行，保存为 `top_10_gdp`。

特殊要求：题面明确分别指定 `.loc` 与 `.iloc` 用于前两项。

### 4.3 筛选

在 GDP 数据中筛选同时符合下列条件的行：

- `year >= 2015`；
- `gdp_per_capita > 40000`。

必须完成两份等价结果：

- 用 `.query()` 得到 `high_gdp_recent`；
- 用普通逻辑运算符 `&` 与 boolean mask 得到 `high_gdp_recent_v2`；
- 确认两份结果相同。

### 4.4 宽表、缺失值与回转长表

以 GDP 数据为基础：

1. 必须用 `.pivot_table()` 建立 `gdp_wide`：每行一个国家、每列一个年份、单元格为 `gdp_per_capita`；
2. 计算整个 `gdp_wide` 的 `NaN` 单元格数量，保存为 `total_missing`；
3. 找出缺失年份最多的国家，保存为 `country_most_missing`；
4. 删除整列全为缺失的年份，结果为 `gdp_wide_trimmed`；再将剩余缺失值填成 0，结果为 `gdp_wide_filled`；
5. 在注释中说明：若之后从该表计算平均值，为什么把缺失 GDP 填为 0 会造成误导；
6. 必须对**原始** `gdp_wide`（不是填 0 后的表）使用 `.melt()` 转回长表；必要时使用 `.reset_index()`；结果为 `gdp_long_again`；
7. 确认转回长表后的非空行数，与原 GDP 长表的行数相同。

特殊要求：本题明确指定 `.pivot_table()`、`.dropna()`、`.fillna()`、`.melt()`，以及在需要时 `.reset_index()`；宽表回转时必须从原始 `gdp_wide` 出发。

### 4.5 写出清理后的文件

把 `cleaned_frames` 中的两份清理数据都写入 `CLEAN_DIR`：

- `gdp_clean.csv`
- `gini_clean.csv`

文件名模式必须是 `{name}_clean.csv`。题目提示使用 `DataFrame.to_csv()`。

## 作业与提交要求

- Lab 在统一 homework deadline 截止；通常是周六下午 6 点，但应以 MDS calendar 或 syllabus 为准；
- 所有运行作业所需的文件必须推送到该 Lab 的 GitHub.ubc.ca 仓库；
- 仓库必须至少有 3 次 commit；
- 向 Gradescope 提交 `.ipynb` 和渲染后的 PDF 或 HTML；整个 notebook 必须已经执行，使助教能看到结果；
- notebook 中不得包含安装套件的代码，例如 `!pip install ...`；
- 有些题提供可见测试；所有题还会由 autograder 或按完成度评分，未自动评分的题也必须体现足够的完成工作；
- 最后一题必须完成 AI 使用声明。

## AI 使用声明

必须说明是否使用 AI 协助完成本作业：

1. 若没有使用，按题面写：

   > I did not use AI in any way to assist me with completing this assignment.

2. 若使用过，则必须：
   - 说明如何使用；
   - 引用所用 AI 工具。
