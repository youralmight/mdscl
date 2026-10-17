# DSCI 552 Quiz 1

## Objects: identify before computing

| Object | One value in the distribution | Center/spread meaning |
|---|---|---|
| Population | one population member's measurement | parameter (μ, p); individual variability |
| Sample | one sampled member's measurement | statistic (x̄, p̂); within-sample SD |
| Sampling distribution | one statistic from one repeated sample | E(T); SE = SD across statistics |
| Bootstrap distribution | one statistic from one resample of the observed sample | centered near observed statistic; estimates SE |
| Null distribution | one statistic from data generated/permuted under H₀ | extremeness under H₀; yields p-value |

Population parameter is fixed/unknown; estimator is a random rule before sampling; estimate is its realized value. Sample statistic can be an estimator when used for a parameter.

Mean: μ = Σyᵢ/N; x̄ = Σxᵢ/n. Proportion: p̂ = successes/n = mean(condition). Bias(T)=E(T)−θ. SE(T)=SD of T's sampling distribution—not SD of raw observations and not distance to truth.

**n** = observations per sample/resample; **m** = repeated population samples in simulation; **b/B** = bootstrap repetitions. Larger n usually lowers estimator SE under a suitable design. Larger m/B only stabilizes the simulated distribution; it adds no original information and does not fix bias.

## Sampling + estimation

Random sampling describes selection; representative describes relation to target population. Random within the wrong frame does not generalize to the desired population. Random sampling supports population generalization; random treatment assignment supports causal comparison—different jobs.

- Without replacement: same member cannot repeat within one sample; used for finite-population sampling.
- With replacement: records can repeat/vanish; required for ordinary bootstrap.
- Sampling variation remains even with a good design. Systematic undercoverage/selection does not disappear with bigger n or more repetitions.

```r
set.seed(552)
samples <- pop |> rep_sample_n(size=n, reps=m, replace=FALSE)
sampling_dist <- samples |>
  group_by(replicate) |>
  summarise(stat=mean(value), .groups="drop")
se_sim <- sd(sampling_dist$stat)
```

`rep_sample_n()` returns original columns + `replicate`, usually grouped; output rows = `size*reps`. `replicate` is sample ID, not member ID. `ungroup()` removes grouping metadata, not the column.

## Bootstrap distribution + CI

Given observed sample of size n:
1. draw n rows **with replacement**; 2. calculate same statistic; 3. repeat B times. Resampling n rows without replacement only permutes the data → zero variability for order-invariant statistics.

```r
set.seed(552)
boot <- observed |>
  specify(response=value) |>
  generate(reps=2000,type="bootstrap") |>
  calculate(stat="mean")
boot_se <- sd(boot$stat)
ci95 <- boot |> get_confidence_interval(level=.95,type="percentile")
```

Proportion:
```r
boot_p <- observed |>
  specify(response=outcome,success="yes") |>
  generate(reps=2000,type="bootstrap") |>
  calculate(stat="prop")
```

Percentile (1−α) CI = empirical quantiles α/2 and 1−α/2 of bootstrap statistics. 95% → 2.5%/97.5%; 90% → 5%/95%; 99% → 0.5%/99.5%. Higher confidence (same data/method) → wider interval. Larger representative n usually → narrower interval.

**Correct interpretation:** if the sampling + interval procedure were repeated many times, about 95% of 95% intervals would capture θ. For this already-computed frequentist interval, do **not** say P(θ lies inside)=.95.

Bootstrap approximates what the observed sample contains. It cannot restore missing groups/tails, repair selection bias, or create real observations. Small/biased samples, boundaries, extreme skew, or nonsmooth statistics can give poor percentile coverage.

Visualization: show observations when possible + point estimate + labeled CI. SD, SE, percentile range, and CI are different. Overlap of two separate group CIs is not a formal test of their difference.

## Hypotheses + test statistic

Hypotheses concern **population parameters**, not observed statistics.

Two proportions, define δ = p_A − p_B:
- H₀: δ=0; two-sided H_A: δ≠0; right-sided: δ>0; left-sided: δ<0.
- observed statistic δ̂ = p̂_A − p̂_B. `order=c("A","B")` means A−B; keep it consistent with H_A.

Decision framework:
1. state population/parameter + H₀/H_A/sidedness; 2. calculate observed t_obs; 3. generate data under H₀; 4. recalculate statistic many times; 5. find tail proportion at least as extreme as t_obs; 6. p<α → reject H₀, otherwise fail to reject.

**p-value:** under H₀/null model, probability of a statistic as or more extreme than observed. It is not P(H₀ true), P(chance caused result), effect size, study quality, or replication probability. Fail to reject ≠ accept/prove H₀.

## Permutation randomization test

Under an independence/no-difference null, shuffle group labels **without replacement**, retaining outcomes and group sizes while breaking the original association. Requires exchangeability/design justification; ordinary shuffling must respect pairing, blocks, clusters, repeated measures. Observational association still does not become causal.

```r
obs <- data |>
  specify(response=outcome,explanatory=group,success="yes") |>
  calculate(stat="diff in props",order=c("A","B"))
set.seed(552)
null <- data |>
  specify(response=outcome,explanatory=group,success="yes") |>
  hypothesize(null="independence") |>
  generate(reps=2000,type="permute") |>
  calculate(stat="diff in props",order=c("A","B"))
p <- null |> get_p_value(obs_stat=obs,direction="two-sided")
```

Numeric mean difference: **remove `success` in both pipelines**; use `calculate(stat="diff in means",order=...)`. Median difference: same valid null mechanism, `stat="diff in medians"`. Randomization tests flexibly support statistics whose analytic null distributions are inconvenient; the statistic must still answer the parameter/question.

Directions: `"greater"` = right tail; `"less"` = left; `"two-sided"` = both extremes. Choose sidedness before seeing the result.

## CI ↔ test; final traps

For the same parameter, assumptions, method, and matching two-sided levels: a (1−α) difference CI excluding null value 0 commonly corresponds to rejection at α. Do not infer this from overlap of separate group CIs, or assume exact equivalence between unrelated bootstrap/permutation constructions.

- Keep raw values, estimates, resamples, and statistics in separate tables/columns.
- `mean(x)`/`sd(x)` return NA with NA unless `na.rm=TRUE`; handling missing values does not fix missingness bias.
- Set seed once per simulation workflow; resetting inside each repetition can duplicate draws.
- Histogram x-axis: raw measurements vs sample statistics vs bootstrap/null statistics—label correctly. More repetitions smooth the picture; they do not narrow the true estimator uncertainty.