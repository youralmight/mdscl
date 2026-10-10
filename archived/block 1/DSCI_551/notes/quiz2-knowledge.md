# DSCI 551 Quiz 2 知识文档

> 本文覆盖当前 checkout 中已发布的 Lecture 5–8 与 Lab 4（Maximum Likelihood Estimation and Monte Carlo Simulation）材料。Lecture 7–8 和 Lab 4 已纳入 Quiz 2 的最终复习范围；正式考试的日期、题数、允许资源等行政信息仍以课程发布的 assessment-specific instructions 和 ORCA 规则为准。

## 范围证据、边界与学习路线

### 已确认的最终材料边界

- `official/current/DSCI_551_stat-prob-dsci_students/website/learning-goals.qmd` 列出 Lecture 5 Continuous Distributions、Lecture 6 Common Distribution Families and Conditioning、Lecture 7 Maximum Likelihood Estimation，以及 Lecture 8 Simulation 的 learning goals。
- 当前课程 README 将 Lecture 7–8 与最终 Lab 4 对应；Lab 4 明确练习 MLE、one-step Monte Carlo、multi-step/conditional simulation。
- 本文保留 Lecture 5–6 的连续分布、常见分布族、二元 PDF、条件密度和变换，并补入 Lecture 7–8 与 Lab 4 的随机样本/iid、MLE、随机数生成、经验量、LLN 和多步骤模拟。

### 范围内的边界与提醒

- Lecture 7 的重点是单参数（univariate）MLE 的概念、likelihood/log-likelihood、经验网格搜索和 Exponential 参数的解析推导；多参数模型、回归/GLM 等只作为背景，不是本稿的解题主线。
- Lecture 8 与 Lab 4 的重点是用 R/Python 生成离散随机样本、设置 seed/random state、用经验量近似理论量，以及处理有依赖步骤的模拟。课程明确不要求在 DSCI 551 自己设计图形；Lab 4 中的绘图代码是提供后运行。
- Exponential 的 rate 参数化与 mean 参数化必须区分：本稿用 β 表示 mean、λ=1/β 表示 rate；R 的 `rexp`/`dexp` 使用 `rate`。
- 日期、题数、计分、允许个人 cheat sheet、计算器、RStudio/网络/文件等考试行政规则不由本知识文档推断；以之后发布的 assessment-specific instructions 为准。

### 总路线

1. 先判断随机变量是离散还是连续，以及支持集；连续模型的单点概率为 0，区间概率由面积给出。
2. 若给 PDF，先检查非负和总面积 1，再用积分算概率、均值和方差。
3. 若给 CDF、survival 或 quantile function，先确认它是哪一种表示，再做差、取补集或反解。
4. 选择分布族必须依据过程假设，不要只凭“正值/右偏/等待时间”下结论。
5. 二元连续题把概率看成密度曲面下的体积；边缘概率是对另一个变量积分，独立时联合 PDF 才能相乘。
6. 连续条件分布用密度重新归一化；给定单点时用联合密度除以边缘密度，而不是把单点概率代入离散公式。
7. MLE 题先明确观测数据、参数和分布假设，再由 iid 构造联合 likelihood；可用 log-likelihood 做网格搜索或解析最大化。
8. Simulation 题先写“一次实验”的随机步骤，再重复许多次，用经验均值/方差/比例/分位数总结，并检查 seed、独立性和每一步的条件依赖。

### Lecture 5–6 与 Lab 3 的原有重点

以上第 1–6 步和下文第 1–5 节覆盖 Lecture 5–6 及 Lab 3 的原有重点；最终新增的 Lecture 7–8 与 Lab 4 内容见第 6–7 节。

---

## 1. 离散与连续随机变量

### 1.1 怎样区分

- **离散**：支持集有限或可数无限，单个值可以有正概率，使用 PMF `P(X = x)`，期望按求和计算。
- **连续**：支持集不可数（实际测量常是离散精度，但若相邻差异不重要可近似连续），使用 PDF `f_X(x)`，概率由区间面积计算。
- “有无穷多个结果”本身不足以判定连续：Poisson/Geometric 可数无限，仍是离散。
- 连续随机变量的 `f_X(x)` 是密度，不是 `P(X = x)`；对每个单点 `P(X = x) = 0`。所以连续模型中 `<` 与 `≤`、`>` 与 `≥` 的概率相同。

