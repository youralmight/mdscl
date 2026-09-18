# DSCI 551 Quiz 1 知识文档

> **第一阶段复习稿，不是 Cheat Sheet。** 本文只整理已确认的 Quiz 1 范围；不把任何历史课程材料当作本学期要求。

## 已确认的范围与考试信息

- **范围：**复习 Lecture 1–4 的全部 learning objectives：不确定性的表述、离散参数分布族、联合/边缘分布与依赖、条件概率与条件独立。
- **题型：**10–12 题；选择、多选、数值计算。
- **环境与时长：**本学期 MDS Quiz Guidelines 规定每个 MDS Quiz 为 50 分钟、在 PrairieLearn（PL）交付；DSCI 551 课程大纲说明 Quiz 在 ORCA 的监考数字评估环境完成。Lecture 4 幻灯片明确说 Quiz 期间可打开 RStudio workspace，且有 PrairieLearn practice quiz。
- **先看本文件的方式：**先能从题目叙述写出随机变量、事件和已知条件；再决定是从 PMF 求和、用分布族公式、从联合表边缘化，还是条件化。不要只按“见过某个公式”代入。

> **评估时以 assessment-specific instructions 为准。** 课程大纲明确禁止在 ORCA Quiz 中使用 GenAI，且禁止未经明确允许的外部协助或资源。

---

## 1. 总路线：从过程到更新后的分布

1. **描述不确定过程：**指定样本空间 $S$、事件 $A$、随机变量 $X$ 与可能结果。
2. **给出一个分布：**离散时用 PMF $p_X(x)=P(X=x)$，由它算事件概率、中心、离散程度和熵；若过程有固定结构，可选合适的参数分布族。
3. **同时考虑多个变量：**用联合 PMF $p_{X,Y}(x,y)$ 取得边缘分布、联合事件概率和依赖关系。
4. **收到信息后更新：**条件 $B$ 把 $B$ 变成新的样本空间；保留满足 $B$ 的结果并重新归一化。条件分布、联合分布和边缘分布可互相转换。

### 记号与底线

| 记号 | 含义 |
|---|---|
| $S$ | 样本空间：随机过程所有可能结果；$P(S)=1$。 |
| $A^c$ | $A$ 的补集（“不发生 $A$”）；$P(A^c)=1-P(A)$。 |
| $A\cap B$, $A\cup B$ | 分别为“$A$ **且** $B$”与“$A$ **或** $B$（至少一个）”。 |
| $X$ 与 $x$ | 大写 $X$ 是随机变量，小写 $x$ 是一个已实现/可能的值；随机变量也可以是类别而非数值。 |
| $p_X(x)$ | 离散 $X$ 的 PMF。必须 $p_X(x)\ge0$，且 $\sum_xp_X(x)=1$。一个事件的概率是满足该事件的所有 PMF 值之和。 |
| $\mathbb E[X]$, $\operatorname{Var}(X)$, $\sigma_X$ | 均值（期望）、方差、标准差，$\sigma_X=\sqrt{\operatorname{Var}(X)}$。数值型随机变量才有这些量。 |

---

## 2. 单一随机过程：概率、PMF 与摘要

### 2.1 概率法则：先画清事件关系

- **频率解释：**在本课使用的 frequentist 视角，重复观察时事件的相对频率在样本量趋于无穷时收敛到 $P(A)$。有限样本的比例是估计，不等于真概率。
- **全概率/分割：**若 $B_1,\ldots,B_k$ 两两不交且穷尽 $S$，且每个条件项的 $P(B_i)>0$，则 $P(A)=\sum_i P(A\cap B_i)=\sum_i P(A\mid B_i)P(B_i)$。
  **何时用：**一个目标事件可以按互斥情形完整拆开，尤其是已给“各组内概率 + 该组边缘概率”时。不要遗漏任何情形，也不要让分割重叠。
- **容斥原理：**$P(A\cup B)=P(A)+P(B)-P(A\cap B)$。
  两次相加会重复计入交集，所以必须减一次。若 $A,B$ 不交，交集为零，才可直接相加。
