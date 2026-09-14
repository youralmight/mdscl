# DSCI 551 Quiz 1

X is a random variable; x is a possible/realized value. Random variables may be categorical, though moments require numerical values.

## Core notation and probability rules

| Item | Rule / meaning |
|---|---|
| Sample space | S: all outcomes; P(S) = 1. |
| Complement | P(Aᶜ) = 1 − P(A). |
| Union / intersection | A ∪ B: at least one; A ∩ B: both. P(A ∪ B) = P(A) + P(B) − P(A ∩ B). |
| Partition / total probability | If {Bᵢ} is mutually exclusive, exhaustive, and P(Bᵢ) > 0: P(A) = Σᵢ P(A | Bᵢ) P(Bᵢ). |
| Independence | A ⟂ B iff P(A ∩ B) = P(A)P(B). Positive-probability mutually exclusive events are **not** independent. |
| Odds | o = p/(1 − p), p = o/(1 + o). Multiplying odds does not multiply probability by the same factor. |

- “or” includes the intersection unless the question says **exactly one**.
- Equal probabilities do not imply independence.
- Frequentist probability: long-run relative frequency; Bayesian probability: belief updated by information.

## PMF, summaries, and transformations

For a discrete X, p_X(x) = P(X = x), p_X(x) ≥ 0, and Σₓ p_X(x) = 1. For an event, sum the PMF over its allowed values.

- E[X] = Σₓ x p_X(x); E[g(X)] = Σₓ g(x)p_X(x).
- Var(X) = E[(X − E[X])²] = E[X²] − E[X]²; SD(X) = √Var(X).
- H(X) = −Σₓ p_X(x) log p_X(x), with 0 log 0 := 0.

| Quantity | Key point / trap |
|---|---|
| Mode | Value(s) with largest PMF; may tie; works for categories. |
| Mean | Probability-weighted long-run average; need not be an attainable value. |
| Variance / SD | Var(X) ≥ 0, in squared units; SD restores units. Do not confuse E[X²] with E[X]². |
| Entropy | Natural log; uncertainty of the probability distribution, not magnitude of outcomes; H = 0 means no randomness. |
| Continuous X | PDF f_X(x) is a density, **not** P(X = x); E[g(X)] = ∫ g(x)f_X(x) dx. |
| Sample mean | X̄ = (1/n)ΣᵢXᵢ estimates E[X]; it is not automatically the model mean. |

For Z = g(X), first map every support point, then combine collisions: P(Z = z) = Σ₍ₓ: g(x)=z₎ P(X = x).

Example: if X ∈ {−1, 0, 1} is uniform and Z = X², then P(Z = 0) = 1/3 and P(Z = 1) = 2/3.

### Linear rules

- E[aX + bY] = aE[X] + bE[Y] (no independence needed).
- Var(aX) = a²Var(X).
- Var(aX + bY) = a²Var(X) + b²Var(Y) + 2ab Cov(X, Y).

Use E[XY] = E[X]E[Y] or drop the covariance term **only when X and Y are independent**.

## Discrete distribution families

| Distribution / process | Support and PMF | Mean, variance | R / distinction |
|---|---|---|---|
| Bernoulli(p): one success/failure trial | x ∈ {0, 1}; pˣ(1 − p)¹⁻ˣ | p; p(1 − p) | `dbinom(x, size = 1, prob = p)` |
| Binomial(n, p): successes in n independent trials with common p | x = 0, …, n; C(n, x)pˣ(1 − p)ⁿ⁻ˣ | np; np(1 − p) | `dbinom(x, size = n, prob = p)`; `size` is trials, not requested successes. |
| Geometric(p): failures **before first success** | x = 0, 1, …; p(1 − p)ˣ | (1 − p)/p; (1 − p)/p² | `dgeom(x, prob = p)`; x = 0 = immediate success. “Trial number of first success” is this variable + 1. |
| NegBin(k, p): failures before k-th success | x = 0, 1, …; C(k − 1 + x, x)pᵏ(1 − p)ˣ | k(1 − p)/p; k(1 − p)/p² | `dnbinom(x, size = k, prob = p)`; `size` is successes. k = 1 is Geometric. |
| Poisson(λ): count of independent arrivals in a fixed window | x = 0, 1, …; λˣe⁻λ/x! | λ; λ | `dpois(x, lambda = lambda)`; mean = variance. |

