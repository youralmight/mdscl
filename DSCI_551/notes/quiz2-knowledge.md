# DSCI 551 Quiz 2 知识文档

> 本文只使用当前课程已发布的本地材料。Quiz 2 的正式范围、日期、题数和允许资源在当前 checkout 中没有被明确发布；因此凡涉及正式考试范围均标为 `[未确认]`。在没有新的 assessment-specific instruction 前，本文以 Lecture 5–6 与已发布 Lab 3 的共同覆盖作为可审计的复习边界。

## 范围证据、边界与学习路线

### 已确认的材料边界

- `official/current/.../website/learning-goals.qmd` 明确列出 Lecture 5 **Continuous Distributions** 与 Lecture 6 **Common Distribution Families and Conditioning** 的 learning goals。
- 当前课程 `README.md` 把 Lab 3 明确标为 **Continuous Distribution Families (Lectures 5 and 6)**；Lab 3 学生版已发布，覆盖连续/离散比较、PDF、CDF、分位数、预测区间、连续分布族、二元密度、条件密度和连续变量变换。
- `notes/resources.md` 说明当前学生版没有 worksheet；`notes/messages.md` 只有课程开场通知，没有 Quiz 2 范围通知。
- 因而本稿的**工作覆盖**是 Lecture 5、Lecture 6 和 Lab 3 中的相关练习；Lecture 7–8（MLE 与 simulation）虽已在仓库中发布，但没有当前 Quiz 2 范围证据，暂不纳入核心复习。

### [未确认]

- Quiz 2 是否恰好覆盖 Lecture 5–6、是否包含 Lecture 7–8、是否包含 Lab 3 的 challenging exercises：当前本地材料没有明示，不能猜测。
- 题数、题型、日期/时间窗、ORCA reservation、计分方式、是否允许个人 cheat sheet、计算器、RStudio/网络/文件等：当前材料没有 Quiz 2-specific 说明。
- 课程 README 只要求 Quiz 1/2 各占 25%，并让学生参考 MDS calendar；它不是 Quiz 2 的详细范围公告。
- 因此做题时以之后发布的 assessment-specific instructions 和 ORCA 规则为准；本知识文档不是对考试许可的推断。

### 总路线

1. 先判断随机变量是离散还是连续，以及支持集；连续模型的单点概率为 0，区间概率由面积给出。
2. 若给 PDF，先检查非负和总面积 1，再用积分算概率、均值和方差。
3. 若给 CDF、survival 或 quantile function，先确认它是哪一种表示，再做差、取补集或反解。
4. 选择分布族必须依据过程假设，不要只凭“正值/右偏/等待时间”下结论。
5. 二元连续题把概率看成密度曲面下的体积；边缘概率是对另一个变量积分，独立时联合 PDF 才能相乘。
6. 连续条件分布用密度重新归一化；给定单点时用联合密度除以边缘密度，而不是把单点概率代入离散公式。

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

## 来源清单与未确认事项

### 当前本地来源

- `official/current/DSCI_551_stat-prob-dsci_students/website/learning-goals.qmd`：Lecture 5–6 learning goals；同时列出后续 Lecture 7–8，说明其主题但没有 Quiz 2 范围标记。
- `official/current/DSCI_551_stat-prob-dsci_students/notes/05_lecture-continuous.qmd`：连续/离散区分、PDF、连续摘要、median/quantile/prediction interval、skewness、CDF、survival、quantile function 及合法性。
- `official/current/DSCI_551_stat-prob-dsci_students/notes/06_lecture-continuous-families.qmd`：Uniform、Normal、Log-Normal、Exponential、Beta、Weibull、Gamma；R 的 d/p/q/r；二元 PDF、区域概率和连续条件密度。
- `official/current/DSCI_551_stat-prob-dsci_students/release/lab3/student/lab3.Rmd`：已发布 Lab 3 的练习边界、模型识别决策、二元密度、CDF 检查、PDF/分位数/预测区间、条件密度和变换。
- `official/current/DSCI_551_stat-prob-dsci_students/README.md`：当前课程 lecture/lab map、Lab 3 对应 Lectures 5–6、Quiz 1/2 权重和 Quiz 仅指向 MDS calendar。
- `notes/resources.md`：当前学生版无 worksheet；Lab 3 主题与 Lecture 5–6 对应。
- `notes/messages.md`：当前课程开场通知；未提供 Quiz 2 范围。

### 明确排除

- 未使用 `official/public/` 历史材料替代当前材料。
- 未把 Lecture 7–8 的 MLE/simulation 当作 Quiz 2 核心，因为没有本地 scope evidence。
- 未把 optional 内容（例如 Lecture 5 的其他分布表示、特殊分位数命名）升级成正式必考范围；相关定义若服务于已发布 Lab 3 或 Lecture 5 learning goals，才在文中保留。
- 未复制课程平台、诚信或 ORCA 操作细节到考试稿；这些应以 assessment-specific instructions 为准。