- **独立事件：**$A$ 和 $B$ 独立当且仅当 $P(A\cap B)=P(A)P(B)$。
  它们可同时发生；反之，两个概率都大于零的互斥事件**不可能**独立：互斥给 $P(A\cap B)=0$，独立会要求正的乘积。

**常见误读：**“or”不是只发生一个；除非题目说“exactly one”，$A\cap B$ 也属于 $A\cup B$。不要因为两个概率数字相同就假定独立。

### 2.2 概率、赔率与解释

若事件概率 $p=P(A)$，其**赔率**（odds）为发生相对不发生的比：
$$
o=\frac{p}{1-p},\qquad p=\frac{o}{1+o}.
$$
例如 $p=0.8$ 时 $o=4$，即 4:1（每一次不发生约有四次发生）。赔率适合比较“发生相对不发生”如何成倍改变；**赔率翻倍不等于概率翻倍**：4:1 $\to$ 8:1 时，概率由 $0.80$ 变为 $8/9\approx0.89$。

概率还可有不同哲学解释：frequentist 把它视为重复过程的长期频率；Bayesian 把它视为可随背景信息/先验更新的信念。二者不是“对/错”的选择；本 Quiz 需要知道它们在解释概率时回答的问题不同。

### 2.3 从 PMF 读出位置、离散和不确定性

对离散数值型 $X$：
$$
\mathbb E[X]=\sum_xx\,p_X(x),\qquad
\mathbb E[g(X)]=\sum_xg(x)p_X(x).
$$
Lecture 1 也区分两类随机变量：**离散**变量有可数结果并由 PMF 描述；**连续**变量有不可数结果并由 PDF $f_X(x)$ 描述。对连续数值型变量，$\mathbb E[g(X)]=\int g(x)f_X(x)\,\mathrm dx$，方差仍是 $\mathbb E\{[X-\mathbb E(X)]^2\}$。PDF 是密度而非单点概率，不能把 $f_X(x)$ 直接当作 $P(X=x)$。

均值是按概率加权的长期平均，**不必是可取的结果**。两个等价方差公式为
$$
\operatorname{Var}(X)=\mathbb E\{[X-\mathbb E(X)]^2\}
=\mathbb E[X^2]-[\mathbb E(X)]^2,
\qquad \operatorname{SD}(X)=\sqrt{\operatorname{Var}(X)}.
$$
第一式解释“围绕均值的平方偏离”，第二式通常较方便计算。方差以原单位的平方计，标准差恢复原单位。

| 摘要 | 如何取得 | 能回答什么 | 容易错在哪里 |
|---|---|---|---|
| Mode（众数） | 找最大 PMF 值对应的结果；可有多个并列众数。 | 最可能的结果。 | 不是均值，也不要求数值变量。 |
| 均值 | $\sum_xxp_X(x)$。 | 数值变量的典型/长期平均。 | 不能省略概率权重。 |
| 方差、标准差 | 先求 $\mathbb E[X]$，再用上式。 | 数值变量的离散程度。 | 方差绝不为负；不要把 $\mathbb E[X^2]$ 写成 $\mathbb E[X]^2$。 |
| 熵 $H(X)$ | $\displaystyle -\sum_xp_X(x)\log p_X(x)$；本课 $\log$ 为自然对数，且 $0\log0$ 按极限取 0。 | 由**概率分配**而非结果数值衡量的不确定性；熵为 0 表示无随机性。 | 熵不能为负；它可用于类别变量，不能把它与方差或“取值大小”混为一谈。 |

有限样本的 $\bar X=\frac1n\sum_{i=1}^nX_i$ 是 $\mathbb E[X]$ 的估计，不是已知模型均值本身。

---

## 3. 变换和线性规则：先问“变了什么”

令 $Z=g(X)$。新的随机变量有新的支持集和 PMF：
$$
P(Z=z)=\sum_{x:g(x)=z}P(X=x).
$$
**步骤：**列出 $X$ 的每个可能 $x$，映射到 $z=g(x)$，再把映射到同一 $z$ 的概率相加。若 $g$ 在给定支持上是一一对应，才会只是“换横轴、不合并概率”。

