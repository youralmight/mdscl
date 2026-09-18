# DSCI 511 Quiz 2：Pandas 数据处理知识复习

## 范围状态（2026-09-18）

**Quiz 2 的逐项考试范围、练习题与专门 logistics 均尚未由本学期教师发布。** 当前 `official/current/` 的课程 README 只确认 Quiz 2 占总评 25%；课程网站配置把 Lecture 5–7 列为已发布章节，把 Lecture 8 注释掉。`_quarto.yml` 中虽预留了 Quiz 2 practice notebook 的路径，但实际仓库没有该题目；`notes/messages.md` 也没有 Quiz 2 公告。

因此，本文以**已发布、Quiz 1 后的教学材料**建立可审计的复习边界：

- **覆盖：**Lecture 5（DataFrames）、Lecture 6（Pandas data wrangling）、Lecture 7（strings、datetimes、categoricals）；Worksheet 5 的 DataFrame 操作练习、Worksheet 6 的 reshape/map/groupby 练习，以及明确说明练习 Lecture 5–6 核心 Pandas 技能的 Lab 3。
- **不纳入：**Lecture 8（课程表仍标为 testing/generators，且 notebook 未发布）、`appendix_numpy.ipynb` 和 `appendix_plotting.ipynb`，以及尚未发布的 Quiz 2 practice questions。
- **[未确认]：**上述 Lecture 5–7 是否正好等于 Quiz 2 全部范围；其中是否有排除主题；Quiz 2 是否会回考 Quiz 1 的 Python/NumPy 基础。本笔记不是教师公布的范围声明。

---

## 1. DataFrame 的结构、读入与快速检查

```python
import pandas as pd
```

`DataFrame` 是 pandas 表格对象：**列**通常是变量，**行**通常是观测，**index** 是行标签。`Series` 是带 index 的一维列；一个 DataFrame 可视为多个 Series 的集合。两者的区别会直接影响选择后的 type、可用方法和题目答案。

### 1.1 读文件：先弄清分隔符、表头与 index

| 任务 | 常用写法 | 要点 |
|---|---|---|
| 普通 CSV | `pd.read_csv("data.csv")` | 默认首行是列名、逗号是分隔符。 |
| TSV | `pd.read_csv("data.tsv", sep="\t")` | 忘记 `sep` 会把整行误读成一列。 |
| 无表头文件 | `pd.read_csv("x.tsv", sep="\t", header=None)` | 不把首行数据误当列名；pandas 用整数列标签。 |
| 无表头且要命名 | `pd.read_csv("x.tsv", header=None, names=[...])` | `names` 的顺序必须对应文件列顺序。 |
| 表头不在首行 | `pd.read_csv("x.csv", header=2)` | `header` 是从 0 开始的位置；空行是否被读取会影响实际位置，读后检查。 |
| Excel | `pd.read_excel("x.xlsx", sheet_name="Sheet2")` | 默认第一张 sheet；也可传从 0 开始的 sheet 编号。 |
| 读入时指定 index | `pd.read_csv("x.csv", index_col="id")` | 该列成为行标签，不再是普通数据列。 |

`read_csv()` 的第一个参数也可为 URL。读入后不要只凭代码“看起来合理”就继续：先检查列名、shape 和前几行，确认 CSV/TSV、表头和编码设定真的匹配文件。

### 1.2 attribute 不加括号；method 要加括号

| 表达式 | 返回/用途 |
|---|---|
| `df.shape` | `(n_rows, n_cols)`；**attribute**，不要写 `()`。 |
| `df.columns` / `df.columns.to_list()` | 列标签 Index / 普通 list。 |
| `df.head(n)` / `df.tail(n)` | 前/后 `n` 行；默认 5。 |
| `df.info()` | 行数、非缺失计数、dtype、内存等结构信息。 |
| `df.describe()` | 默认数值列的统计摘要；`include="all"` 可包含非数值列。 |
| `s.value_counts()` / `s.nunique()` | 值频数 / 不同值个数。 |

方法通常产生新结果；不要把“看到了输出”误认成原对象已改变。题目若要求保存变换结果，必须赋回名字或赋给新名字。

