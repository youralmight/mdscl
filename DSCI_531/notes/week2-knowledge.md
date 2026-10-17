# DSCI 531 第二周：统计摘要、分布与探索性数据分析

## 范围与阅读路线

当前课程 README 指定 Lecture 3 阅读 **Ch7–8**，Lecture 4 阅读 **Ch9–12、15，其中 Ch11 optional**。本文覆盖当前在线课程书 2026-10-15 版本的 Ch7–10、12、15，并把 Altair 与 ggplot2 的同一原则并列说明；Ch11 累积分布按 optional 不作为主线。Lab 2 仅用于核对应用范围，不给原题答案。**这是第二周知识笔记，不是已确认的 Quiz 1 范围，也不是 cheat sheet。**

## 1. 摘要是压缩：先说保留了什么、丢掉了什么

多个观测可以压缩成中心、离散程度或数量。压缩使组间比较更容易，但不同数据可能共享相同摘要，因此不能把摘要当成原始分布。

### 1.1 中心位置

- **Mean：**$\bar x=\frac{1}{n}\sum_i x_i$。每个值都参与，极端值影响大；总量/期望意义常使 mean 有价值。
- **Median：**排序后中间位置。对长尾和少量极端值更稳健；但不表示极端值“不重要”。
- **Mode：**最常出现的值或区间；连续数据的结果依赖测量精度/分箱。

选择不是“偏态永远用 median”的机械规则，而要看问题：想知道总资源、平均负担、典型个体，答案可能不同。最好同时看 mean、median 与原始分布。

### 1.2 离散程度

- **Standard deviation（SD）**描述观测相对 mean 的 spread；mean ± SD 是描述性摘要，不是 confidence interval。
- **Percentiles**按排序位置给阈值；IQR = Q3 − Q1。
- **Boxplot：**箱体 Q1–Q3，中线 median；默认 whiskers 通常延伸到距箱体不超过 1.5 IQR 的最远观测，超出的点单画。whisker 不是 min/max，也不是“统计异常错误”。

**描述性 spread**回答“观测值有多分散”；**inferential uncertainty**回答“估计值跨重复样本有多不确定”。二者都常画成 error bar，但不能混称。

## 2. 在图上计算摘要

### 2.1 Altair

```python
base = alt.Chart(df).encode(y="group:N", x="value:Q")
means = base.mark_circle(color="black").encode(x="mean(value):Q")
spread = base.mark_errorbar(extent="stdev")
means + spread
```

- `mean(value)`、`median(value)`、`sum(value)` 是 encoding aggregate。
- `mark_errorbar(extent="stdev")` 从原始观测计算 mean ± SD。
- `mark_boxplot()` 计算箱线图摘要。
- layer 中每层可有不同 aggregation；需确认它们使用同一数据与 grouping。

### 2.2 ggplot2

```r
ggplot(df, aes(y = group, x = value)) +
  geom_point(stat = "summary", fun = mean) +
  geom_pointrange(
    stat = "summary",
    fun.data = mean_sdl,
    fun.args = list(mult = 1)
  )
```

- geom 负责画法，stat 负责数据变换；`geom_point(stat="summary")` 与 `stat_summary(geom="point")` 可表达同一件事。
- `fun` 返回单一摘要；`fun.data` 返回中心与上下界。
- `mean_sdl` 依赖 Hmisc；缺包时 layer 可能被省略，需看 rendering warnings。
- `geom_boxplot()` 计算 boxplot。`geom_jitter()` 默认会同时 jitter x 与 y；它不会自动识别哪个轴是 quantitative。

### 2.3 摘要和原始观测一起画

jitter 只能用于减少 overlap，不能随意移动表示数值的坐标。横向 quantitative x-axis 应显式固定 `width = 0`，只沿 categorical y-axis jitter：

```r
ggplot(df, aes(y = group, x = value)) +
  geom_jitter(width = 0, height = 0.1)
```

若 quantitative value 在 y-axis，则反过来设 `height = 0`。样本很小时直接显示每个点；样本大时结合 histogram/density/rug。

## 3. Counts、bars 与 proportions

### 3.1 Count 是在数什么

先定义 observational unit。一部电影展开多个 genres 后，一行是 film–genre membership，不再是一部独立电影。`count()` 的结果必须用“rows / memberships / people / days”中的正确名词解释。

```python
alt.Chart(df).mark_bar().encode(
    x="count():Q",
    y=alt.Y("category:N").sort("-x")
)
```