最小反例：若 $P(X=-1)=P(X=0)=P(X=1)=1/3$，$Z=X^2$，则
$$
P(Z=0)=1/3,\qquad P(Z=1)=P(X=-1)+P(X=1)=2/3.
$$
因此不能把 $-1$ 与 $1$ 的概率分别留在两个同为 $z=1$ 的格子里。

### 3.1 可以直接用的规则和条件

对常数 $a,b$，不要求独立：
$$
\mathbb E[aX+bY]=a\mathbb E[X]+b\mathbb E[Y].
$$
但一般而言
$$
\mathbb E[XY]\ne\mathbb E[X]\mathbb E[Y],\qquad
\mathbb E[X^2]\ne[\mathbb E[X]]^2.
$$

方差的缩放规则为 $\operatorname{Var}(aX)=a^2\operatorname{Var}(X)$。更一般地，
$$
\operatorname{Var}(aX+bY)=a^2\operatorname{Var}(X)+b^2\operatorname{Var}(Y)+2ab\operatorname{Cov}(X,Y).
$$
只有 $X,Y$ 独立（从而协方差为 0）时，才可删掉协方差项；特别地 $\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)$。

---

## 4. 用过程选择离散参数分布族

“Binomial family” 是所有 $(n,p)$ 组合形成的**一族**分布；$\operatorname{Binomial}(5,0.25)$ 才是其中一个完全指定的分布。参数是在某个 family 内把可能分布缩小到唯一一个的量。

| 家族与过程 | 支持集与 PMF | 均值、方差 | R：求 $P(X=x)$；关键陷阱 |
|---|---|---|---|
| $X\sim\operatorname{Bernoulli}(p)$：一次二元试验，成功=1、失败=0。 | $x\in\{0,1\}$，$p^x(1-p)^{1-x}$。 | $p,\ p(1-p)$。 | 可用 `dbinom(x, size = 1, prob = p)`。 |
| $X\sim\operatorname{Binomial}(n,p)$：$n$ 次**独立且成功概率相同**的试验中的成功数。 | $x=0,\ldots,n$，$\binom nxp^x(1-p)^{n-x}$。 | $np,\ np(1-p)$。 | `dbinom(x, size = n, prob = p)`；`size` 是试验总数，不是所求成功数。 |
| $X\sim\operatorname{Geometric}(p)$：首次成功**之前的失败数**。 | $x=0,1,\ldots$，$p(1-p)^x$。 | $(1-p)/p,\ (1-p)/p^2$。 | `dgeom(x, prob = p)` 与本课定义一致，$x=0$ 表示第一次就成功。有些教材把“首次成功所需试验数”定义为 Geometric；那是本定义 $+1$。 |
| $X\sim\operatorname{Negative\ Binomial}(k,p)$：第 $k$ 次成功前的失败数；独立、固定 $p$。 | $x=0,1,\ldots$，$\binom{k-1+x}{x}p^k(1-p)^x$。 | $k(1-p)/p,\ k(1-p)/p^2$。 | `dnbinom(x, size = k, prob = p)`；`size` 是成功数 $k$。$k=1$ 是 Geometric。 |
| $X\sim\operatorname{Poisson}(\lambda)$：固定时间/空间内独立到达事件的计数，平均率为 $\lambda$。 | $x=0,1,\ldots$，$\lambda^xe^{-\lambda}/x!$。 | $\lambda,\ \lambda$。 | `dpois(x, lambda = lambda)`；Poisson 的均值和方差必须相等。 |

参数条件：Bernoulli/Binomial 的 $0\le p\le1$、$n$ 为非负整数；Geometric/Negative Binomial 的 $0<p\le1$、$k$ 为正整数；Poisson 的 $\lambda\ge0$。`d*` 函数返回 **PMF 高度 $P(X=x)$**，不是累计概率，也不是随机抽样。

### 4.1 由均值和方差判断参数是否“够用”

