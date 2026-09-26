# DSCI 551 Quiz 2

## Continuous distributions

- PDF `f(x) ≥ 0`, `∫ f(x)dx = 1`; density may exceed 1. `P(X=x)=0`; interval probability is area: `P(a≤X≤b)=∫ₐᵇf(x)dx=F(b)−F(a)`.
- `F(x)=P(X≤x)=∫₋∞ˣf(t)dt`; `S(x)=P(X>x)=1−F(x)`; quantile `Q(p)=F⁻¹(p)`. CDF is nondecreasing, in `[0,1]`, limits 0/1. Continuous `<`/`≤` probabilities agree.
- `E[g(X)]=∫g(x)f(x)dx`; `Var(X)=E[X²]−E[X]²`; `SD=√Var`. Median `Q(.5)`; mode maximizes density. Central `p` interval: `[Q((1−p)/2), Q((1+p)/2)]`.
- Right-skew: usually mode < median < mean; left-skew: mean < median < mode.

## Family identification & parameters

| Family / cue | Support; parameterization | Mean; variance |
|---|---|---|
| Uniform(a,b), constant density | `[a,b]`; `f=1/(b−a)` | `(a+b)/2`; `(b−a)²/12` |
| Normal(μ,σ²), symmetric bell | real; `σ` is SD | `μ`; `σ²` |
| Lognormal(μ,σ²), `log X~N(μ,σ²)` | `x>0` | `exp(μ+σ²/2)`; `exp(2μ+σ²)(exp(σ²)−1)` |
| Exponential(mean β) | `x≥0`; `f=β⁻¹exp(−x/β)`, rate `λ=1/β` | `β`; `β²` |
| Beta(α,β), proportion | `[0,1]`; shapes α,β | `α/(α+β)`; `αβ/[(α+β)²(α+β+1)]` |
| Weibull(scale λ, shape k), event time | `x≥0`; `f=(k/λ)(x/λ)^(k−1)e^(−(x/λ)^k)` | `λΓ(1+1/k)`; `λ²[Γ(1+2/k)−Γ²(1+1/k)]` |
| Gamma(shape k, scale θ), sum of waits | `x≥0`; `f=x^(k−1)e^(−x/θ)/(Γ(k)θ^k)` | `kθ`; `kθ²` |

- Single next event, constant rate, memoryless → Exponential. kth accumulated event / sum of exponentials → Gamma. Weibull shape controls changing hazard; `k=1` is Exponential. Log(X) bell-shaped → Lognormal. Proportion → Beta; bounded constant density → Uniform. Positive/right-skewed/waiting-time alone does not identify family.
- Do not infer parameter meaning from symbol: Exponential λ=rate; Weibull λ=scale; Normal σ=SD, not variance.

## R distribution functions

- `d*` density, `p*` CDF, `q*` quantile, `r*` random draws. `p*(q=...)`; `q*(p=...)`; density is not point probability.
- `dnorm(x, mean=μ, sd=σ)` (pass SD); `dexp(x, rate=λ)` (rate, not mean β); `dweibull(x, shape=k, scale=λ)`. Other families: `d/p/q/r` + `unif`, `lnorm`, `beta`, `gamma`.

R call examples: `pexp(q=3, rate=1/β)` gives `P(X≤3)`; `1-pexp(q=3, rate=λ)` gives the upper tail. `qnorm(.975, mean=μ, sd=σ)` returns the 97.5th percentile; `rpois(n=1000, lambda=λ)` draws 1000 counts. Always match `p*` input `q` and `q*` input probability `p`.

For a central 90% interval, use `q*(.05)` and `q*(.95)`; for a right-tail probability `P(X>a)`, use `1-p*(a)` or `lower.tail=FALSE`.


## Joint, marginal, conditional

- Joint PDF nonnegative, integrates to 1 over joint support; event probability is region integral. Marginals: `f_X(x)=∫f_X,Y(x,y)dy`, `f_Y(y)=∫f_X,Y(x,y)dx` over legal support.
- Independence permits `f_X,Y=f_X f_Y`; otherwise do not multiply. Draw/describe event region to set bounds.
- Event conditioning: restrict to event support, `f_X|B(x)=f_X(x)/P(B)` within B, zero outside. Point conditioning: `f_Y|X(y|x)=f_X,Y(x,y)/f_X(x)`; if independent, equals `f_Y(y)`. Conditional density integrates to 1 on updated support.

Example: independent `X,Y~Uniform(5,5.5)` has joint density `4` on the support square. The event `X<Y` is half the square, so probability `1/2`; `P(X≤5.2)=4×0.2×0.5=0.4`. For non-rectangular events, split the integral at the support/event boundary.

Conditioning checklist: (1) restrict to the event's support; (2) divide by event probability, or for `X=x` divide joint density by marginal density; (3) verify the conditional density integrates to 1.

## Transformations `Y=g(X)`

- Find Y support. CDF route: rewrite `{Y≤y}` as an X event, evaluate by original CDF/probability, split by support, differentiate.
- One-to-one: `f_Y(y)=f_X(g⁻¹(y))·|d g⁻¹(y)/dy|`; multiple valid inverse branches: sum each contribution. Keep Jacobian factor.
- Example `X~Exp(rate=1), Y=X²`: `F_Y(y)=0` for `y<0`, else `1−e^(−√y)`; `f_Y(y)=e^(−√y)/(2√y)` for `y>0`.

