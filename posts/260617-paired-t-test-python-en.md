---
title: Tutorial: Paired T-Test with Python
date: 2026-06-17
tag: Statistics
---

This is a tutorial to run a paired t-test with Python. A paired t-test compares two conditions measured on the same subjects (within-subject design with 2 conditions). If normality is not satisfied in at least one condition, use a [Wilcoxon signed-rank test](/posts?post=260617-wilcoxon-signed-rank-python-en) instead (see 2-2 for normality check).

# 1. Organize Data

Use Google Spreadsheet to organize your data table (Before running any test, first look at the mean and SD for each condition to get an overall sense of the data).

![|40%](img/posts/260617-paired-t-test-python/data-table.jpg)

Save this table as a CSV file (data.csv), and put it in the same folder as the Python script (main.py).

<a href="/files/260617-paired-t-test-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Run Python Script

Let me first attach the full Python script here, and then explain each part.

<a href="/files/260617-paired-t-test-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
import pingouin as pg
from scipy import stats

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Paired T-Test Start
print("=== Paired T-Test ===")
result = pg.ttest(df[conditions[0]], df[conditions[1]], paired=True)
print(result[['T', 'dof', 'p_val', 'cohen_d']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_val': '{:.6f}'.format, 'cohen_d': '{:.4f}'.format}))
```

### 1) Data Preparation

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
```

`pd.read_csv` reads the CSV as wide format.

### 2) Normality Test

```python
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

Before running a parametric test like the paired t-test, check whether the data in each condition is normally distributed using the Shapiro-Wilk test. The null hypothesis is that the data is normally distributed, so p > 0.05 means you fail to reject it (i.e., normality is assumed).

Output:

```
=== Normality Test ===
ExpCond: Condition A 
Statistic: 0.9762, P-value: 0.9637
Data is normally distributed (fail to reject H0).

ExpCond: Condition B 
Statistic: 0.9561, P-value: 0.7264
Data is normally distributed (fail to reject H0).
```

Both conditions pass the normality assumption, so we proceed with the paired t-test. If even one condition fails, the conservative choice is to use a [Wilcoxon signed-rank test](/posts?post=260617-wilcoxon-signed-rank-python-en) for the entire dataset.

### 3) Paired T-Test

```python
result = pg.ttest(df[conditions[0]], df[conditions[1]], paired=True)
print(result[['T', 'dof', 'p_val', 'cohen_d']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_val': '{:.6f}'.format, 'cohen_d': '{:.4f}'.format}))
```

`pg.ttest()` with `paired=True` runs a paired t-test between the two conditions. We print the t-statistic, degrees of freedom (dof = n - 1), p-value, and Cohen's d as an effect size measure.

Output:

```
=== Paired T-Test ===
      T dof    p_val cohen_d
-6.9663  11 0.000024  0.9860
```

The paired t-test revealed a significant difference between conditions, t(11) = -6.97, p < .001, d = 0.99.

# 3. Report Results

```note
**Writing for report:** A paired t-test revealed a significant difference between Condition A and Condition B (t(11) = -6.97, p < .001).
```

*Side Note: I previously used [SPSS](/posts?post=200203-spss-repeated-measures) for the test but switched entirely to using Python, which I feel is more simpler and transparent (and it's even free!).*

# References

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [pingouin ttest](https://pingouin-stats.org/generated/pingouin.ttest.html)


# Changelog
- Jun 17, 2026: Post published