---

## 2. 选择、index 与向量化列操作

### 2.1 `[]`、`.loc`、`.iloc`：先问“按什么定位？”

| 目的 | 写法 | 基准 | 常见返回 |
|---|---|---|---|
| 一列 | `df["city"]` | 列标签 | `Series` |
| 多列 | `df[["city", "region"]]` | 列标签 | `DataFrame` |
| 按标签取 | `df.loc[row_label, col_label]` | 行/列**标签** | 单值、Series 或 DataFrame |
| 按位置取 | `df.iloc[row_int, col_int]` | 从 0 开始的整数位置 | 单值、Series 或 DataFrame |
| 按位置切片 | `df.iloc[0:5, 1:3]` | 整数位置 | stop 不含，取第 0–4 行、第 1–2 列 |

- 单一选择通常降维：`df["city"]` 是 Series；`df[["city"]]` 才保留 DataFrame。相同原则适用于单行 `df.loc[label]` 与 `df.loc[[label]]`。
- `.iloc` 只能用整数位置（或相应 slice/list/boolean array）；把列名传给 `.iloc` 是错误。
- `.loc` 用 label。默认 RangeIndex 为 `0, 1, ...` 时 `.loc[0]` 与 `.iloc[0]` 恰好看似相同；一旦 `set_index("iso_code")`，二者语义立即不同。
- `df.set_index("key")` **返回新 DataFrame**；`df = df.set_index("key")` 才会让后续 `df.loc[...]` 使用新 index。
- 需要“第 i 个行位置 + 某列名”时写 `df.loc[df.index[i], "col"]`；需要“某行标签 + 第 j 列位置”时写 `df.loc[label, df.columns[j]]`。

### 2.2 不用逐行 loop：整列向量化

```python
scores["Student Mean"] = scores.mean(axis=1)       # 每行均值
scores["Scaled Chemistry"] = scores["Chemistry"] * 1.03
scores["Science Mean"] = (
    scores["Biology"] + scores["Chemistry"] + scores["Physics"]
) / 3
```

列与 scalar、两列之间的运算按相同 index 对齐后逐元素进行。`axis` 决定归约方向：对表 `df`，默认 `axis=0` 给**每列**一个结果；`axis=1` 给**每行**一个结果。因而 `scores.idxmax()` 是每列最大值的行标签，`scores.idxmax(axis=1)` 是每行最大值所在列名；`mean`、`min`、`max` 也遵循相同 axis 规则。

### 2.3 排序、过滤与 `query`

```python
recent = df.sort_values(by="year_formed", ascending=False)

selected = df[(df["region"] == "Cariboo") | (df["region"] == "Kootenay")]
selected = df[(df["industry_sector"] == "Construction") & (df["year_formed"] > 2015)]

selected = df.query("industry_sector == 'Construction' and year_formed > 2015")
```

- `sort_values(by=...)` 默认升序；`ascending=False` 降序。
- 用 boolean mask 时，pandas 用逐元素逻辑运算符 `&`、`|`、`~`，**不用** Python 的 `and`、`or`、`not`；每个比较条件都必须用圆括号包住，避免优先级错误。
- `.query()` 把条件写为字符串，内部可用 `and`/`or`/`not`；列名直接写，不重复 `df[...]`。含空格的列名须用反引号包住；匹配的字符串值用引号。
- `query()` 对长的普通列条件较易读；涉及 Series method（如 `.isin()`、`.str.contains()`）时，boolean mask 更灵活。

---

## 3. 清理与保存：缺失值、删除、改名

### 3.1 `NaN` 是数据，先检测再决定规则

```python
has_na_by_col = df.isna().any()
only_complete = df.dropna()
filled = df.fillna("No source")
```

`NaN` 表示缺失值；不要凭肉眼把空格、空字符串与 NaN 混为一谈。`df.isna()` 返回同 shape 的 bool DataFrame；再用 `.any()` 可按列判断是否至少有一个缺失。`dropna()` 删除含 NaN 的行，`fillna(value)` 用给定值替换 NaN；Lecture 5 的示例中它们都**返回 copy**，不赋值就不会改变 `df`。删除前须判断“缺失的行应该删掉吗？”而不是把 `dropna()` 当成无条件清理。