### 1.2 PDF 的合法性与单位

PDF 必须满足：

1. `f_X(x) ≥ 0`；
2. 全部支持上的面积为 1：`∫ f_X(x) dx = 1`；
3. 支持外通常定义为 0。

若 `f_X(x)` 在某处大于 1，并不表示非法；密度是“每单位 x 的概率”，只有面积必须是概率。若 `X` 用米，PDF 单位是 `1/m`，与 `dx` 相乘后得到无单位的概率。

区间概率：

`P(a ≤ X ≤ b) = ∫ₐᵇ f_X(x) dx`。

最小例子：若 `f_X(x) = 2x`（`0 ≤ x ≤ 1`，其他处为 0），则 `P(X < 0.5) = ∫₀⁰·⁵ 2x dx = 0.25`，而 `P(X = 0.5) = 0`。

### 1.3 连续变量的摘要

把离散求和换成对 PDF 的积分：

- `E[X] = ∫ x f_X(x) dx`；
- `E[g(X)] = ∫ g(x) f_X(x) dx`；
- `Var(X) = E[(X − μ)²] = ∫ (x − μ)² f_X(x) dx = E[X²] − E[X]²`；
- `SD(X) = √Var(X)`；
- `Mode(X) = arg maxₓ f_X(x)`（PDF 最高处）；
- 连续熵可写为 `H(X) = −∫ f_X(x) log f_X(x) dx`，但 Lecture 5 明确提醒连续熵可能为负，且后续统计内容不常使用。

### 1.4 中位数、分位数与预测区间

- 中位数 `M` 满足 `P(X ≤ M) = 0.5`。
- p-分位数 `Q(p)` 满足 `P(X ≤ Q(p)) = p`；中位数就是 `Q(0.5)`。
- 中央 p×100% 预测区间：下界为 `Q((1−p)/2)`，上界为 `Q((1+p)/2)`；两侧各有 `(1−p)/2` 的概率。
- `0.25, 0.5, 0.75` 分位数分别是四分位数；特殊命名在 Lecture 5 标为 optional，计算定义仍可用。
- 偏度衡量尾部方向：对称为 0；右尾长为正偏，通常 `Mode < Median < Mean`；左尾长为负偏，通常 `Mean < Median < Mode`。

---

## 2. CDF、survival 与 quantile function

### 2.1 三种表示

- CDF：`F_X(x) = P(X ≤ x) = ∫₋∞ˣ f_X(t) dt`。
- PDF 是 CDF 的导数（可导处）；CDF 是 PDF 的累积积分。
- Survival function：`S_X(x) = P(X > x) = 1 − F_X(x)`。
- Quantile function：`Q(p) = F⁻¹(p)`，输入域为 `0 ≤ p ≤ 1`，把概率映射到对应分位点。
- 这些表示携带同一分布的信息；Lecture 6 另外提醒本课程不覆盖 multivariate quantile function。

### 2.2 合法性检查

CDF 必须：

- 单调不减；
- 始终在 `[0, 1]` 内；
- `x → −∞` 时趋于 0；
- `x → +∞` 时趋于 1。

连续变量的区间概率既可用 PDF 积分，也可用 CDF 相减：

`P(a ≤ X ≤ b) = F_X(b) − F_X(a)`。

由 survival 求尾部：`P(X > a) = S_X(a)`；由 quantile 求值时，先确定要求的是概率 p 还是返回 p 的分位点，不能把 `p` 与 `q` 混用。

---

## 3. 常见连续分布族

选择族时先读过程、支持和参数含义。正值、右偏、等待时间或 lifetime 单独都不能唯一决定 Exponential/Gamma/Weibull/Log-Normal。

