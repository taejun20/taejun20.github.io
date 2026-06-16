---
title: Tutorial: One-way Repeated-Measures ANOVA with Python
date: 2026-06-15
tag: Statistics
---

This is a tutorial to run a Repeated Measure (Within-Subject) ANOVA with Python. If normality assumption is not satisfied in at least one condition, use [Friedman Test](/posts?post=260616-friedman-test-python-en) instead (see 2-2 for normality check).

# 1. Organize Data

Use Google Spreadsheet to organize your data table (Before running any test, first look at the mean and SD for each condition to get an overall sense of the data).

![|50%](img/posts/260615-one-way-rm-anova-python/data-table.jpg)

Save this table as a CSV file (data.csv), and put it in the same folder as the Python script (main.py).

<a href="/files/260615-one-way-rm-anova-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Run Python Script

Let me first attach the full Python script here, and then explain each part step-by-step for those who need.

<a href="/files/260615-one-way-rm-anova-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
df = df.melt(id_vars=[df.columns[0]], var_name='ExpCond', value_name='value')

# Perform normality test for each condition
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# perform RM-ANOVA: statsmodels AnovaRM
testingMeasure = 'value'
anovaRM = AnovaRM(data=df, depvar=testingMeasure, subject='Participant', within=['ExpCond'])
res = anovaRM.fit()
print(res)

# post-hoc: pairwise t-test with Bonferroni correction
pairwise_results = pg.pairwise_ttests(dv=testingMeasure, within='ExpCond', subject='Participant', data=df, padjust='bonferroni')
pg.print_table(pairwise_results)
```

### 1) Data Preparation

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
df = df.melt(id_vars=[df.columns[0]], var_name='ExpCond', value_name='value')
```

`pd.read_csv` reads the CSV as wide format and `melt` reshapes it to long format, which is required by the ANOVA functions.

### 2) Normality Test

```python
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

Before running a parametric test like RM ANOVA, check whether the data in each condition is normally distributed using the Shapiro-Wilk test. The null hypothesis is that the data is normally distributed, so p > 0.05 means you fail to reject it (i.e., normality is assumed).

Output:

```
ExpCond: Condition A 
Statistic: 0.9532, P-value: 0.6846
Data is normally distributed (fail to reject H0).

ExpCond: Condition B 
Statistic: 0.9177, P-value: 0.2676
Data is normally distributed (fail to reject H0).

ExpCond: Condition C 
Statistic: 0.9427, P-value: 0.5339
Data is normally distributed (fail to reject H0).
```

All three conditions pass the normality assumption, so we proceed with RM ANOVA. If even one condition fails, the conservative choice is to use a non-parametric alternative (Friedman's test) for the entire dataset.

### 3) One-way Repeated-Measures ANOVA

```python
testingMeasure = 'value'
anovaRM = AnovaRM(data=df, depvar=testingMeasure, subject='Participant', within=['ExpCond'])
res = anovaRM.fit()
print(res)
```

Output:

```
                Anova
=====================================
        F Value Num DF  Den DF Pr > F
-------------------------------------
ExpCond  4.6625 2.0000 22.0000 0.0205
=====================================
```

A one-way repeated-measures ANOVA revealed a significant main effect of condition, F(2, 22) = 4.66, p < .05.

### 4) Post-hoc Analysis

```python
pairwise_results = pg.pairwise_ttests(dv=testingMeasure, within='ExpCond', subject='Participant', data=df, padjust='bonferroni')
pg.print_table(pairwise_results)
```

Since the ANOVA is significant, run pairwise comparisons with Bonferroni correction to identify which pairs differ.

Output:

```
Contrast    A            B            Paired    Parametric         T     dof  alternative      p_unc    p_corr  p_adjust      BF10    hedges
----------  -----------  -----------  --------  ------------  ------  ------  -------------  -------  --------  ----------  ------  --------
ExpCond     Condition A  Condition B  True      True          -2.084  11.000  two-sided        0.061     0.184  bonferroni   1.421    -0.800
ExpCond     Condition A  Condition C  True      True          -2.884  11.000  two-sided        0.015     0.045  bonferroni   4.294    -1.266
ExpCond     Condition B  Condition C  True      True          -0.970  11.000  two-sided        0.353     1.000  bonferroni   0.426    -0.440
```

Post-hoc pairwise comparisons with Bonferroni correction showed a significant difference between Condition A and Condition C (t = -2.88, p < .05).

```note
**Note on Bonferroni Correction:** Whether to apply Bonferroni correction to p-values is ultimately a judgment call. This is kind of a tricky point. Applying Bonferroni is the conservative choice and safe from reviewer pushback. Theoretically, if each comparison were a genuinely independent question, e.g., comparisons planned before data collection rather than exploratory post-hoc, correction would not be needed. A separate question that supports one separate claim does not technically require Bonferroni correction, but if the comparisons are presented together and the reader interprets them as a whole, applying correction is still the safer choice. The ANOVA itself tests one question, "do any conditions differ?", and the post-hoc comparisons are follow-ups to that single question. This is a strong counter-logic against skipping the correction. Let's make safer move.
```

# 3. Report Results

```note
**Writing for report:** A one-way repeated-measures ANOVA revealed a significant main effect of condition (F(2, 22) = 4.66, p < .05). Post-hoc pairwise comparisons with Bonferroni correction showed a significant difference between Condition A and Condition C (t = -2.88, p < .05).
```

*Side Note: I previously used [SPSS](/posts?post=200203-spss-repeated-measures) for the test but switched entirely to using Python, which I feel is more simpler and transparent (and it's even free!).*

# References

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [statsmodels AnovaRM](https://www.statsmodels.org/stable/generated/statsmodels.stats.anova.AnovaRM.html)
- [pingouin pairwise_tests](https://pingouin-stats.org/generated/pingouin.pairwise_tests.html)


# Changelog
- Jun 15, 2026: Post published