只在**已知分布家族**时谈参数是否足够；只知道任意分布的均值和方差通常不能唯一确定整张 PMF。

1. 写出该 family 的均值/方差公式和已给信息。
2. 求参数，检查范围、整数条件和是否产生矛盾。
3. **够用：**得到唯一合法参数组合；**太少：**仍有多个合法组合；**太多：**信息冗余或彼此矛盾。

有用的快速检查：

- Bernoulli：$\mu=p$、$v=\mu(1-\mu)$。均值已指定分布；再给方差是冗余检查，若不等于该式则不可能。
- Poisson：$\mu=v=\lambda$。给均值已够；均值与方差不同则不能是 Poisson。
- Geometric（本课“失败数”定义）：$p=1/(\mu+1)$、$v=\mu(\mu+1)$。均值已够。
- Binomial（非退化 $\mu>0$）：$p=1-v/\mu$，$n=\mu/p$。必须有 $0\le p\le1$ 且 $n$ 是合法整数；合法时均值和方差够用。
- Negative Binomial（$0<p<1$）：$p=\mu/v$、$k=\mu^2/(v-\mu)$，所以还要 $v>\mu$ 且 $k$ 为正整数。

---

## 5. 两个变量：联合分布先于“关系”

### 5.1 联合、边缘和事件

联合 PMF $p_{X,Y}(x,y)=P(X=x,Y=y)$ 为每个可能对 $(x,y)$ 赋概率，所有单元格之和必须为 1。顺序可重要，例如两次抛硬币的 $HT$ 与 $TH$ 是不同联合结果。

从联合表得到边缘分布时，**对另一个变量所有可能值求和**：
$$
p_X(x)=\sum_yp_{X,Y}(x,y),\qquad p_Y(y)=\sum_xp_{X,Y}(x,y).
$$
表格中是“加行”还是“加列”取决于哪个变量放在行/列；原则永远是消去另一个变量。整张联合表和每个边缘 PMF 各自应归一化；一行或一列一般**不会**各自等于 1。

联合表能推出边缘；反过来，两条边缘 PMF **不能**唯一推出联合表，因为它们没有说明变量如何一起变化。对 $X,Y$ 的事件题，先列出所有满足条件的 $(x,y)$ 单元格，再相加；不要只凭单独边缘概率相乘。

### 5.2 独立是对整张联合分布的断言

$$
X\perp Y
\quad\Longleftrightarrow\quad
p_{X,Y}(x,y)=p_X(x)p_Y(y)\quad\text{对所有 }x,y.
$$

**检验流程：**从联合表求边缘；把每一个相应边缘乘积与联合单元格比较。任一不相等即不独立；所有都相等才可结论独立。若题目明确独立，已知两条边缘即可用乘积重建整个联合表。

独立且相关期望存在时：
$$
\mathbb E[XY]=\mathbb E[X]\mathbb E[Y],\qquad
\operatorname{Cov}(X,Y)=0.
$$
反向不成立：协方差为 0 或 Pearson 相关为 0 只表示没有线性趋势，不能证明独立。实验室的 $Y=X^2$ 对称例子正是 $X,Y$ 确定性相关但协方差为 0。

### 5.3 协方差、Pearson 与 Kendall 衡量的不是同一件事

对数值变量：
$$
\operatorname{Cov}(X,Y)
=\mathbb E[(X-\mu_X)(Y-\mu_Y)]
=\mathbb E[XY]-\mathbb E[X]\mathbb E[Y],
$$
其中 $\mathbb E[XY]=\sum_x\sum_yxy\,p_{X,Y}(x,y)$。协方差正/负分别表示共同增减/一增一减的**线性**方向；数值受单位缩放影响，且 0 不等于独立。

当两者方差均为正时，Pearson 相关为
$$
\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sqrt{\operatorname{Var}(X)\operatorname{Var}(Y)}}\in[-1,1].
$$
它标准化了协方差，衡量**线性**关系：$-1$、0、1 分别是完美负线性、无**线性**关系、完美正线性；方差为 0 时该相关系数未定义。