If `g` is not one-to-one, sum every valid inverse branch. Example: `X~Uniform(-1,1)`, `Y=X²`; for `0<y<1`, roots `±√y` both contribute, giving `f_Y(y)=1/(2√y)`.

## iid and likelihood / MLE

- iid sample `y₁,…,yₙ`: independent, same distribution/parameters. Seed does not create iid; dependence may violate model.
- Fix observed data, vary parameter: likelihood `L(θ|y)=∏ᵢ f(yᵢ|θ)` (PMF for discrete data); it is a function of θ, not a probability distribution over θ. `ℓ(θ)=Σᵢlog f(yᵢ|θ)` has same maximizer and avoids underflow.
- Grid MLE: evaluate log-likelihood on legal θ grid; take `argmax` (`which.max`); grid spacing gives approximation. Analytical: differentiate log-likelihood, set derivative to zero, check support/boundaries and maximum.
- Exponential(mean β): `ℓ(β)=−n log β−Σyᵢ/β`; `β̂=ȳ` (second derivative `−n/β²<0`). In R use `rate=1/β`.
- Bernoulli(p): `ℓ(p)=Σy log p+(n−Σy)log(1−p)`; `p̂=ȳ`. For grid search keep `p∈[0,1]`; endpoints with incompatible data give `log(0)`.
- Poisson(λ): grid concept—evaluate `Σ dpois(y, lambda=λ, log=TRUE)` on legal `λ≥0`, maximize; distinguish observed y from candidate λ.
```r
# Exponential mean β: maximize the log-likelihood; β̂ also equals mean(y)
ll_exp <- function(beta) sum(dexp(y, rate = 1 / beta, log = TRUE))
beta_grid <- seq(0.1, 10, by = 0.01)
beta_grid[which.max(vapply(beta_grid, ll_exp, numeric(1)))]

# Bernoulli MLE grid; observed y contains 0/1 values
p_grid <- seq(0.001, 0.999, by = 0.001)
ll <- sum(y) * log(p_grid) + (length(y)-sum(y)) * log(1-p_grid)
p_grid[which.max(ll)]  # analytical estimate: mean(y)
```


## Reproducible simulation & Monte Carlo


- Define one replicate’s random mechanism (including dependencies), repeat complete replicate, summarize simulated outcomes. Theoretical quantities belong to model; empirical quantities to draws (`mean(x)`, `var(x)` with R denominator `n−1`, `mean(x==0)`, quantiles). Finite estimates differ; LLN: iid sample mean approaches theoretical mean as n grows.
- Set seed once before experiment; same seed/RNG settings reproduce draws within a system, not necessarily across R/Python. Never reset seed inside each replicate.

- R: `set.seed(551)` once; `sample(x, size, replace=TRUE, prob=...)`; `rbinom(n=draws, size=trials, prob=p)` (`n`=draw count, `size`=trials); `rpois(n, lambda)`.
- Python: `rng = np.random.default_rng(551)`; `rng.choice(x, size=n, replace=True, p=...)`; `stats.binom.rvs(n=trials, p=p, size=draws, random_state=rng)`; `stats.poisson.rvs(mu=lambda, size=n, random_state=rng)`.
- Multi-step conditional simulation: simulate stage 1, use its result to parameterize/decide stage 2, then summarize the full replicate. E.g., attendance Bernoulli → draw Poisson cupcakes only for attendees → total. Do not replace random draws by conditional means or simulate outcomes for absent cases; distinguish replicate count from distribution parameters.

One-step probability estimate: `mean(simulated_event)` because `TRUE=1`, `FALSE=0`; for a Bernoulli sample, `mean(y)` estimates `p`. Empirical PMF: `table(x) / length(x)`. Larger independent replication usually reduces Monte Carlo variability, not to zero.

```r
set.seed(551)
misses <- rbinom(n = 10000, size = 2, prob = 0.30)
p_miss_both <- mean(misses == 2)  # theoretical: 0.30^2
empirical_pmf <- prop.table(table(misses))
```

Conditional mixture: if attendance `A~Bernoulli(p)` and `C|A=1~Poisson(λ)`, with `C=0` when absent, then `P(C=0)=1−p+p·e^(−λ)`; for `c≥1`, `P(C=c)=p·e^(−λ)λ^c/c!`. The mass at zero includes both absence and an attendee consuming zero.
## Solve-and-check workflow

1. Identify the variable type, support, units, and data-generating process; choose PMF/PDF family from the process, not from “positive” or “count” alone.
2. Probability target: discrete event → sum PMF; continuous interval → area or `F(b)−F(a)`; right tail → `1−F(a)`; quantile → solve `F(x)=p` / call `q*`.
3. Bivariate event: write joint support, mark the event region, set integration bounds; factor the joint density only after independence is stated.
4. MLE: observed values are fixed, parameter varies. Write one-observation PMF/PDF → iid product → log-likelihood → legal parameter domain → grid maximum or derivative/root → verify a maximum.
5. Simulation: write one full replicate in dependency order → repeat with one seed set before the run → summarize empirical mean/proportion/quantile → compare to theoretical benchmark and explain finite-run variation.
6. Sanity checks: probability in `[0,1]`; density integrates to 1; conditional density renormalizes on updated support; estimate lies in parameter range; distinguish replication count from distribution parameters.