| 家族与过程 | 支持、PDF 与参数 | 均值、方差 | R 函数与识别陷阱 |
|---|---|---|---|
| Uniform(a,b)：`[a,b]` 内等密度 | `f(x)=1/(b−a)`，`a≤x≤b` | `(a+b)/2`；`(b−a)²/12` | `dunif/punif/qunif/runif`；端点是 `min/max` |
| Normal(μ,σ²)：钟形对称 | `f(x)=1/√(2πσ²) · exp(−(x−μ)²/(2σ²))`，全实数 | `μ`；`σ²` | `dnorm/pnorm/qnorm/rnorm`；R 的 `sd` 要填 `σ`，不是方差 `σ²` |
| Log-Normal(μ,σ²)：`log(X)` 正态 | `x≥0`；`f(x)=1/(x√(2πσ²)) · exp(−(log x−μ)²/(2σ²))` | `exp(μ+σ²/2)`；`exp(2(μ+σ²))−exp(2μ+σ²)` | `dlnorm/plnorm/qlnorm/rlnorm`；μ、σ²是 `log(X)` 的参数，不是 X 的均值/方差 |
| Exponential(β) 或 Exponential(λ)：一次等待到下一事件 | `f(x)=β⁻¹ exp(−x/β)` 或 `λ exp(−λx)`，`x≥0`；`λ=1/β` | β 或 `1/λ`；β² 或 `1/λ²` | `dexp/pexp/qexp/rexp`；R 用 `rate = λ`，不是 mean β |
| Beta(α,β)：比例/概率 | `0≤x≤1`；`f(x)=Γ(α+β)/(Γ(α)Γ(β)) · x^(α−1)(1−x)^(β−1)` | `α/(α+β)`；`αβ/[(α+β)²(α+β+1)]` | `dbeta/pbeta/qbeta/rbeta`；α、β>0，Uniform 是特殊情形 |
| Weibull(λ,k)：时间到事件，形状随时间变化 | `x≥0`；`f(x)=k/λ · (x/λ)^(k−1) exp(−(x/λ)^k)` | `λ Γ(1+1/k)`；`λ²[Γ(1+2/k)−Γ²(1+1/k)]` | `dweibull/pweibull/qweibull/rweibull`；λ是 scale，k 是 shape；k=1 为 Exponential |
| Gamma(k,θ)：非负，尤其是多个等待时间总和 | `x≥0`；`f(x)=x^(k−1)exp(−x/θ)/(Γ(k)θ^k)` | `kθ`；`kθ²` | `dgamma/pgamma/qgamma/rgamma`；k 是 shape，θ 是 scale；k=1 为 Exponential |

### 3.1 由过程选择家族

- 一次稳定速率下、到**下一次**事件的等待，或 memoryless：Exponential。
- 多个独立同均值 Exponential 等待之和，或累计到第 `k>1` 次事件：Gamma；Exponential 是 `k=1` 的特殊情况。
- 时间到事件且风险随已等待时间上升/下降，由 shape 参数控制：Weibull；`k>1` 表示随时间更容易发生，`0<k<1` 表示随时间更不容易发生。
- `log(X)` 近似 Normal：Log-Normal；只说正值和右偏不够。
- `(0,1)` 上的比例、两个 shape 参数、形状可对称或不对称：Beta。
- 固定区间内每个等长区间等可能：Uniform。
- 连续、对称、bell-shaped 的测量误差/身高：Normal。
- 仅知“正值、右偏、等待时间、lifetime”：`Not enough information`，因为多个家族都可能。

### 3.2 R 的 d/p/q/r 前缀

对同一分布族：

- `d*`：density（连续时是 PDF 高度，不是点概率）；
- `p*`：CDF，输入 `q`，默认 `lower.tail = TRUE`；
- `q*`：quantile，输入概率 `p`；
- `r*`：random generator，输入样本量 `n`。

常见模板：

```r
dnorm(x = 3, mean = 2, sd = 2)       # σ² = 4，所以 sd = 2
punif(q = c(0.25, 0.5), min = 0, max = 2)
qexp(p = 0.75, rate = 1 / beta)       # rate 是均值等待时间的倒数
rnorm(n = 10, mean = 0, sd = 5)
```

先问“要密度、累计概率、分位点还是随机样本”，再选 `d/p/q/r`。不要把 PDF 高度当概率，也不要把 Normal 方差直接传给 `sd`。

---

## 4. 二元连续分布

