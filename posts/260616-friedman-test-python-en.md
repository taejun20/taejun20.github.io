---
title: Tutorial: Friedman Test with Python
date: 2026-06-16
tag: Statistics
---

This is a tutorial to run a Friedman test with Python. The Friedman test is used when the normality assumption is violated in at least one condition. If your data passes the normality test in all conditions, use [RM ANOVA](/posts?post=260615-one-way-rm-anova-python-en) instead (see 2-2 for normality check).

# 1. Organize Data

Use Google Spreadsheet to organize your data table (Before running any test, first look at the mean and SD for each condition to get an overall sense of the data).

![|50%](img/posts/260616-friedman-test-python/data-table.jpg)

Save this table as a CSV file (data.csv), and put it in the same folder as the Python script (main.py).

<a href="/files/260616-friedman-test-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Run Python Script

Let me first attach the full Python script here, and then explain each part step-by-step for those who need.

<a href="/files/260616-friedman-test-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
from itertools import combinations
from scipy.stats import shapiro, friedmanchisquare, wilcoxon
from statsmodels.stats.multitest import multipletests

# read csv (wide format)
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Perform normality test for each condition
for cond in conditions:
    stat, p_value = shapiro(df[cond].values)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# perform Friedman test
stat, p_value = friedmanchisquare(*[df[cond].values for cond in conditions])
df_val = len(conditions) - 1
print(f"Friedman Test \ndf: {df_val}, Statistic (chi-square): {stat:.4f}, P-value: {p_value:.6f}")
if p_value < 0.05:
    print("There is a statistically significant difference between conditions.")
else:
    print("No statistically significant difference between conditions.")

# post-hoc: Wilcoxon signed-rank test with Bonferroni correction
pairwise_p = []
pairwise_z = []
comparisons = list(combinations(range(len(conditions)), 2))

for i, j in comparisons:
    res = wilcoxon(df[conditions[i]].values, df[conditions[j]].values, method='approx')
    pairwise_p.append(res.pvalue)
    pairwise_z.append(res.zstatistic)

corrected_pvals = multipletests(pairwise_p, method='bonferroni')[1]

print("\nPost-hoc: Wilcoxon signed-rank test with Bonferroni correction:")
for (i, j), z, p_val in zip(comparisons, pairwise_z, corrected_pvals):
    print(f"{conditions[i]} vs {conditions[j]}: Z = {z:.4f}, Adjusted P-value = {p_val:.6f}")
```

### 1) Data Preparation

```python
# read csv (wide format)
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
```

`pd.read_csv` reads the CSV as wide format.

### 2) Normality Test

```python
for cond in conditions:
    stat, p_value = shapiro(df[cond].values)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

Before deciding on a test, check whether the data in each condition is normally distributed using the Shapiro-Wilk test. The null hypothesis is that the data is normally distributed, so p > 0.05 means you fail to reject it (i.e., normality is assumed).

Output:

```
ExpCond: Condition A 
Statistic: 0.5588, P-value: 0.0000
Data is not normally distributed (reject H0).

ExpCond: Condition B 
Statistic: 0.9177, P-value: 0.2676
Data is normally distributed (fail to reject H0).

ExpCond: Condition C 
Statistic: 0.9427, P-value: 0.5339
Data is normally distributed (fail to reject H0).
```

Condition A fails the normality assumption, so we use the Friedman test for the entire dataset instead of RM ANOVA.

### 3) Friedman Test

```python
stat, p_value = friedmanchisquare(*[df[cond].values for cond in conditions])
df_val = len(conditions) - 1
print(f"Friedman Test \ndf: {df_val}, Statistic (chi-square): {stat:.4f}, P-value: {p_value:.6f}")
if p_value < 0.05:
    print("There is a statistically significant difference between conditions.")
else:
    print("No statistically significant difference between conditions.")
```

Degrees of freedom (df) = number of conditions − 1.

Output:

```
Friedman Test 
df: 2, Statistic (chi-square): 18.1667, P-value: 0.000114
There is a statistically significant difference between conditions.
```

The Friedman test revealed a significant effect of condition, χ²(2) = 18.17, p < .0005.

### 4) Post-hoc Analysis

```python
pairwise_p = []
pairwise_z = []
comparisons = list(combinations(range(len(conditions)), 2))

for i, j in comparisons:
    res = wilcoxon(df[conditions[i]].values, df[conditions[j]].values, method='approx')
    pairwise_p.append(res.pvalue)
    pairwise_z.append(res.zstatistic)

corrected_pvals = multipletests(pairwise_p, method='bonferroni')[1]

print("\nPost-hoc: Wilcoxon signed-rank test with Bonferroni correction:")
for (i, j), z, p_val in zip(comparisons, pairwise_z, corrected_pvals):
    print(f"{conditions[i]} vs {conditions[j]}: Z = {z:.4f}, Adjusted P-value = {p_val:.6f}")
```

Since there is a significant main effect, run pairwise Wilcoxon signed-rank tests with Bonferroni correction to identify which pairs differ.

Output:

```
Post-hoc: Wilcoxon signed-rank test with Bonferroni correction:
Condition A vs Condition B: Z = -3.0594, Adjusted P-value = 0.006653
Condition A vs Condition C: Z = -3.0594, Adjusted P-value = 0.006653
Condition B vs Condition C: Z = -1.1767, Adjusted P-value = 0.717950
```

Post-hoc pairwise comparisons with Bonferroni correction showed significant differences between Condition A and Condition B (Z = -3.06, p < .01), and between Condition A and Condition C (Z = -3.06, p < .01).

```note
**Note on Bonferroni Correction:** Whether to apply Bonferroni correction to p-values is ultimately a judgment call. This is kind of a tricky point. Applying Bonferroni is the conservative choice and safe from reviewer pushback. Theoretically, if each comparison were a genuinely independent question, e.g., comparisons planned before data collection rather than exploratory post-hoc, correction would not be needed. A separate question that supports one separate claim does not technically require Bonferroni correction, but if the comparisons are presented together and the reader interprets them as a whole, applying correction is still the safer choice. The Friedman test itself tests one question, "do any conditions differ?", and the post-hoc comparisons are follow-ups to that single question. This is a strong counter-logic against skipping the correction. Let's make safer move.
```

# 3. Report Results

```note
**Writing for report:** A Friedman test revealed a significant effect of condition (χ²(2) = 18.17, p < .001). Post-hoc pairwise Wilcoxon signed-rank tests with Bonferroni correction showed significant differences between Condition A and Condition B (Z = -3.06, p < .01), and between Condition A and Condition C (Z = -3.06, p < .01).
```

*Side Note: I previously used [SPSS](/posts?post=200203-spss-repeated-measures) for the test but switched entirely to using Python, which I feel is more simpler and transparent (and it's even free!).*

# References

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [scipy.stats.friedmanchisquare](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.friedmanchisquare.html)
- [scipy.stats.wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)
- [statsmodels multipletests](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)


# Changelog
- Jun 16, 2026: Post published