### 3.2 `drop`、`rename` 与列名

```python
df = df.drop([14379, 54578])          # 按 index 标签删行
df = df.drop(["Art", "Drama"], axis=1)  # 删列

df = df.rename(columns={"language_name": "name", "area": "region"})
df.columns = ["col_a", "col_b", "col_c"]
```

- `.drop()` 按 index label 删除行；`axis=1` 表示删除列。它返回 copy。
- `.rename(columns=mapping)` 只改指定列；mapping 的 key 是旧名、value 是新名，返回 copy。
- 直接赋 `df.columns = [...]` 是整体替换，长度与顺序必须完整匹配当前列，适合确定所有新列名时。reshape 后的 MultiIndex columns 常需先 `reset_index()`，再明确检查/设置列名。
- 保存为 CSV 用 `df.to_csv("out.csv")`；写出前检查是否应同时输出 pandas index，以免意外多出索引列。

---

## 4. Tidy data 与 reshape

### 4.1 先从分析问题判断“tidy”，不是机械追求 long 格式

一份 tidy 数据满足：

1. 每个变量是一列；
2. 每个 observation 是一行；
3. 每种 observational unit 是一张表。

**wide** 与 **long** 只是结构；不是任何场景下谁更“好”。问题若要比较同一 `country`、`food_category` 下的 consumption 与 emissions，这两个测量应成为两列；若原表把同一变量的多个取值塞在列名里，则通常需转 long。先说清“每行应代表什么”，再选操作。

### 4.2 转置、`pivot`、`pivot_table` 与 `melt`

| 目标 | 写法 | 约束/结果 |
|---|---|---|
| 行列互换 | `df.transpose()` | 行和列互换；返回 copy。 |
| long → wide | `df.pivot(index="id", columns="kind", values="value")` | 每个 `(index, columns)` 组合必须唯一；否则报 duplicate-entry 错。参数中的列成为 index/columns。 |
| long → wide，容许重复 | `df.pivot_table(index="id", columns="kind", values="score")` | 相同组合有多行时用它；默认聚合为 mean。可形成多层 columns。 |
| wide → long | `df.melt(id_vars=[...], value_vars=[...], var_name="...", value_name="...")` | `id_vars` 保留并随值复制；原列名进 `var_name`，单元格值进 `value_name`。 |

```python
# 每行 country × sport，列是 medal total：需要唯一的 country/sport 组合
wide = olympics.pivot(index="NOC", columns="Competitions", values="Total")

# 若同一 FirstLanguage × Accent 有多位参与者，pivot_table 默认求平均
means = results.pivot_table(
    index="FirstLanguage", columns="Accent", values="TestPct"
)

long = imdb.melt(
    id_vars=["Director"],
    value_vars=["Star1", "Star2", "Star3", "Star4"],
    var_name="Billing_Order",
    value_name="Actor",
)
```

- `pivot()` 产生的缺格是 `NaN`；这未必表示原数据错误，例如没有获奖牌的国家/项目组合。若业务含义是 0，才使用 `.fillna(0)`；若后续需要整数再用 `.astype(int)`。
- `pivot_table()` 的“默认 mean”是重要考点：它不是凭空选一条重复记录，而是聚合。选择 index/columns 前先识别潜在重复组合。
- 需要保留更细粒度时，`columns=["Accent", "Test"]` 会产生多层 columns；这也会增加缺少组合的 NaN。
- reshape 后想让参与 index 的变量重新成为普通列，写 `result.reset_index()`；它返回 copy。
- `melt()` 若省略 `value_vars`，会 melt 所有不在 `id_vars` 中的列。若要保留某些测量列不被 melt，务必显式写 `value_vars`。

---

## 5. 合并 DataFrame：`concat` 和 `merge` 回答不同问题

### 5.1 `pd.concat`：沿某个 axis 直接接起来

```python
all_days = pd.concat([w1, w2, w3, w4])       # 默认 axis=0，接行
combined_columns = pd.concat([w1, w3], axis=1)  # 接列，按 index 对齐
```