### 4.1 联合 PDF 与事件概率

`f_{X,Y}(x,y)` 是密度曲面，不是单点概率。合法联合 PDF 要满足：

- `f_{X,Y}(x,y) ≥ 0`；
- 全部支持上双重积分为 1：`∫∫ f_{X,Y}(x,y) dx dy = 1`；
- 支持外为 0。

二维事件的概率是该事件区域下的体积。例如，两个独立且均匀分布在 `[5,5.5]` 的完赛时间，联合支持是边长 0.5 的正方形，联合密度为 `1/0.5 × 1/0.5 = 4`。`X<Y` 是正方形的一半，概率为 1/2；`X≤5.2` 是覆盖全部 y 范围的竖条，概率为该区域面积 `0.2×0.5` 乘密度 4，即 0.4。

边缘 PDF：

- `f_X(x) = ∫ f_{X,Y}(x,y) dy`；
- `f_Y(y) = ∫ f_{X,Y}(x,y) dx`。

若 X、Y 独立：`f_{X,Y}(x,y) = f_X(x) f_Y(y)`；只有独立成立时才能直接相乘。连续单点事件仍是零概率，题目应转成区域/积分。

### 4.2 连续条件密度

若条件是正概率事件 `B`，用原 PDF 限制到 B 后归一化：

`f_{X|B}(x) = f_X(x) / P(B)`（x 在 B 内），否则为 0。

例如 `X≥2500`：保留 `x≥2500` 的 PDF，除以 `P(X≥2500)`，检查新面积为 1。

给定连续变量单点 `X=x` 时，`P(X=x)=0`，不能使用离散的点概率比值；改用密度：

`f_{Y|X}(y|x) = f_{Y,X}(y,x) / f_X(x)`（要求 `f_X(x)>0`）。

若 X、Y 独立，则 `f_{Y|X}(y|x)=f_Y(y)`：知道 X 不改变 Y 的分布。

---

## 5. 连续变量变换与 Lab 3 的做题流程

### 5.1 连续变换的安全流程

Lab 3 的 challenging Exercise 7 用 `Y=X²` 与 `X~Exponential(λ=1)` 强调：连续变换不能只把原 PDF 的表达式替换变量，因为区间长度会被拉伸/压缩。

推荐先求 CDF：

1. 找 Y 的支持；这里 `Y≥0`。
2. 把事件 `Y≤y` 改写成关于 X 的事件；因为 `X≥0`，`X²≤y` 等价于 `X≤√y`（`y≥0`）。
3. 得 `F_Y(y)=F_X(√y)=1−exp(−√y)`（`y≥0`），支持外为 0。
4. 对 CDF 求导得 `f_Y(y)=exp(−√y)/(2√y)`（`y>0`），支持外为 0；端点按密度的适当极限/定义处理，概率计算仍由积分决定。

常见错法：把 `exp(−y²)` 或 `exp(−√y)` 当成变换后的 PDF；后者只是 CDF，遗漏了导数的尺度因子。

### 5.2 逐题检查清单

- 先写支持集和事件，再算数值；单位换算（如 60–90 秒 = 1–1.5 分钟）。
- 点概率：离散看 PMF，连续直接为 0；连续区间看 PDF 面积。
- 变换：先把事件拉回原变量，再整合原模型；或先 CDF 再求导。
- CDF 检验四条性质后再读中位数（CDF=0.5 的 x）。
- 分布族：读过程假设、support、shape/scale 的定义；参数符号本身不是证据。
- 独立二元题：先写联合支持和 `f_{X,Y}=f_Xf_Y`，再画/识别事件区域并积分。
- 条件密度：限制支持、除以条件事件概率/边缘密度、检查归一化。

---

## 6. Lecture 7：随机样本与最大似然估计（MLE）

### 6.1 Random sample 与 iid

- 随机样本是来自目标 population/system 的随机结果集合；大小为 `n` 时写作 `X₁,…,Xₙ`。观测到的具体数据写作小写 `y₁,…,yₙ`。
- 默认的 random sample 假设为 **iid（independent and identically distributed）**：任意观测之间相互独立，且每个观测来自同一个分布（同一参数）。
- iid 是建模假设，不是现实中自动成立的事实。共享城市、时间段、个体或其他相关来源可能破坏 independence；不同来源/不同参数可能破坏 identical distribution。
- MLE 的方向是：给定观测数据和选定的 parametric family，找使这些数据最可能出现的参数值。参数是未知的，观测值在 likelihood 中固定。

