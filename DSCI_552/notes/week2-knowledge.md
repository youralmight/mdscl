# DSCI 552 第二周：Bootstrap 置信区间与置换检验

## 范围与阅读方式

按 2026/27 当前 README 的 Lecture 3–4 整理：**Confidence Intervals via Bootstrapping** 与 **Hypothesis Testing via Permutation**。覆盖两讲 11 项 learning goals、当前 lecture notes/slides 和 Lab 2 所需概念；Lab 题面只用于识别应用范围，不生成作业答案。**这是第二周完整知识笔记，不是已确认的 Quiz 1 范围，也不是 cheat sheet。**

## 1. 从 point estimate 到 interval estimate

用一个样本计算的统计量通常不会刚好等于未知总体参数。Point estimate 给一个数；confidence interval（CI）给一段按指定程序构造的 plausible values，并用 repeated-sampling coverage 描述该程序的可靠性。

设目标参数为 $\theta$，样本估计为 $\hat\theta$。区间写作

$$[L(X),U(X)],$$

其中端点取决于随机样本 $X$。样本改变，端点也改变；参数 $\theta$ 在 frequentist 框架下是固定未知量。

### 1.1 95% confidence 的正确解释

若用同一 sampling design 与同一 95% CI procedure 重复取样并构造许多 intervals，长期约 95% 的 intervals 会覆盖真实参数。

对已经得到的一条具体 frequentist interval，不应说“参数有 95% 概率在这里”。区间构造前是随机的；构造后端点已固定。课程中的自然语言“95% confident”是对 procedure reliability 的简写。

CI 不保证：

- 本次区间一定覆盖参数；
- 样本具有代表性；
- 参数落在区间正中央；
- 区间内各值同样可信；
- 估计无 bias 或研究设计无问题。

## 2. Percentile bootstrap confidence interval

给定原样本 $x_1,\ldots,x_n$：

1. 从这 $n$ 条记录中**有放回**抽 $n$ 条，得到 bootstrap sample。
2. 计算同一个 statistic，得到 $\hat\theta^{*(1)}$。
3. 重复 $B$ 次，得到 bootstrap distribution。
4. 对 $(1-\alpha)100\%$ percentile CI，取 bootstrap estimates 的 $\alpha/2$ 与 $1-\alpha/2$ quantiles。

例如 95% CI 取 2.5th 和 97.5th percentiles；90% 取 5th 和 95th；99% 取 0.5th 和 99.5th。

### 2.1 `infer` pipeline

```r
set.seed(552)
bootstrap_estimates <- sample_df |>
  specify(response = measurement) |>
  generate(reps = 2000, type = "bootstrap") |>
  calculate(stat = "mean")

ci <- bootstrap_estimates |>
  get_confidence_interval(level = 0.95, type = "percentile")
```

对二元比例：

```r
sample_df |>
  specify(response = outcome, success = "yes") |>
  generate(reps = 2000, type = "bootstrap") |>
  calculate(stat = "prop")
```

- `specify()` 声明 response / explanatory 与 success level。
- `generate(type="bootstrap")` 从已观测样本有放回重抽。
- `calculate()` 必须与参数/估计量一致，例如 `mean`、`median`、`prop`。
- `get_confidence_interval()` 输入是 bootstrap estimates，不是原始 observations。
- `set.seed()` 使有限 simulation 可复现；它不改变统计定义。

### 2.2 三个数量不要混

| 数量 | 作用 | 增大后通常怎样 |
|---|---|---|
| 原样本量 $n$ | 决定原始信息量与 sampling variability | representative 条件下 CI 通常变窄 |
| bootstrap sample size | 标准 bootstrap 保持为 $n$ | 不能擅自改大来伪造更多信息 |
| repetitions $B$ | 近似 bootstrap distribution 的 simulation precision | quantiles 更稳定，但不能修复原样本 bias |

提高 confidence level 而其他条件不变，CI 更宽；降低 level，CI 更窄。提高 $n$ 通常提高 precision，但宽度还受 variation、statistic 与 design 影响。

### 2.3 Percentile method 的适用边界