`concat` 的核心是沿共享 axis 拼接：默认叠行，`axis=1` 并列列。它不会理解“两个日期相同就应是同一观测”这一业务关系：列集合不同会产生 NaN，index 相同也可能留下重复行/重复列。应先决定这些表是否真的已按位置和 index 对齐。

每次 `pd.concat` 都创建新的 DataFrame；要合并多个同类表时，先收集为一个 list、一次性 concat，而不是在 loop 中逐个 concat。

### 5.2 `pd.merge`：按 key 做关系型匹配

```python
outer = pd.merge(w1, w4, how="outer", on=["Date/Time", "Month", "Year"])
by_index = pd.merge(w1, w4, how="outer", left_index=True, right_index=True)
with_season = pd.merge(
    left=weather, right=seasons, how="left", left_on="Month", right_on="month"
)
```

`merge` 适用于“哪些行是同一个实体/观测”由 key 决定的情形；不是按物理行号粘贴。`on` 用两表同名 key；名称不同则用 `left_on`/`right_on`；要按 index 匹配用 `left_index=True` 与 `right_index=True`。

- `how="outer"` 保留两边的全部 key；只能在一边找到的资料在另一边字段为 NaN。
- `how="left"` 以左表的 key 为主，常用于为主表加 lookup 属性。
- `how="right"` 以右表的 key 为主。
- 按列 `on` merge 会建立新的默认 index；原 index 不会自动保留。
- join 前检查 key 的含义和重复：`merge` 可进行 one-to-one、one-to-many 或 many-to-many；重复 key 会使行数增长。行数突然暴增首先检查 key 是否唯一，而不是盲目删重。

---

## 6. 自定义函数、`map` 与分组聚合

### 6.1 `.apply()` 与 `.map()`：输入形状决定选择

| 操作 | 函数接收什么 | 作用范围 | 典型写法 |
|---|---|---|---|
| `df.apply(func, axis=0)` | 一列 Series（默认） | DataFrame 按列 | `df[["a", "b"]].apply(np.sum)` |
| `df.apply(func, axis=1)` | 一行 Series | DataFrame 按行 | 用行内多列计算时 |
| `df.map(func)` | 一个 scalar | DataFrame 每个元素 | `df.map(round)` |
| `s.apply(func)` | 一个 Series 的逐值应用 | Series | `s.apply(int)` |
| `s.map(mapping_or_func)` | 单值；也可查 dict | Series | `s.map({"Winter": "Cold"})` |

对能接收/返回单个值的函数（如 `round`），`apply` 与 `map` 可能看似一样；但 `np.sum` 这类接收 array/Series、返回单值的函数会显露差别：`df.apply(np.sum)` 给按列 summary，`df.map(np.sum)` 是错误的形状匹配。`Series.map(dict)` 中找不到的 key 会变成 `NaN`，所以 map 后要检查是否每个类别都有映射。

给既有 DataFrame 新增列会改变对象。题目若要求保留原表，先写 `new_df = df.copy()`，再在 `new_df` 上赋值。

### 6.2 `groupby`：split → aggregate，而不是一个普通 DataFrame

```python
co2_by_country = (
    df.groupby("country")["co2_emmission"]
      .sum()
      .sort_values(ascending=False)
)

summary = (
    imdb.loc[:, ["Released_Year", "IMDB_Rating", "Meta_score", "No_of_Votes"]]
        .groupby("Released_Year")
        .agg(["mean", "sum", "count"])
)

custom_summary = imdb.groupby("Released_Year").agg(
    imdb_avg=("IMDB_Rating", "mean"),
    meta_score_avg=("Meta_score", "mean"),
)
```

`df.groupby(by=...)` 先创建 `DataFrameGroupBy`：每个 group key 对应一组原行。通常不直接阅读该对象，而是选定值列并 aggregate：`.mean()`、`.sum()`、`.count()`，或 `.agg()`/`.aggregate()`。