### 6.2 从单个 PDF/PMF 到 likelihood

1. 先根据数据类型、支持集和生成过程选择模型，例如非负等待时间可考虑 Exponential，但“正值/右偏”单独不足以决定分布族。
2. 写一个观测的 PDF 或 PMF，例如 Exponential(mean 参数 β)：
   `f(y_i | β) = (1/β) exp(-y_i/β)`，其中 `β > 0`。
3. iid 带来联合 PDF/PMF 的乘积：
   `f(y₁,…,yₙ | β) = ∏ᵢ f(yᵢ | β)`。
4. 把同一个数学表达式换成“参数的函数、数据已观察”的视角：
   `L(β | y₁,…,yₙ) = ∏ᵢ f(yᵢ | β)`。
   因此 likelihood 在数值上等于观测样本的 joint PDF/PMF，但它不是关于 β 的概率分布；不要把 likelihood 的高度当成 `P(β)`。

### 6.3 Log-likelihood 与两条 MLE 路径

- likelihood 是许多小的概率/密度值的乘积，样本大时可能下溢；取自然对数把乘积变成和，也让求导更容易：
  `ℓ(θ) = log L(θ | y) = Σᵢ log f(yᵢ | θ)`。
- `log` 是严格递增变换，所以使 `L` 最大的参数也使 `ℓ` 最大；log-likelihood 的值可能是负数，比较时“较大”（较不负）才是较好。
- **经验（empirical/grid）MLE**：选定合法参数网格；对每个候选值计算 likelihood 或直接计算 log-likelihood；用 `which.max()`/`argmax` 取最大者。网格步长越小，网格估计通常越精细，但它仍是近似，不等于解析解。
- **解析 MLE**：对 log-likelihood 对参数求一阶导数，令其等于 0 并解出候选值；再用参数支持、边界和二阶导数检查它是否为 maximum。Lab 4 中 Bernoulli 的 analytical derivation 标为 optional，但“模型 → likelihood → log-likelihood → 最大化”的逻辑是核心。

### 6.4 Exponential(mean β) 的完整例子

假设 `Y₁,…,Yₙ iid ~ Exponential(β)`，且 `β` 是平均等待时间（不是 rate）。由 iid：

`L(β | y) = ∏ᵢ [β⁻¹ exp(-yᵢ/β)] = β⁻ⁿ exp[-(Σᵢ yᵢ)/β]`。

所以

`ℓ(β) = -n log(β) - (Σᵢ yᵢ)/β`；

`ℓ′(β) = -n/β + (Σᵢ yᵢ)/β²`。

令一阶导数为 0：

`β̂ = (Σᵢ yᵢ)/n = ȳ`。

这表示 Exponential(mean 参数) 的 MLE 是 observed sample mean。注意样本平均是估计量时可写 `β̂ = X̄`，代入具体 observed data 时写 `mean(y)`。

二阶导数为

`ℓ″(β) = n/β² - 2(Σᵢ yᵢ)/β³`。

在 `β̂ = Σyᵢ/n` 处，`ℓ″(β̂) = -n³/(Σyᵢ)² < 0`（只要样本和为正），所以该驻点是局部 maximum。还要检查 `β > 0` 的支持。

R 中 Exponential 使用 `rate = λ = 1/β`：

```r
y <- c(0.8, 2.1, 2.4)
beta_hat <- mean(y)                         # analytical MLE
log_lik <- function(beta) sum(dexp(y, rate = 1 / beta, log = TRUE))
grid <- seq(0.1, 10, by = 0.01)
empirical_beta <- grid[which.max(sapply(grid, log_lik))]
```

经验网格结果可能和 `mean(y)` 略有不同，因为候选网格通常不恰好包含解析解。计算大样本 likelihood 时优先使用 `sum(..., log = TRUE)`，避免先乘很多很小的数。