Percentile bootstrap 用经验分布近似未知总体，并直接取 bootstrap quantiles。它简单直观，但在样本很小、estimate 有强 bias、分布极偏、参数在边界或 statistic 不平滑时，coverage 可能不好。课程本周要求掌握该方法，不代表它适用于所有问题。

Bootstrap 只重用样本已包含的信息。漏掉的 subgroup、selection bias 或 measurement bias 不会被重抽样修好。

## 3. 可视化 point estimate 与 CI

目的不是只画一根 error bar，而是同时让读者知道数据、estimate、uncertainty 各是什么。

```r
ggplot(sample_df, aes(x = group, y = measurement)) +
  geom_jitter(alpha = 0.25, width = 0.12) +
  stat_summary(fun = mean, geom = "point", size = 3) +
  geom_errorbar(
    data = result_df,
    aes(y = estimate, ymin = lower_ci, ymax = upper_ci),
    width = 0.1
  )
```

- 小样本可画 observations + point + CI；大样本 overplot 时可用 violin/density + point + CI。
- error bar 必须标明是 confidence interval、SD、SE 还是 percentile range。
- 只凭两个单组 CI overlap 与否不能替代正式 two-group test。CI 是否 overlap 与 difference CI 是否包含 0 不是同一规则。
- 图上显示总体真值只适用于教学 simulation；现实中参数未知，否则无需推断。

## 4. Hypothesis testing 在比较什么

Hypothesis test 用样本评估关于**总体参数**的两个互斥主张。

- **Null hypothesis $H_0$：**status quo / no effect / no difference 的具体参数主张。
- **Alternative hypothesis $H_A$：**研究问题对应的参数主张。

假设必须写总体参数，不写样本 statistic。例如比较两总体比例：

$$
H_0:p_A-p_B=0
\quad\text{vs}\quad
H_A:p_A-p_B\ne0.
$$

不能写 $H_0:\hat p_A=\hat p_B$；sample estimates 已经由观察数据确定，test 的对象是未知 population relation。

### 4.1 Test statistic

Test statistic 是样本与 $H_0$ 冲突程度的 numerical summary。例如

$$\hat\delta=\hat p_A-\hat p_B$$

或

$$\hat\delta=\bar x_A-\bar x_B.$$

`order = c("A", "B")` 决定计算 A − B 还是 B − A。方向写反会改变 observed statistic 的符号和 one-sided p-value，必须与 $H_A$ 一致。

## 5. Permutation randomization test

对“group 与 outcome 独立 / 两组总体分布在 null 下无差别”这类 null，permutation 的直觉是：若 $H_0$ 成立，group labels 与 outcomes 的原配对不含真实 association，因此重新打乱 labels 是 null 下合理的 reassignments。

### 5.1 六步框架

1. 用 population parameter 写 $H_0,H_A$，定义 sidedness。
2. 从原样本计算 observed test statistic $t_{obs}$。
3. 在 $H_0$ 下生成许多 permuted samples。
4. 每次算同一个 statistic，形成 null distribution。
5. 按 $H_A$ 的方向，计算与 $t_{obs}$ 一样或更 extreme 的比例。
6. 若 $p<\alpha$，reject $H_0$；否则 fail to reject $H_0$。

### 5.2 `infer` pipeline

```r
observed <- data |>
  specify(response = outcome, explanatory = group, success = "yes") |>
  calculate(stat = "diff in props", order = c("A", "B"))

set.seed(552)
null_dist <- data |>
  specify(response = outcome, explanatory = group, success = "yes") |>
  hypothesize(null = "independence") |>
  generate(reps = 2000, type = "permute") |>
  calculate(stat = "diff in props", order = c("A", "B"))

p_value <- null_dist |>
  get_p_value(obs_stat = observed, direction = "two-sided")
```

均值差要求 numeric response，并在 observed 与 null 两条 pipeline 的 `specify()` 中都**去掉**只适用于 categorical success level 的 `success`；两条 `calculate()` 都改为 `stat = "diff in means"`，并保持同一个 group `order`：