Kendall 的 $\tau_K$ 用样本中每一对观测的排序：两对 $(x_i,y_i),(x_j,y_j)$ 同向排序为 concordant，反向为 discordant。无 ties 时
$$
\tau_K=\frac{\#\text{concordant}-\#\text{discordant}}{\binom n2}.
$$
它衡量**单调**关系，故非线性但严格递增的 $Y=X^3$ 也可有 $\tau_K=1$。`cor(x, y, method = "pearson")` 与 `cor(x, y, method = "kendall")` 分别计算样本 Pearson/Kendall 相关；不要把 0 当作独立证明。非单调的 $Y=X^2$ 可以同时有 Pearson=0、Kendall=0，却仍由 $X$ 完全决定。

---

## 6. 条件概率：信息改变样本空间

对 $P(B)>0$，
$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)}.
$$
条件 $B$ 不是“再乘一个概率”，而是把 $B$ 作为新的样本空间：条件 PMF 对所有可能结果仍须和为 1。

### 6.1 从完整 PMF 或联合表构造条件分布

**离散条件化 workflow：**

1. 写清条件 $B$，删去不满足 $B$ 的结果（概率变 0）。
2. 求保留结果的原始总概率 $P(B)$。
3. 把每个保留的联合/边缘概率除以 $P(B)$。
4. 检查新的概率和为 1，再用这个条件 PMF 求条件概率或条件期望。

例如 $(P(X=1),P(X=2),P(X=3),P(X=4))=(0.1,0.2,0.3,0.4)$。已知 $X\ge3$ 时，$P(X\ge3)=0.7$，所以
$$
P(X=3\mid X\ge3)=0.3/0.7=3/7,
\quad P(X=4\mid X\ge3)=4/7.
$$
比值 $0.3:0.4$ 保持，但它们需重新缩放；$X=1,2$ 已不可能。

对两个变量，
$$
P(Y=y\mid X=x)=\frac{P(Y=y,X=x)}{P(X=x)},
$$
即从联合表取条件 $X=x$ 对应的一行/列，再除以该行/列总和。一般 $P(A\mid B)\ne P(B\mid A)$，因为分母不同。

### 6.2 联合、边缘与条件分布之间的转换

下列式子是同一关系的不同方向（条件事件概率必须大于 0）：
$$
\begin{aligned}
P(Y=y,X=x)&=P(Y=y\mid X=x)P(X=x),\\
P(Y=y)&=\sum_xP(Y=y\mid X=x)P(X=x),\\
\mathbb E[Y]&=\sum_x\mathbb E[Y\mid X=x]P(X=x)
=\mathbb E_X\big[\mathbb E[Y\mid X]\big].
\end{aligned}
$$
第二式是全概率公式，最后一式是全期望定律：用每个 $X=x$ 情形的条件均值，按 $X$ 的边缘概率加权，而不是把条件均值等权平均。若 $X\perp Y$，则 $P(Y=y\mid X=x)=P(Y=y)$：知道 $X$ 不应改变 $Y$ 的分布。

### 6.3 条件独立不同于边缘（普通）独立

| 概念 | 要检验的式子 | 直觉 |
|---|---|---|
| 边缘独立 $X\perp Y$ | $P(X=x,Y=y)=P(X=x)P(Y=y)$ | 未知道其他变量时，得知一个不改变另一个。 |
| 给定 $Z$ 的条件独立 $X\perp Y\mid Z$ | $P(X=x,Y=y\mid Z=z)=P(X=x\mid Z=z)P(Y=y\mid Z=z)$，对每个 $P(Z=z)>0$ 的 $z$ 成立。 | 已知道 $Z$ 后，$X$ 对 $Y$ 不再提供额外信息。 |

**检验条件独立：**对每个 $z$ 分别把三变量联合表限制到 $Z=z$、用 $P(Z=z)$ 重新归一化、求两个条件边缘，再检验条件联合是否分解。二元变量且条件边缘已给时，核对 $(X,Y)=(1,1)$ 的一个格子可推出余下三格；一般多类别情形必须检查全部组合。