- 先选择数值列再 aggregate，可避免非数值列干扰；`mean(numeric_only=True)` 也可明确忽略非数值列。
- `.agg(["mean", "sum", "count"])` 对选择的每个数值列施加多个函数；传 dict 可为不同列指定不同函数。
- `groupby(["Released_Year", "Certificate"])` 按两个变量的已出现组合分组；结果 index 是这些组合。
- 未 `groupby` 的 `df.agg(...)` 是对整张表进行 summary；可用于多项整体统计。
- 分组结果是否要 `reset_index()` 取决于后续是否把 group key 当普通列使用；题目要的 `Series` 不要无故转为 DataFrame。

---

## 7. 字符串、日期时间与类别变量

### 7.1 pandas 字符串操作：在 Series 前加 `.str`

```python
genres = imdb["Genre"].str.split(",", expand=True)
genres[1] = genres[1].str.strip()
```

普通 Python 字符串有 `.find()`、`.replace()`、`.join()` 等 method；列是 Series 时，不能把它当一个 string 调用这些 method，而是经 `Series.str` 向量化调用。上例 `split(..., expand=True)` 将每条字符串拆为多列；分隔符后出现的空白仍在结果中，故再对相应列使用 `.str.strip()`。做清理前后都应检查一个具体单元格，确认去的是空白而非有效字符。

Lecture 7 的 regex 示例标为 **OPTIONAL**，并明确写明 DSCI 521 会进一步教授 regex；本材料不把 regex 语法列为本次复习内容。

### 7.2 pandas 的时间对象与创建

| 对象 | 表示什么 | 创建/例子 |
|---|---|---|
| `Timestamp` | 一个时间点 | `pd.Timestamp("2005-07-29")` |
| `Period` | 一段时间（如一天） | `pd.Period("2005-07-09")`；有 `.start_time`、`.end_time` |
| `Timedelta` | 时间间隔/持续时间 | `pd.Timedelta("1.5 hours")`；可加到 date/period range |
| `DateOffset` | 日历偏移规则 | 时间运算所用的 offset 类型 |
| `DatetimeIndex` / `PeriodIndex` | 一列/数组式时间 index | `pd.date_range(...)` / `pd.period_range(...)` |
| `NaT` | 缺失的日期时间 | pandas 的 datetime 缺失值 |

```python
point = pd.Timestamp(year=2005, month=7, day=9)
span = pd.Period("2005-07-09")
dates = pd.date_range("2020-09-01 12:00", "2020-09-11 12:00", freq="2D")
periods = pd.period_range("2020-09-01", "2020-09-11", freq="D")

df["Date"] = pd.to_datetime(df["Date"])
```

`Timestamp` 是点，`Period` 是有边界的 span；不要把两者混作同一个概念。字符串日期先由 `pd.to_datetime()` 转换；一列日期格式混杂时，Lecture 7 给出的 `format="mixed"` 可逐值推断。也可在 `read_csv` 时解析日期并以其为 index，例如 `parse_dates=True, index_col=0`，但读入后仍需检查得到的 index 是否真是 datetime。

### 7.3 DatetimeIndex：选取、拆分和重采样

```python
cycling.loc["2019-10"]                         # 2019 年 10 月
cycling.sort_index().loc["2019-10-01":"2019-10-13"]
cycling.between_time("00:00", "01:00")

s.dt.year                                       # Series 的 datetime accessor
cycling.index.weekday                           # DatetimeIndex attribute
weekly = cycling[["Time", "Distance"]].resample("1D").mean()
```

- DatetimeIndex 支持**部分字符串索引**（年月等）和普通 selection。按日期范围 slice 前需 index 有序；未排序的 index 可能报错，`sort_index()` 后再切。
- 对 DatetimeIndex 直接取 `.weekday`、`.second`、`.day_name()`、`.month_name()` 等；对 datetime **Series** 用 `.dt`，如 `s.dt.year`。`s.year` 不可用。
- `.between_time(start, end)` 按一天中的时刻选记录。
- `.resample(freq)` 类似专为时间 index 设计的 `groupby`，先产生 Resampler；必须接 aggregate（如 `.mean()`）才得到每个时间桶的结果。`"1D"` 表示每天；课程列出 `h`、`min`、`s`、`B`、`MS`、`ME` 等常用频率。没有观测的桶常得到 NaN，是否填 0 要由业务含义决定。