```r
observed_mean <- data |>
  specify(response = value, explanatory = group) |>
  calculate(stat = "diff in means", order = c("A", "B"))

null_mean <- data |>
  specify(response = value, explanatory = group) |>
  hypothesize(null = "independence") |>
  generate(reps = 2000, type = "permute") |>
  calculate(stat = "diff in means", order = c("A", "B"))
```

当前 infer 文档使用 `get_p_value()`；`get_pvalue()` 仍保留为 alias。

### 5.3 Permutation 保留与打破什么

- 保留 observations 的 outcome values 与总体 group sizes。
- 重新分配 labels，打破原有 group–outcome association。
- 是无放回的 label shuffle，不是 bootstrap 的有放回 resampling。
- 只有 exchangeability / randomization 逻辑与 study design 支持时，这个 null mechanism 才合理。

Permutation test 不自动把 observational association 变成 causal effect。因果解释需要 treatment assignment、interference、compliance 等设计条件。

### 5.4 为什么 randomization test 不只适用于 mean 与 proportion

Randomization test 的核心是构造一个与 $H_0$ 一致、且由 study design / exchangeability 支持的 label-reassignment mechanism。只要该 mechanism 合理，每次 permutation 后可以计算与问题匹配的其他 statistic，不必为每个 statistic 先推导新的 analytic reference distribution。

例如长尾 outcome 想比较两总体的典型位置，可把 test statistic 定义为 sample median difference。Null generation 仍然打乱 group labels，但每次改算

```r
calculate(stat = "diff in medians", order = c("A", "B"))
```

这种灵活性特别适合 analytic sampling distribution 难推导的 statistic；它不表示任意 shuffle 都有效。Median、variance 或其他 statistic 仍必须对应明确的 parameter/question，而且 permutation 必须尊重 paired、clustered、blocked 等原始设计结构。

## 6. $p$-value、$\alpha$ 与结论语言

$p$-value 是：**假设 $H_0$ 与 null model 成立时**，获得与 observed statistic 同样或更 extreme 结果的概率。Simulation 中用 tail proportion 近似。

它不是：

- $H_0$ 为真的概率；
- 结果“由随机造成”的概率；
- effect size；
- study quality；
- 未来复现概率。

$\alpha$ 是分析前选择的 significance threshold。规则：

- $p<\alpha$：reject $H_0$ in favour of $H_A$；
- $p\ge\alpha$：fail to reject $H_0$。

**Fail to reject 不等于 accept $H_0$ 或证明“没有差异”。**可能是 effect 很小，也可能是样本/设计没有足够信息。

### 6.1 One-sided 与 two-sided tails

- $H_A:\delta>0$：`direction="greater"`，看右尾。
- $H_A:\delta<0$：`direction="less"`，看左尾。
- $H_A:\delta\ne0$：two-sided，看两侧与 null 同样 extreme 的统计量。

Sidedness 必须由问题在看数据前决定，不能看到符号后改成 one-sided 来缩小 p-value。

## 7. CI 与 hypothesis test 的关系

二者都量化 sampling uncertainty：

- CI 给与数据相容的一段 parameter values；
- hypothesis test 评估某个 null value 是否与数据冲突。

对于同一 parameter、同一 assumptions、匹配的 two-sided level 与对应方法，若 $(1-\alpha)$ CI 不包含 null value，通常等价于在 $\alpha$ 水平 reject。若 95% difference CI 包含 0，则通常 fail to reject equality。

但这不是可对任何两条单组 CI 机械使用的规则：bootstrap percentile CI 与 permutation test 的 construction 不同，one-sided tests、multiple testing、离散 statistics 也会破坏简单一一对应。以正式 difference CI 或正式 test 为准。

## 8. Bootstrap 与 permutation 对比

| 维度 | Bootstrap | Permutation test |
|---|---|---|
| 目的 | 近似 estimator 的 sampling variability / CI | 模拟 $H_0$ 下 statistic 的 distribution |
| 操作 | 从 observed sample 有放回抽 $n$ 条 | 无放回打乱 labels/assignments |
| distribution 中心 | 通常围绕 observed estimate | 按 null value 构造，常围绕 0 |
| 关键输出 | CI endpoints、SE 等 | null distribution、p-value |
| 不能修复 | sample bias、coverage failure | confounding、错误 exchangeability |

