# DSCI 551 Quiz 2

## Continuous basics

- 离散：PMF，单点可有正概率，期望用 Σ。连续：PDF，单点 P(X = x) = 0，区间概率用面积/积分。
- PDF 合法：f(x) ≥ 0；∫ f(x)dx = 1；支持外 f = 0。密度可 > 1；只有面积必须是概率。
- P(a ≤ X ≤ b) = ∫ₐᵇ f(x)dx = F(b) − F(a)。连续中 < 与 ≤、> 与 ≥ 概率相同。
- E[X] = ∫ x f(x)dx；E[g(X)] = ∫ g(x)f(x)dx。
- Var(X) = E[(X − μ)²] = E[X²] − E[X]²；SD = √Var。
- Mode = PDF 最高的 x；median M：P(X ≤ M) = 0.5；p-quantile Q(p)：P(X ≤ Q(p)) = p。
- 中央 p 预测区间：[Q((1−p)/2), Q((1+p)/2)]；两侧各 (1−p)/2。
- 右偏：右尾长，通常 Mode < Median < Mean；左偏：Mean < Median < Mode。

## PDF / CDF / survival / quantile

- PDF：f_X(x)，概率是曲线下的面积；CDF：F_X(x) = P(X ≤ x) = ∫₋∞ˣ f_X(t)dt。
- Survival：S_X(x) = P(X > x) = 1 − F_X(x)。Quantile：Q(p) = F⁻¹(p)，输入 0 ≤ p ≤ 1。
- 合法 CDF：单调不减；值在 [0,1]；x→−∞ 时到 0；x→∞ 时到 1。
- 由 PDF 算区间、由 CDF 做差、由 survival 取尾部、由 quantile 反解概率。先辨认题目要 f、F、S 还是 Q。
- 例：f(x)=2x（0≤x≤1）：P(X<0.5)=0.25，P(X=0.5)=0；中位数 √0.5。

## Continuous families

| Family / cue | Support / key formulas | Mean；variance | R |
|---|---|---|---|
| Uniform(a,b)：区间内等密度 | f=1/(b−a)，a≤x≤b | (a+b)/2；(b−a)²/12 | `dunif`, `punif`, `qunif`, `runif` |
| Normal(μ,σ²)：对称 bell | 全实数；f=1/√(2πσ²) · exp(−(x−μ)²/(2σ²)) | μ；σ² | `dnorm`, `pnorm`, `qnorm`, `rnorm` |
| Log-Normal(μ,σ²)：log X 正态 | x≥0；参数是 log(X) 的 μ、σ² | exp(μ+σ²/2)；exp(2(μ+σ²))−exp(2μ+σ²) | `dlnorm`, `plnorm`, `qlnorm`, `rlnorm` |
| Exponential(β)：一次等待/mean wait | x≥0；f=β⁻¹exp(−x/β)；λ=1/β | β；β² | `dexp`, `pexp`, `qexp`, `rexp`，R 用 `rate=λ` |
| Exponential(λ)：rate 参数化 | x≥0；f=λexp(−λx) | 1/λ；1/λ² | `rate` 不是 mean |
| Beta(α,β)：(0,1) 比例，shape 两参数 | 0≤x≤1；f=Γ(α+β)/[Γ(α)Γ(β)] · x^(α−1)(1−x)^(β−1) | α/(α+β)；αβ/[(α+β)²(α+β+1)] | `dbeta`, `pbeta`, `qbeta`, `rbeta` |
| Weibull(λ,k)：time-to-event，shape 改变风险 | x≥0；f=k/λ · (x/λ)^(k−1) exp(−(x/λ)^k) | λΓ(1+1/k)；λ²[Γ(1+2/k)−Γ²(1+1/k)] | `dweibull`, `pweibull`, `qweibull`, `rweibull` |
| Gamma(k,θ)：多个 Exponential 等待之和 | x≥0；f=x^(k−1)exp(−x/θ)/[Γ(k)θ^k] | kθ；kθ² | `dgamma`, `pgamma`, `qgamma`, `rgamma` |

- 一次下一事件、稳定速率、memoryless → Exponential。
- 第 k>1 次事件累计等待/多个独立 Exponential 之和 → Gamma；k=1 为 Exponential。
- 风险随时间增/减，shape k 控制 → Weibull；k=1 为 Exponential。
- log(X) bell-shaped → Log-Normal；仅“正值/右偏/等待时间” → Not enough information。
- 0–1 比例且两个 shape 参数 → Beta；固定区间等密度 → Uniform；对称 bell → Normal。
- 不要按符号猜参数：Exponential 的 λ 是 rate，Weibull 的 λ 是 scale。

## R d / p / q / r

