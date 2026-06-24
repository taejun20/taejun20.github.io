---
title: Understanding Power Analysis: Sample Size and Effect Size
date: 2026-06-19
tag: Statistics
---

Power analysis is the statistical framework behind two questions: "How many participants are needed?" (sample size analysis) and  "Given a fixed sample size, what is the smallest effect size that can be reliably detected?" (sensitivity analysis).

# 1. The Four Parameters

- **α (alpha)**: The probability of detecting an effect that isn't real. About false positive we tolerate. **Mostly set to .05.**
- **Power**: The probability of correctly detecting an effect when it exists. About false negative we tolerate. **Mostly set to .80,** meaning a 20% chance of missing a real effect.
- **Effect size**: How large the difference between conditions is.
- **n**: Sample size (number of participants).

These four are mathematically linked: fix any three and you can solve for the fourth. Since α = .05 and power = .80 are conventional standards that almost everyone uses, in practice it reduces to two questions:

- Given an expected effect size → how many participants are needed? **(sample size analysis)**
- Given a fixed n → what's the smallest effect that can be reliably detected? **(sensitivity analysis)**

## Effect Size

Effect size measures how big a difference is between conditions. In paired t-test, the standard measure of effect size is Cohen's d. In RM-ANOVA, it's Cohen's f. In Wilcoxon signed-rank test, it's rank-biserial correlation (r). In Friedman test, it's Kendall's W.

For Cohen's d:

| Effect Size | Cohen's d | Sample Size (n) | Meaning |
|-------------|-----------|----------------------|---------|
| Small | 0.2 | 199 | Subtle, hard to notice without measurement |
| Medium | 0.5 | 34 | Moderate, noticeable in practice |
| Large | 0.8 | 15 | Substantial, clearly visible difference |

```note
**Important:** effect size and p-value measure completely different things. A p-value reflects whether a difference is statistically significant. Effect size reflects how big the difference actually is. Again, p-value tells nothing about how big the difference is. Effect size does.

With a large enough n, even a trivially small effect (d = 0.01) will eventually produce p < .05, which is statistically significant but practically meaningless. This is why statisticians recommend reporting effect size alongside p-values.
```

# 2. Sample Size Analysis

Sample size analysis answers: **given an expected effect size, how many participants are needed?**

The challenge is estimating the expected effect size before collecting data (before running user study, in HCI). There are three approaches:

1. **Prior literature**: Find a published study with a similar task and design. Even if effect size is not reported directly, we can back-calculate it from reported statistics such as t, F, or Z values:


2. **Pilot study**: Run 5-10 participants and compute the effect size from that data. Note that effect sizes from small samples are noisy and tend to overestimate the true effect (need to be conservative, such as by using a slightly smaller value).

3. **Cohen's medium convention**: When no prior estimate of effect size is available, and no pilot study, default to d = 0.5 (which concludes to required sample size of 34 participants).

Below is an example Python script that runs a power analysis for paired t-test:

```python
from statsmodels.stats.power import TTestPower
import math

analysis = TTestPower()

d = 0.5  # expected Cohen's d (medium)
n = analysis.solve_power(effect_size=d, alpha=0.05, power=0.80, alternative='two-sided')
print(f"Required n: {math.ceil(n)}")
```

Output:

```
Required n: 34
```

The smaller the effect, the more participants are needed to reliably detect it. A small effect (d = 0.2) requires nearly 200 participants!

# 3. Sensitivity Analysis

Sensitivity analysis answers: **given a fixed n, what's the smallest effect that can be reliably detected?**

This is useful when sample size is already fixed. The minimum detectable effect size (MDES) can be computed to assess whether the study is adequately powered.

```python
from statsmodels.stats.power import TTestPower
import math

analysis = TTestPower()

n = 12
mdes = analysis.solve_power(nobs=n, alpha=0.05, power=0.80, alternative='two-sided')
print(f"Minimum Detectable Effect Size (MDES) for n={n}: d = {mdes:.2f}")
```

Output:

```
Minimum Detectable Effect Size (MDES) for n=12: d = 0.89
```

```note
Minimum Detectable Effect Size (MDES) for sample sizes (number of participants):

| n | MDES (Cohen's d) |
|---|------------------|
| 10 | 1.00 |
| 12 | 0.89 |
| 15 | 0.78 |
| 20 | 0.66 |
| 34 | 0.50 |

It is common that HCI papers use 10-20 participants for quick proof-of-concept testing of novel ideas. But this comes with a statistical cost. For example, n = 12 can only, statistically speaking, detect very large differences (d = 0.89). Moderate effects that many PoC systems may produce might not be detected at this sample size.
```

# 4. Responding to a Reviewer

A common reviewer comment in HCI: *"The number of participants (n = X) seems too small to support adequate statistical power. Was a power analysis conducted?"*

**If a power analysis was run beforehand,** cite it. State the effect size assumed, and the n it produced.

**If it wasn't** (or the required n couldn't be recruited), run a sensitivity analysis now and see where things stand.

### Case 1: Actual effect size ≥ MDES from sensitivity analysis (good)

Say the study had n = 12 (Minimum Detectable Effect Size = 0.89) and the data shows d = 1.1. This is an easy situation. A possible response:

```note
A post-hoc sensitivity analysis (α = .05, power = .80) showed that n = 12 is sufficient to detect effects of d ≥ 0.89. The observed effect size in our study was d = 1.1, indicating our sample was adequate for the effect size present.
```

### Case 2: Actual effect size < MDES from sensitivity analysis (tough spot)

If n = 12 (MDES = 0.89) but actual d = 0.5, the study was genuinely underpowered for the observed effect. Adequacy cannot be argued. Honest options:

- **(1) Acknowledge as a limitation**: "We acknowledge the study may be underpowered for medium effects, and the observed effect size from the study data suggests a potentially meaningful effect that warrants investigation in a larger follow-up study."
- **(2) Reframe as a pilot**: If statistics are not the main contribution of the paper, frame the study as preliminary evidence rather than a definitive test.
- **(3) Collect more data**: If the venue's revision timeline allows it, recruit additional participants and rerun.
- **(4) Avoid responding**: Leave it unaddressed in the rebuttal and move on. If the reviewer considers statistical power a critical flaw, the paper is likely rejected regardless. Just pray.
# References

- Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum.
- [statsmodels TTestPower](https://www.statsmodels.org/stable/generated/statsmodels.stats.power.TTestPower.html)

# Changelog
- Jun 19, 2026: Post published