看到 `generate()` 必须看 `type` 与上游 `hypothesize()`，不能把两个过程都称为“resampling 所以一样”。

## 9. 独立最小算例

设两组二元结果：A 为 `1,1,1,0`，B 为 `1,0,0,0`。

$$\hat p_A=0.75,\quad \hat p_B=0.25,\quad \hat\delta=0.50.$$

Permutation test 在固定 4 个 1、4 个 0 和两组各 4 人的条件下，枚举/随机抽取 label assignments，形成 null distribution。它不是重新生成新的 Bernoulli outcomes。

若对单一样本数值 `2,4,8,10` 估计 mean，bootstrap 每次从这四个值有放回取 4 个并算 mean；95% percentile CI 取 bootstrap means 的 2.5% 与 97.5% quantiles。增加 bootstrap repetitions 只使这两个 Monte Carlo quantiles 更稳定，不让原样本变成更多真实 observations。

## 10. 复习判断顺序

1. 目标 population 与 parameter 是什么？
2. estimate/statistic 与 parameter 对应吗？
3. sampling / assignment design 支持怎样的推广或因果解释？
4. CI 用的 procedure、level、$n$、$B$ 各是什么？
5. 假设里是否错误写了 sample statistic？
6. observed statistic 的 `order` 与 alternative direction 一致吗？
7. null distribution 是如何生成的；为什么该 shuffle 合理？
8. p-value tail 是否与 sidedness 一致？
9. 结论是否写成 reject / fail to reject，而不是“证明 null”？
10. statistical significance、effect magnitude 与 practical importance 是否分开？

## 来源、具体缺项与版本说明

### 当前课程主来源

- [当前 README](/Users/youralmight/workspaces/reps/mdscl/DSCI_552/official/current/DSCI_552_stat-inf-1_students/README.md)
- [Lecture 3：Confidence Intervals via Bootstrapping](/Users/youralmight/workspaces/reps/mdscl/DSCI_552/official/current/DSCI_552_stat-inf-1_students/docs/_sources/lecture-notes/03_lecture-confidence-intervals.ipynb)
- [Lecture 4：Hypothesis Testing via Permutation](/Users/youralmight/workspaces/reps/mdscl/DSCI_552/official/current/DSCI_552_stat-inf-1_students/docs/_sources/lecture-notes/04_lecture-hyp-test-intro.ipynb)
- [Lecture 3 slides](/Users/youralmight/workspaces/reps/mdscl/DSCI_552/official/current/DSCI_552_stat-inf-1_students/docs/slides/lec03/lec03.html)
- [Lecture 4 slides](/Users/youralmight/workspaces/reps/mdscl/DSCI_552/official/current/DSCI_552_stat-inf-1_students/docs/slides/lec04/lec04.html)
- [Lab 2 题面，仅用于应用范围](/Users/youralmight/workspaces/reps/mdscl/DSCI_552/assignments/lab2/DSCI_552_lab2_yz2000/lab2.Rmd)

### 指定辅助阅读

- ModernDive Ch8 §§8.3–8.7.1：bootstrap CI。
- ModernDive Ch9 §§9–9.5（omit 9.4.2）：simulation-based hypothesis testing。
- README 指定 permutation interactive visualization；本文不依赖其动画画面。

### 缺项与讲义细节

- Canvas 上的推荐视频清单与登录后材料未读取，不推断内容。
- Lecture 3 的“这一次 100 intervals 正好 95 条覆盖”只是一次 simulation outcome，不是每批必然恰好 95 条。
- Lecture 4 用 CI non-overlap 作为探索线索，并明确要求正式 test；本文保留该边界。
- `infer` API 可能随版本使用 `get_p_value` / `get_pvalue` 命名差异；笔记采用当前文档常见接口并要求以实际安装版本核对。
- 本文未执行或填写 Lab 2 的原题 pipeline、数值答案、hypotheses 或文字结论。