- `d*` = density；`p*` = CDF；`q*` = quantile；`r*` = random sample。
- `dnorm(x=3, mean=2, sd=2)`：σ²=4 时传 `sd=2`，不是 4。
- `punif(q=c(0.25,0.5), min=0, max=2)`：求 CDF；`qunif(p=0.5, min=0, max=2)`：求中位数。
- `qexp(p=0.75, rate=1/beta)`：R 的 Exponential 用 rate；先确认题给的是 mean β 还是 rate λ。
- `rnorm(n=10, mean=0, sd=5)`：生成 10 个值；`d*` 返回密度高度，不是点概率。

## Bivariate continuous

- 联合 PDF f_X,Y(x,y) ≥ 0；全支持 ∬ f_X,Y(x,y)dxdy = 1；概率 = 事件区域下的体积。
- 边缘：f_X(x)=∫f_X,Y(x,y)dy；f_Y(y)=∫f_X,Y(x,y)dx。
- 独立时 f_X,Y(x,y)=f_X(x)f_Y(y)；没有独立不能直接相乘。
- 例：X,Y 独立且均匀在 [5,5.5]：联合密度 4；P(X<Y)=1/2；P(X≤5.2)=4×(0.2×0.5)=0.4。
- 计算前先画/描述区域：点、条、矩形、三角形；只对事件区域积分。

## Conditional density

- 事件条件 B：保留 B 内的 PDF，再除以 P(B)：f_X|B(x)=f_X(x)/P(B)（B 外为 0）；最后检查面积=1。
- 连续单点 P(X=x)=0，不能用点概率比值；给定 X=x：f_Y|X(y|x)=f_Y,X(y,x)/f_X(x)。
- 若独立：f_Y|X(y|x)=f_Y(y)。
- 支持也要更新：例如给定 X≥2500，x<2500 的条件密度为 0，x≥2500 的原密度重新归一化。

## Transformations

- 连续 `Y=g(X)`：先找 Y 的支持；把 Y 的事件改写成 X 的事件，或先求 `F_Y` 再求导；不能只替换 PDF 表达式。
- 一一对应且单调时：`f_Y(y) = f_X(g⁻¹(y)) · |d g⁻¹(y) / dy|`，仅在 Y 的支持内；导数绝对值是尺度因子。
- 多个有效反解时，必须把每条分支的密度贡献相加；先列出满足原 X 支持的反解，不能只取一个根。

```r
# X ~ Exponential(rate = 1), X ≥ 0; Y = X^2
# y < 0: F_Y(y) = 0
# y ≥ 0: F_Y(y) = P(X ≤ sqrt(y)) = 1 - exp(-sqrt(y))
# y > 0: f_Y(y) = exp(-sqrt(y)) / (2 * sqrt(y))
```

- `exp(−y²)` 或 `exp(−√y)` 单独都不是此变换的完整 PDF；后者是上例 CDF 的一部分，遗漏了导数因子。
- CDF 路径最稳：支持 → `{Y≤y}` 改写 → 原分布概率/CDF → 按 y 分段 → 求导并检查密度非负、积分为 1。

## 二元与条件题：最短流程

1. 写完整联合支持；PDF 在支持外为 0。
2. 先画/描述事件区域，再决定积分界；点、竖条、横条、矩形、三角形的面积不同。
3. 若题目给独立，先写 `f_X,Y = f_X · f_Y`；没给独立不能相乘。
4. 边缘：对另一变量、在其合法支持内积分；条件事件先限制支持，再除以条件事件的概率。
5. 给 `X=x` 时用 `f_Y|X(y|x) = f_Y,X(y,x) / f_X(x)`，不是 `P(Y=y)/P(X=x)`。

```r
# Uniform X,Y on [5, 5.5], independent:
# joint density = 4; P(X <= 5.2) = 4 * (0.2 * 0.5) = 0.4
# P(X < Y) = half the support square = 0.5
```

- 条件密度最终必须在新支持上积分为 1；若知道 X、Y 独立，`f_Y|X(y|x)` 直接等于 `f_Y(y)`。

## 读题与查错顺序

1. **对象**：离散/连续？题目要 PMF、PDF、CDF、survival、quantile、样本还是条件密度？
2. **支持**：端点、支持外为 0、参数合法性和单位是否已写清？
3. **操作**：区间用积分或 CDF 差；右尾用 `1−F`；分位点用 `q*`；随机样本用 `r*`。
4. **分布族**：先看生成过程与参数定义；只凭“正值”“右偏”或“等待时间”不够。
5. **R 参数**：Normal 传 `sd`；Exponential 传 `rate`；`p*` 的输入是数值 `q`，`q*` 的输入是概率 `p`。
6. **最后检查**：概率在 `[0,1]`；PDF/CDF 的支持和极限合理；条件密度重归一化；不要把 density 高度当点概率。