### 7.4 `category`：有限取值、顺序和清理次序

```python
bean["Class"] = bean["Class"].astype("category")
bean["Class"].cat.categories

order = ["single author", "indie", "small/medium", "big five"]
pub["publisher.type"] = pd.Categorical(
    pub["publisher.type"], categories=order, ordered=True
)
pub = pub.sort_values("publisher.type", ascending=False)
```

category 适用于取值数有限、通常固定的变量。它内部以 categories 和 codes 存储，重复值多时可减少内存，并可改善某些 `groupby`/sort 操作；最关键的是可表达**非字母顺序**的有序等级。

- `astype("category")` 将现有列转为 category；用 `s.cat.categories` 查看 level。
- `pd.Categorical(..., categories=order, ordered=True)` 明确指定 categories 和排序语义；字符串默认按字母排序，不代表业务顺序。
- **先清理、后转 category。** 如 `'comics'` 与 `'Comics'` 实为同一类别，先标准化文本；否则 category 会把它们当不同 level。

---

## 8. 读题与查错清单

1. **先写出对象结构。** 是 DataFrame 还是 Series？列名、index、shape、dtype 分别是什么？
2. **选择前确认基准。** 题目给的是 label 还是从 0 开始的位置？要一列 Series 还是一列 DataFrame？
3. **每一步问“是否返回 copy？”** `set_index`、`drop`、`fillna`、`rename`、`reset_index`、`sort_values` 和 reshape 的结果若不赋值，原变量不会自动替换。
4. **过滤逐条件加括号。** boolean mask 中使用 `&`/`|`/`~`，不用 `and`/`or`/`not`；长条件可先分开命名 mask 再组合。
5. **reshape 先定义一行代表什么。** `pivot` 前检查 index/columns 组合是否唯一；重复时用 `pivot_table`，并说明它应如何 aggregate。
6. **合并先说 key，再看行数。** `concat` 是沿轴拼接；`merge` 是依 key 匹配。merge 后行数异常增长通常意味着重复 key 形成 many-to-many。
7. **`apply` 与 `map` 先看函数输入。** 函数吃 Series/array 时选 `apply`；吃 scalar 时选 `map`；`Series.map(dict)` 的未映射值会成为 NaN。
8. **日期先转换且排序。** `pd.to_datetime` 后才有 datetime 操作；日期范围 slicing 先 `sort_index()`；Series 用 `.dt`，DatetimeIndex 直接用其属性。
9. **类别先清理再排序。** `category` 的顺序不是文本字母序时，明确给 `categories` 与 `ordered=True`。

---

## 主要来源

- 本学期课程 README：课程学习目标、Lecture 5–8 主题表、Quiz 2 评分权重，`official/current/DSCI_511_py-prog_students/README.md`。
- 已发布课程章节边界及 Quiz 2 practice/Lecture 8 未发布状态：`official/current/DSCI_511_py-prog_students/_quarto.yml`。
- 本学期 Lecture 5：DataFrame 读入、检查、indexing、向量化、排序、清理、过滤，`official/current/DSCI_511_py-prog_students/lecture-notes/lecture5.ipynb`。
- 本学期 Lecture 6：tidy data、reshape、concat/merge、apply/map、groupby/agg，`official/current/DSCI_511_py-prog_students/lecture-notes/lecture6.ipynb`。
- 本学期 Lecture 7：`Series.str`、datetime、resample、categorical；其中 regex 段明确为 OPTIONAL，`official/current/DSCI_511_py-prog_students/lecture-notes/lecture7.ipynb`。
- 已发布练习：Worksheet 5（DataFrames）与 Worksheet 6（filter/melt/pivot/reset_index/map/groupby），分别在 `official/current/DSCI_511_py-prog_students/worksheets/worksheet5/student/worksheet5.ipynb`、`worksheets/worksheet6/student/worksheet6.ipynb`。
- 已发布 Lab 3：明示练习 Lectures 5–6 的 core Pandas skills，`official/current/DSCI_511_py-prog_students/labs/lab3/student/lab3.ipynb`。