### 6.5 Lab 4 的 Bernoulli MLE 连接

若 `Yᵢ iid ~ Bernoulli(p)`，观测为 0/1，令 `s = Σᵢ yᵢ`，则

`L(p | y) = ∏ᵢ pʸⁱ (1-p)^(1-yᵢ)`；

`ℓ(p) = s log(p) + (n-s) log(1-p)`，且 `0 ≤ p ≤ 1`。网格上对 `p` 计算 log-likelihood 并取最大值；解析结果为 `p̂ = s/n`（样本中 1 的比例）。这是 Lab 4 中“observed Bernoulli data → estimate p → simulate future rush”的桥梁。

Lab 4 的 Exercise 3 也用 Poisson 模型练习“先选模型、再写 likelihood、最后做网格 MLE”：若 `Yᵢ iid ~ Poisson(λ)`，则

`ℓ(λ) = -nλ + (Σᵢ yᵢ) log(λ) - Σᵢ log(yᵢ!)`，`λ > 0`。实际练习可在例如 `0.3, 0.4, …, 5.0` 的候选网格上直接比较 log-likelihood；解析结果（Lab 4 标作 optional derivation）为 `λ̂ = mean(y)`。不要混淆 likelihood 最高的候选参数与该参数的概率。

---

## 7. Lecture 8 与 Lab 4：Simulation / Monte Carlo

### 7.1 Pseudorandom、seed 与可复现性

- 计算机通常生成的是 deterministic pseudorandom sequence，而不是真正不可预测的随机数。seed（或 random state）是决定该序列的初始状态。
- 每次在**同一语言、同一 RNG 设置**下使用同一 seed，代码会产生相同样本，便于复现、调试和检查答案；R 与 Python 即使 seed 数值相同，也不保证产生相同序列。
- seed 只能保证生成过程可重现，不会自动保证 iid。人为递推的序列可能相邻相关；要检查模拟步骤是否真的符合模型假设。

R 生成有限类别离散样本：

```r
set.seed(551)
outcomes <- c("banana", "coin", "shell")
probs <- c(0.12, 0.75, 0.13)
sample(outcomes, size = 10, replace = TRUE, prob = probs)
rbinom(n = 10, size = 5, prob = 0.6)  # 10 个 Binomial 观测
rpois(n = 20, lambda = 10)
```

Python 生成有限类别或分布样本：

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(551)  # random state
rng.choice(["banana", "coin", "shell"], size=10,
           replace=True, p=[0.12, 0.75, 0.13])