Parameters: Binomial 0 ≤ p ≤ 1 and n ∈ {0, 1, …}; Geometric / NegBin 0 < p ≤ 1 and k ∈ {1, 2, …}; Poisson λ ≥ 0. R `d*` functions return P(X = x), not a CDF or random draw.

**Family vs distribution:** a family contains all legal parameter combinations; parameters specify one distribution.

### Recovering parameters from μ and v (only after family is known)

| Family | Fast check |
|---|---|
| Bernoulli | p = μ; v = μ(1 − μ). Mean determines it; incompatible variance means impossible. |
| Poisson | λ = μ = v. Mean determines it; μ ≠ v means not Poisson. |
| Geometric | p = 1/(μ + 1); v = μ(μ + 1). Mean determines it. |
| Binomial, μ > 0 | p = 1 − v/μ; n = μ/p; require legal p and integer n. |
| NegBin, 0 < p < 1 | p = μ/v; k = μ²/(v − μ); require v > μ and integer k > 0. |

A unique legal parameter set is sufficient; multiple legal sets mean insufficient information; contradictions mean impossible. Mean and variance alone do **not** determine an arbitrary PMF.

## Joint distributions, marginals, and dependence

- p_X,Y(x, y) = P(X = x, Y = y); ΣₓΣᵧ p_X,Y(x, y) = 1.
- p_X(x) = Σᵧ p_X,Y(x, y); p_Y(y) = Σₓ p_X,Y(x, y).

- To find an event probability from a joint table, identify all allowed (x, y) cells and sum them.
- Marginals do not determine the joint distribution. Do not multiply marginal probabilities unless independence is given or verified.
- To test X ⟂ Y: compute both marginals, then verify p_X,Y(x, y) = p_X(x)p_Y(y) for **every** cell. One failure disproves independence.

- E[XY] = ΣₓΣᵧ xy p_X,Y(x, y).
- Cov(X, Y) = E[XY] − E[X]E[Y].
- ρ_XY = Cov(X, Y) / √(Var(X)Var(Y)), with −1 ≤ ρ_XY ≤ 1 if both variances are positive.

| Measure / implication | What it does **not** establish |
|---|---|
| Independent ⇒ E[XY] = E[X]E[Y] and Cov(X, Y) = 0 | — |
| Cov(X, Y) = 0 or Pearson ρ = 0 | Does not imply independence; it only rules out linear association. |
| Pearson ρ | Standardized **linear** association; undefined if either variance is 0. |
| Kendall τ_K | Rank-based **monotonic** association. Without ties: τ_K = (number concordant − number discordant)/C(n, 2). |

A non-monotonic deterministic relationship such as Y = X² can have Pearson = 0 and Kendall = 0, yet Y is fully determined by X. A strictly increasing nonlinear relationship such as Y = X³ can have τ_K = 1.

## Conditional probability and conditional independence

- For P(B) > 0: P(A | B) = P(A ∩ B) / P(B).
- Conditioning restricts the sample space to B: discard excluded outcomes, divide each retained probability by P(B), and check the resulting PMF sums to 1.
- P(Y = y | X = x) = P(Y = y, X = x) / P(X = x), for P(X = x) > 0.
- P(Y = y, X = x) = P(Y = y | X = x)P(X = x).
- P(Y = y) = Σₓ P(Y = y | X = x)P(X = x).
- E[Y] = Σₓ E[Y | X = x]P(X = x) = E_X[E[Y | X]].

- P(A | B) ≠ P(B | A) in general: denominators differ.
- Under X ⟂ Y, P(Y = y | X = x) = P(Y = y): learning X does not change Y's distribution.
- For total expectation, weight conditional means by P(X = x); do not take an unweighted average.

X ⟂ Y | Z iff P(X = x, Y = y | Z = z) = P(X = x | Z = z)P(Y = y | Z = z) for every z with P(Z = z) > 0.

To test conditional independence: for each z, restrict the three-way joint distribution to Z = z, renormalize, obtain conditional marginals, and test factorization across all (x, y). Marginal independence and conditional independence do not imply one another; use the distributional test, not a correlation coefficient.
