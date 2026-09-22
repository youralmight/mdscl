# DSCI 511 Worksheet 5–6：中文题面

本文只整理两份当前提交 notebook 中的题面，不包含解题方法或答案。

## Worksheet 5：Working with DataFrames

数据集为 `bcindigenousbiz.csv`，记录卑诗省原住民拥有企业的信息，包括企业名称、城市、坐标、地区、企业类型、行业、成立年份和员工数量等。

数据字段如下：

| 字段 | 含义 |
|---|---|
| `business_name` | 企业名称 |
| `city` | 企业所在城市 |
| `latitude` | 企业地点纬度 |
| `longitude` | 企业地点经度 |
| `region` | BC 经济发展地区 |
| `type` | 企业类型，例如私营公司、合伙企业 |
| `industry_sector` | 企业所属行业领域 |
| `year_formed` | 企业成立年份 |
| `number_of_employees` | 员工人数区间 |

### 1.1

从 `bcindigenousbiz.csv` 导入数据，建立一个名为 `df` 的 DataFrame。

### 1.2

创建一个只包含行业领域列的 DataFrame，保存为 `sector`。

注意：结果必须是 DataFrame，不是 Series。

### 1.3

找出位置为第 1234 行的企业名称，保存为 `business_1234`。

### 1.4

计算整个数据集 `year_formed` 的中位数，保存为 `median_year_formed`。结果应为 `np.float64` 类型。

### 1.5

计算数据集中：

- 不同行业领域的数量，保存为 `n_sector`；
- 不同地区的数量，保存为 `n_region`。

两个结果都应为 `int` 类型。

### 1.6

按 `year_formed` 从最新到最早排序。取排序后前 11 行的 `type` 列，作为 Series 保存为 `sorted_recent`。

### 1.7

创建新的 DataFrame `modified_df`，并新增 `business_age` 列，表示企业年龄。假定当前年份为 2026：

```text
business_age = 2026 - year_formed
```

### 1.8

计算位于 Northeast 地区的企业总数，保存为 `northeast`。结果应为 `int` 类型。

### AI 使用声明

说明是否使用 AI 协助完成作业：

1. 若未使用，写明：
   
   > I did not use AI in any way to assist me with completing this assignment.
2. 若使用了 AI：
   - 描述如何使用 AI；
   - 列出所使用的 AI 工具。

## Worksheet 6：Data Wrangling with Pandas

数据集记录不同国家、不同食物类别的消费量和碳排放量，原始数据来自 Tidy Tuesday 的 `food_consumption.csv`。
Notebook 会从以下地址读取原始 CSV：

```text
https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-18/food_consumption.csv
```

这是 Lecture 1 使用过的同一份数据。原始 `df` 有四列：

| 字段 | 含义 |
|---|---|
| `country` | 国家 |
| `food_category` | 食物类别 |
| `consumption` | 该食物类别的消费量 |
| `co2_emmission` | 对应的二氧化碳排放量；字段拼写按原数据保留 |

Q3 提供的本地 CSV `data/food_consumption2.csv` 已经是长格式，字段为 `country`、`food_category`、`metrics`、`measurements`；其中 `metrics` 的值是 `consumption` 或 `co2_emmission`。


### Q1

创建一个由国家名称构成的 Series：该国的牛肉或禽肉消费量中，至少有一种超过 10kg。保存为 `beef_or_chicken`。

### Q2

原始 DataFrame `df` 中，`consumption` 和 `co2_emmission` 是两个独立的测量列，因此数据对这两个测量维度而言是宽格式。

使用 `.melt()` 将 `df` 重塑为较长的整洁格式，并满足：

- `country` 和 `food_category` 保留为标识列；
- 新列 `metrics` 包含字符串 `'consumption'` 或 `'co2_emmission'`；
- 新列 `measurements` 包含对应的数值测量结果。

保存结果为 `df_melted`。

### Q3

读取 `data/food_consumption2.csv` 并保存为新的 DataFrame `df2`。该文件是原始 `df` 的 melt 后版本。

考虑以下研究问题：

> 食物类别的消费量与该食物类别产生的 $CO_2$ 排放之间是否存在关系？这种关系是否会因食物生产和消费所在的国家而不同？

根据这个问题，判断给出的数据是否整洁；若不整洁，使用适当的 pandas 函数将它整理为整洁数据，并保存为 `df2_tidy`。

注意：本题不能重置索引，也不能修改 `.pivot()` 或 `.melt()` 输出的列名。

### Q4

当调用 `.pivot()` 时若传入多个列名作为 `index`，这些值会成为每一行的名称，而不是常见的整数行索引。

使用 `.reset_index()`，使 `df2_tidy` 恢复为每行以整数命名的常规索引。保存为 `df2_tidy_index`。

### Q5

`.pivot()` 会保留原本的列名，并加入新的第二层列名；双层列名容易造成混淆。

将 DataFrame 的列重命名，使每列只保留一个名称。保存为 `df2_tidy_index_renamed`。

### Q6

每个 `food_category` 都属于以下两个较大类别之一：

- `'Animal Product'`
- `'Plant Product'`

题目提供一个将 `food_category` 映射到上述类别的字典。

在初始 DataFrame `df` 的副本中，使用 `Series.map()` 新建 `food_type` 列；原始 `df` 不得被修改。保存新 DataFrame 为 `df_mapped`。

### Q7

使用 `.groupby()` 和 `.agg()`，或等价的聚合方法，计算每个 `country` 的 `co2_emmission` 总和，并按总排放量从高到低排序。

结果应为 pandas Series，保存为 `co2_by_country`。

### AI 使用声明

说明是否使用 AI 协助完成作业：

1. 若未使用，写明：
   
   > I did not use AI in any way to assist me with completing this assignment.
2. 若使用了 AI：
   - 描述如何使用 AI；
   - 列出所使用的 AI 工具。