普通独立不保证给定 $Z$ 后仍独立，反之亦然。$Z$ 可能解释掉 $X,Y$ 的表面关联，也可能像“报警已响”那样使原本独立的两个原因在条件下相关。不要用相关系数来代替这个联合分布检验。

---

## 7. 考前自检：按目标做题

- 能从 PMF 求 $P(A)$、mode、$\mathbb E[X]$、$\operatorname{Var}(X)$、$\operatorname{SD}(X)$、$H(X)$，并解释各量代表什么。
- 能识别互斥、独立、补集、完整不交分割，并选择容斥或全概率公式。
- 能在概率与赔率间双向转换，并说明为何“倍数赔率”不能直接读成“倍数概率”。
- 能从真实过程的“成功/失败次数、到第几次成功、固定窗口到达数”区分 Bernoulli、Binomial、Geometric、Negative Binomial、Poisson；能写出其支持、PMF、均值和方差，并正确调用相应 R `d*` 函数。
- 能把 $Z=g(X)$ 的值映射并合并撞到同一 $z$ 的概率；能在独立条件满足时使用方差相加规则。
- 能从联合 PMF 求边缘、联合事件、$\mathbb E[XY]$、协方差和 Pearson 相关，并以完整因子分解检验独立。
- 能说清 independence、零协方差/零 Pearson、零 Kendall 的不同强度；能从 concordant/discordant 对计算无 ties 的 $\tau_K$。
- 能由完整 PMF 或联合表限制、归一化得到条件 PMF，随后求条件概率/条件期望；能用全概率和全期望在条件、联合、边缘形式间转换。
- 能在每个 $Z=z$ 下检验条件独立，并说明它不等同于普通独立。

---

## 来源与未确认事项

### 本文使用的本学期官方来源

- `official/current/DSCI_551_stat-prob-dsci_students/website/learning-goals.qmd`：Lecture 1–4 的逐讲 learning objectives。
- `official/current/DSCI_551_stat-prob-dsci_students/notes/01_lecture-uncertainty.qmd` 至 `04_lecture-conditional.qmd`：定义、公式、例子与 Lecture 3 的 optional 标记。
- `official/current/DSCI_551_stat-prob-dsci_students/slides/04_lecture-conditional/04_lecture-conditional.qmd`：Quiz 1 的范围、10–12 题题型、PrairieLearn practice quiz、RStudio workspace。
- `official/current/DSCI_551_stat-prob-dsci_students/release/lab1/student/lab1.Rmd`、`release/lab2/student/lab2.Rmd`：Block 1 的应用、条件化 workflow、依赖度量与条件独立练习。
- <https://ubc-mds.github.io/resources_pages/quiz_guidelines/>：所有 MDS Quiz 的 50 分钟时长与 PrairieLearn 交付方式；具体资源权限仍由 instructor policy 决定。
- `official/current/DSCI_551_stat-prob-dsci_students/README.md`：Quiz 1 权重、ORCA、assessment-specific instruction 与 GenAI 政策；`notes/messages.md` 未提供额外的 Quiz 1 范围或工具规定。

### [未确认]

- Quiz 1 的精确日期/时间窗、ORCA reservation、每题计分与 partial credit：本学期 README 只指向 MDS calendar，所读材料未给出这些细节。
- 可带/可用的具体资源（包括个人 Cheat Sheet、计算器、纸笔、RStudio 的包/文件/网络访问）未在已读 Quiz 1 幻灯片中完整列明；不可因“可开 RStudio”推断其他权限。以 Quiz/ORCA 的 assessment-specific instructions 为准。
- Lecture 3 的 mutual information 在讲义中明确标为 **Optional**，且不在 Lecture 3 learning objectives 中；没有更明确的 Quiz 1 说明前，本文不把它当作已确认核心范围。
- 幻灯片确认 PrairieLearn practice quiz 存在，但学生版当前课程仓库没有其题目或链接；因此本文没有从该 practice assessment 推断额外考点。
