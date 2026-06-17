---
title: Tutorial: Wilcoxon Signed-Rank Test with Python
date: 2026-06-17
tag: Statistics
---

This is a tutorial to run a Wilcoxon signed-rank test with Python. Use it when normality is not satisfied in at least one condition. If your data passes the normality test in all conditions, use a [paired t-test](/posts?post=260617-paired-t-test-python-en) instead (see 2-2 for normality check).

# 1. Organize Data

Use Google Spreadsheet to organize your data table (Before running any test, first look at the mean and SD for each condition to get an overall sense of the data).

![|40%](img/posts/260617-wilcoxon-signed-rank-python/data-table.jpg)

Save this table as a CSV file (data.csv), and put it in the same folder as the Python script (main.py).

<a href="/files/260617-wilcoxon-signed-rank-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Run Python Script

Let me first attach the full Python script here, and then explain each part.

<a href="/files/260617-wilcoxon-signed-rank-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
from scipy.stats import shapiro, wilcoxon

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Wilcoxon Signed-Rank Test Start
print("=== Wilcoxon Signed-Rank Test ===")
result = wilcoxon(df[conditions[0]], df[conditions[1]], method='approx')
print(f"Z = {result.zstatistic:.4f}, P-value = {result.pvalue:.6f}")
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
    stat, p_value = shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

Before deciding on a test, check whether the data in each condition is normally distributed using the Shapiro-Wilk test. The null hypothesis is that the data is normally distributed, so p > 0.05 means you fail to reject it (i.e., normality is assumed).

Output:

```
=== Normality Test ===
ExpCond: Condition A 
Statistic: 0.5341, P-value: 0.0000
Data is not normally distributed (reject H0).

ExpCond: Condition B 
Statistic: 0.8995, P-value: 0.1564
Data is normally distributed (fail to reject H0).
```

Condition A fails the normality assumption, so we use the Wilcoxon signed-rank test instead of a paired t-test. If both conditions pass, use a [paired t-test](/posts?post=260617-paired-t-test-python-en) instead.

### 3) Wilcoxon Signed-Rank Test

```python
result = wilcoxon(df[conditions[0]], df[conditions[1]], method='approx')
print(f"Z = {result.zstatistic:.4f}, P-value = {result.pvalue:.6f}")
```

`method='approx'` uses a normal approximation to compute the z-statistic, which is required to report a Z value.

Output:

```
=== Wilcoxon Signed-Rank Test ===
Z = -2.3238, P-value = 0.020137
```

The Wilcoxon signed-rank test revealed a significant difference between conditions (Z = -2.32, p < .05).

# 3. Report Results

```note
**Writing for report:** A Wilcoxon signed-rank test revealed a significant difference between Condition A and Condition B (Z = -2.32, p < .05).
```

*Side Note: I previously used [SPSS](/posts?post=200203-spss-repeated-measures) for the test but switched entirely to using Python, which I feel is more simpler and transparent (and it's even free!).*

# References

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [scipy.stats.wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)


# Changelog
- Jun 17, 2026: Post published