```r
ggplot(df, aes(y = category)) + geom_bar()
```

- Altair `count()`、ggplot `geom_bar()` 默认 `stat="count"` 均按组数行。
- 已经预聚合出 `n` 时，ggplot 用 `geom_col(aes(x=n))`；不要再 count summary rows。
- bar 用长度表示从零累积的 count/sum，通常必须从 zero baseline 开始。
- categories 无自然顺序时按值排序方便比较；星期、等级等有语义顺序时保留该顺序。
- 不推荐用 bar 表 mean/median：bar 从零填充的面积暗示累积量，也会造成 within-the-bar bias。

### 3.2 Stacked 与 side-by-side

- stacked bar 适合总量优先、组成次要；中间 segments 没有共同 baseline，精确比较困难。
- grouped/dodged bar 让每组都从零开始，适合跨组比较 components。
- Altair 可用 `yOffset`/`xOffset`；ggplot 用 `position="dodge"`。

### 3.3 Proportion 的 denominator 必须写清

$$\text{proportion}=\frac{\text{subgroup count}}{\text{relevant total}}.$$

“所有电影中既是 horror 又是 R 的比例”、“horror 内 R 的比例”、“R-rated 内 horror 的比例”分母不同，回答不同问题。

- Altair normalized stack：`alt.X("count()").stack("normalize")`。
- ggplot：`geom_bar(position="fill")`。
- normalized bar 隐藏 group size；需要时同时报告 counts。
- 两部分 stacked proportion 可借助 0 与 100% 两端比较；三部分以上中间 segment 仍难比较。
- pie chart 用 angle/area，通常不如共享 baseline 的 bar 精确；仅在类别很少、强调简单 part-to-whole 时考虑。

## 4. Histogram：把数值轴分箱再计数

连续值很少完全相同，逐值 count 会很碎。Histogram 将 quantitative axis 分成 intervals，并计算每个 interval 中的 observations。

```python
alt.Chart(df).mark_bar().encode(
    x=alt.X("value:Q").bin(step=5),
    y="count():Q"
)
```

```r
ggplot(df, aes(x = value)) +
  geom_histogram(binwidth = 5, boundary = 0, color = "white")
```

### 4.1 两个必须检查的设计选择

1. **Bin width：**窄 bin 显示细节但噪声多；宽 bin 平滑但可隐藏 clusters/gaps。
2. **Bin origin / boundary：**相同宽度只移动边界也可改变峰形。

用变量单位选择有意义的 width，并尝试多个设置。不同 width 下每个 bin count 改变很正常，不表示总样本数变了。不能只挑支持预期故事的分箱。

### 4.2 加回观测与比较多组

- Rug plot 用 tick 标出观测位置。Altair 将 tick chart 与 histogram 垂直 concatenate 并共享 x-scale；ggplot 用 `geom_rug()`。
- 多组 histogram 叠加易遮挡；只有 2–3 组且分布分开时可用透明度。
- 多组比较通常 facet 成单列，并保持相同 bin boundaries、x-scale；否则 panel 形状不能直接比较。

## 5. KDE / density：以每个观测为中心做平滑

Kernel density estimation 在每个 observation 上放一个 kernel，将贡献相加并归一化，使整条 density curve 面积为 1。

- **Height 是每 x-unit 的 density，不是某点概率。**区间概率对应曲线下面积。
- 改变 x 单位会改变 numerical density height；同一分布按分钟与秒表示，高度不同。
- 每组 density 都归一化为面积 1，因此 taller peak 表示组内更集中，不表示 observations 更多。

```python
alt.Chart(df).transform_density(
    "value", as_=["value", "density"], bandwidth=2
).mark_area().encode(x="value:Q", y="density:Q")
```

```r
ggplot(df, aes(x = value)) + geom_density(bw = 2)
```

### 5.1 Bandwidth

- 小 bandwidth：曲线更 wiggly，可能显示局部结构，也可能追随 sampling noise。
- 大 bandwidth：更 smooth，突出总体形状，但可能抹掉 multimodality。
- bandwidth 用原变量单位表达；应尝试多个合理值。ggplot 可用 `bw="SJ"` 选择 Sheather–Jones rule。

### 5.2 Density 的风险

- Gaussian kernels 可把 density 延伸到不可能范围，如负时长。裁掉显示范围只隐藏 tail，不会自动修正 boundary bias 或重新归一化。
- 5 个点和 500 个点都可产生光滑 curve；smoothness 不代表证据多。报告 $n$，必要时加 rug/points。
- count-scaled density 的总面积等于 sample size，但高度仍是每单位 x 的 rate，不是 histogram bin count。