stats.binom.rvs(n=5, p=0.6, size=10, random_state=rng)
stats.poisson.rvs(mu=10, size=20, random_state=rng)
```

注意 `rbinom(n = 10, size = 5, ...)` 中第一个 `n` 是要生成的观测个数，`size` 是每个 Binomial 变量的 trial 数；Python `size=10` 通常是生成的观测个数。R `sample()` 会自动重新缩放不加和为 1 的 `prob`，而 `numpy.choice` 要求概率和为 1。

### 7.2 Theoretical quantity 与 empirical quantity

- **Theoretical/distribution-based** quantity 使用已知的分布和参数，例如 `E(X)`、`Var(X)`、`P(X=x)`；它是模型下的真值。
- **Empirical/data-based** quantity 使用一个随机样本，例如 `mean(x)`、`var(x)`、`mean(x == 0)`、`quantile(x, 0.95)`；它是对真值的近似，会随样本改变。
- R 的 `var()` 是分母为 `n−1` 的 sample variance；不要在它和理论 variance 之间无提示地混用。`sd()` 是 `sqrt(var())`。
- 对事件概率，逻辑值的平均数就是经验比例：`mean(x == 0)` 估计 `P(X=0)`。经验 PMF 可用各类别频率（`table(x) / length(x)`）。
- Simulation 的基本流程：定义一次随机实验 → 重复很多次得到 simulated sample → 用经验量总结 → 与理论值（若可得）比较并解释误差。

### 7.3 Law of Large Numbers（LLN）

若重复产生来自同一分布的 iid 样本，样本平均 `X̄ₙ = (1/n)Σᵢ Xᵢ` 随 `n` 增加趋近理论均值 `E(X)`。因此更大的 simulation replication 数通常使经验 mean、variance、probability 更稳定、更接近理论量，但有限样本不会保证恰好相等。

LLN 解释了 Monte Carlo：每次模拟都带有随机误差，增加独立重复次数通常减小近似误差；一组重复实验的 Monte Carlo estimate 本身也仍是随机的。模拟只能逼近它所指定的概率模型，不能自动修正错误的分布或依赖假设。

### 7.4 Multi-step / conditional simulation

当目标变量由多个随机变量组合而成，按生成机制分阶段模拟：

1. 明确一次 replicate 的目标和所有随机输入。
2. 先生成第一阶段（如每位客人是否出席的 Bernoulli）。
3. 根据第一阶段结果生成第二阶段；只有满足条件的对象才生成其条件结果（如出席者的 Poisson cupcake count）。
4. 汇总一次 replicate 的总量，再重复很多次；最后对 totals 计算 mean、variance、概率或 quantile。

例如，客人出席概率为 `p_attend`，且“在出席条件下”消费 `Poisson(mean = cupcakes)`。不能把 `cupcakes` 直接当无条件消费量，也不能对缺席者照样加入第二阶段随机消费。若第一阶段决定第二阶段参数，必须在每个 replicate 内更新；有新信息时只修改受影响的阶段并保持其他独立步骤。

Lab 4 同时练习 one-step Monte Carlo（例如重复模拟两次投篮并估计 miss-both 概率）和 multi-step/conditional simulation（party attendance/cupcake demand）。绘图不是 DSCI 551 的学习目标；复习重点是随机机制、重复、经验总结和与理论结果的比较。

### 7.5 Simulation 查错清单

- 先区分“样本大小/replication 数”和分布自身的参数（特别是 Binomial 的 trial 数）。
- 先设置 seed，再运行需要复现的完整随机流程；不要在每次循环内部重复重置 seed，否则每次 replicate 可能完全相同。
- 检查每一步是否使用正确的分布、参数化和支持；Exponential 的 R 函数传 `rate`。
- 理论量和经验量使用同一对象：`mean` 对 `mean`、`var` 对 `var`，并注明 variance 的分母约定。
- 结果不必与理论值完全相同；小的 Monte Carlo 样本波动正常，增加独立 replication 后通常更接近。

---

## 来源清单

本文只引用当前课程的最终发布材料：

- `official/current/DSCI_551_stat-prob-dsci_students/website/learning-goals.qmd`：Lecture 5–8 的 learning goals。
- `official/current/DSCI_551_stat-prob-dsci_students/notes/05_lecture-continuous.qmd`：连续/离散区分、PDF、连续摘要、median/quantile/prediction interval、skewness、CDF、survival、quantile function 及合法性。
- `official/current/DSCI_551_stat-prob-dsci_students/notes/06_lecture-continuous-families.qmd`：Uniform、Normal、Log-Normal、Exponential、Beta、Weibull、Gamma；R 的 d/p/q/r；二元 PDF、区域概率和连续条件密度。
- `official/current/DSCI_551_stat-prob-dsci_students/notes/07_lecture-maximum-likelihood-estimation.qmd`：random sample/iid、likelihood、log-likelihood、经验与解析 MLE、Exponential mean 参数 β 的估计和二阶导数检查。
- `official/current/DSCI_551_stat-prob-dsci_students/notes/08_lecture-simulation.qmd`：seed、R/Python 随机样本生成、经验与理论量、LLN 和 multi-step simulation。
- `official/current/DSCI_551_stat-prob-dsci_students/release/lab3/student/lab3.Rmd`：Lecture 5–6 的模型识别、二元密度、CDF、PDF/分位数/预测区间、条件密度和变换练习。
- `official/current/DSCI_551_stat-prob-dsci_students/release/lab4/student/lab4.Rmd`：Bernoulli/Poisson MLE、one-step Monte Carlo、重复实验、multi-step/conditional simulation；其中分析推导与绘图 construction 的标注边界按 Lab 4 原文保留。
- `official/current/DSCI_551_stat-prob-dsci_students/README.md`：当前课程的 lecture/lab 对应关系。