### 5.3 多组与 violin

- density lines 可把几个组靠近比较，但颜色太多会乱；facet 更清楚。
- violin plot 是镜像 density；厚度表示 concentration，不是 raw count，除非明确采用 count scaling。
- violin 的镜像没有增加统计信息。最好结合 median/boxplot/points，并说明 scaling 与 bandwidth。

## 6. Joint distributions：保留变量之间的配对

两个变量各自的 marginal counts 不能告诉我们组合 count。Joint distribution 描述 observations 落在值组合上的分布。

### 6.1 两个 categorical variables

将类别放 x/y，把 combination count 映射到 color 和/或 size：

```python
alt.Chart(df).mark_circle().encode(
    x="category_a:N", y="category_b:N",
    color="count():Q", size="count():Q"
)
```

```r
df |>
  dplyr::add_count(category_a, category_b) |>
  ggplot(aes(x = category_a, y = category_b, color = n, size = n)) +
  geom_point()
```

color + size 提供冗余 cue，能区分大/小 count；heatmap 只用 color，结构紧凑但精确比较不如 position/length。类别有 natural order 时不要仅按 count 重排。

必须区分：

- **joint count / proportion：**组合占全体多少；
- **marginal count：**某一变量单独的组数；
- **conditional proportion：**在某 row/column group 内，各组合占多少。

### 6.2 两个 quantitative variables：2D histogram

scatterplot 严重 overplot 时，透明度也无法区分密度。2D histogram 同时分 x/y bins，用 cell color 表 count：

```python
alt.Chart(df).mark_rect().encode(
    x=alt.X("x:Q").bin(step=0.1),
    y=alt.Y("y:Q").bin(step=500),
    color="count():Q"
)
```

```r
ggplot(df, aes(x, y)) + geom_bin_2d(binwidth = c(0.1, 500))
```

与 1D histogram 一样，bin sizes 会改变可见结构；尝试多个有意义设置。

## 7. EDA：从预期、观察到下一次检查

Exploratory data analysis 是一个循环：

> 形成有来源的预期 → 检查数据 → 找到一致或意外之处 → 提出多个解释 → 做能区分解释的下一次检查。

EDA 不是无目的地把每列画出来，也不是看到异常就修数据。

### 7.1 先确认数据表示什么

- 一行是什么 observational unit？有没有 repeated measures 或 membership expansion？
- columns 的定义、单位、采集时点和可取范围是什么？
- row count、distinct IDs、日期覆盖是否一致？正确行数也可能同时藏一个重复和一个缺失。
- 数值 dtype 不代表是 measurement；ID、postal code 不能机械放进 histogram/correlation。

### 7.2 Broad overview 的三个部分

1. 每个 quantitative variable 的 distribution；每个 categorical variable 的 counts。
2. variables 之间的 relationships，例如 pairs plot。
3. missingness：每列 missing count/percentage，以及 missing 落在哪些 observations、时间或 groups。

Altair `repeat` 是把同一 chart specification 替换成不同 variables；facet 是把同一个 variable 按 observations 的 group 分 panel。ggplot 常把多列 `pivot_longer()` 后 facet。

### 7.3 Missing values 是数据故事的一部分

`NA` 可能来自设备失败、未提问、不适用、拒答或 join 失败；编码成 `999` 的 missing 不会被 `isna()` 发现。反过来，合法 0（例如无降水）不能当 missing。

只报告“8% missing”不够。要检查 missingness 是否与日期、group 或其他 observed variable 有结构。发现 association 只支持进一步调查，不证明缺失机制。不要机械地填 0 或删除整行；这会分别伪造具体值或丢掉其他有效 measurements。

### 7.4 异常与 follow-up

| 初始观察 | 可能解释 | 有用检查 |
|---|---|---|
| 两个 peaks | 隐藏 subgroups、rounding、bin choice | 分组、查原值、改 bin/bandwidth |
| extreme value | 真异常、单位错、录入错 | 查该 row、相关列与 provenance |
| 某组 curve 更高 | 更集中或 scaling，不一定人数多 | 报 counts 与 normalized shapes |
| pooled association | 组内关系或组间差异 | color/facet by plausible group |
| transformation 后 rows 增多 | memberships 被展开 | 同时数 rows 与 distinct units |

“删除后图更干净”不是删除依据。任何 exclusion 都要有理由和记录。

### 7.5 围绕 outcome 的 EDA

可以固定 outcome，分别画它与 candidate predictors 的关系。仍需问：predict 时 feature 是否可用？用事后记录的信息预测结果会造成 target leakage。

Correlation heatmap 可导航，但不能替代 plots：

- Pearson 总结 linear association；Spearman 总结 rank-based monotonic association。
- U-shape 可有接近 0 correlation；组合关系也可能在单变量中看不见。
- pairwise complete observations 使不同 cells 使用不同 subsets。
- correlation 不证明因果。

ML 场景中，影响 feature selection、transformations 的 EDA 应只用 training data；time-dependent task 还需考虑 chronological split。

### 7.6 记录结论与仍未解决的问题

EDA 的交付不应只剩一组图。每次重要调查至少留下以下记录：

| 项目 | 要写什么 |
|---|---|
| expectation | 根据 documentation、采集过程或领域知识，原本预期看到什么 |
| observation | 实际看到了什么；说明涉及的变量、单位、group 与有效样本 |
| competing explanations | 至少列出仍与现象相容的解释，不把第一种猜测当事实 |
| checks | 做了哪些 follow-up；每项排除了什么、仍不能排除什么 |
| supported conclusion | 当前证据真正支持的最窄结论 |
| unresolved | 仍缺哪些数据、provenance 或领域信息；下一步是否必须找 data provider |

“机制仍未确认”是有效结论。若现有 variables 不能回答业务问题，也应明确停止，而不是继续画图制造确定感。最终沟通只保留与问题和重要决策相关的图，但要保存足够的 reasoning trail，使 exclusions、transformations 与结论可以追溯。

## 8. 快速选择表

| 问题 | 起点 | 必查项 |
|---|---|---|
| 各组典型值与 spread | points + mean/median + SD/IQR | 原始 shape、outliers、error bar 含义 |
| 类别多少 | count bar | observational unit、zero baseline、排序 |
| 类别构成 | count + conditional proportion | denominator 与 group size |
| 一个数值分布 | histogram / density + rug | bin/bandwidth、n、boundaries |
| 多组分布 | facets / density lines / violin | shared scales、normalization、group size |
| 两类别组合 | count heatmap / sized points | joint vs conditional |
| 两连续变量过密 | 2D histogram | x/y bin sizes |
| 新数据 EDA | distributions + relationships + missingness | provenance、units、next check |

## 来源、版本与材料边界

### 当前课程来源

- [当前课程 README](/Users/youralmight/workspaces/reps/mdscl/DSCI_531/official/current/DSCI_531_viz-1_students/README.md)：Lecture 3 = Ch7–8；Lecture 4 = Ch9–12、15，Ch11 optional。
- [Ch7 Central tendency & spread](https://joelostblom.github.io/viz-oer/7_summaries.html)
- [Ch8 Counts & proportions](https://joelostblom.github.io/viz-oer/8_counts.html)
- [Ch9 Binned distributions](https://joelostblom.github.io/viz-oer/9_binned-distributions.html)
- [Ch10 Smoothed distributions](https://joelostblom.github.io/viz-oer/10_smoothed-distributions.html)
- [Ch12 Joint distributions](https://joelostblom.github.io/viz-oer/12_joint-distributions.html)
- [Ch15 Exploratory data analysis](https://joelostblom.github.io/viz-oer/15_exploratory-data-analysis.html)

### 应用材料

- [Lab 2 Python 题面，仅用于确认应用知识](/Users/youralmight/workspaces/reps/mdscl/DSCI_531/assignments/lab2-py/DSCI_531_lab2-py_yz2000/lab2_py.ipynb)
- [Lab 2 R 题面，仅用于确认应用知识](/Users/youralmight/workspaces/reps/mdscl/DSCI_531/assignments/lab2-r/DSCI_531_lab2-r_yz2000/lab2_r.qmd)

### 边界

- Ch11 cumulative distributions 是本周 optional，本文不把 ECDF 当必学主线。
- 当前在线书发布日期为 2026-10-15；本文按该版本整理。未公开的口头说明、iClicker 题与登录后材料标为未确认，不推断内容。
- Lab 2 只确认 boxplot、density/violin、histogram、repeat/facet、counts、joint categories 与 EDA 的应用范围；本文没有填写任何 Lab 变量、原题分析结论或可提交答案。