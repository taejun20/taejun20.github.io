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
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df = df.melt(id_vars=[subject_col], var_name='ExpCond', value_name='value')

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Sphericity Check Start
print("=== Sphericity Check ===")
aov = pg.rm_anova(data=df, dv='value', within='ExpCond', subject=subject_col, detailed=True)
F_val = aov['F'].values[0]
df_num = int(aov['DF'].values[0])
n_subjects = df[subject_col].nunique()
df_denom = (n_subjects - 1) * df_num
eps = aov['eps'].values[0]
p_unc = aov['p_unc'].values[0]
p_GG = stats.f.sf(F_val, df_num * eps, df_denom * eps)
eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
p_HF = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)

if len(conditions) <= 2:
    print("Sphericity: automatically satisfied (only 2 levels)")
    p_report, use_col = p_unc, 'p-unc'
else:
    spher_result = pg.sphericity(data=df, dv='value', within='ExpCond', subject=subject_col)
    W, p_spher = spher_result.W, spher_result.pval
    if p_spher > 0.05:
        p_report, use_col = p_unc, 'p-unc'
    elif eps < 0.75:
        p_report, use_col = p_GG, 'p-GG-corr'
    else:
        p_report, use_col = p_HF, 'p-HF-corr'
    p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
    eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
    print(f"Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}\n{p_cond} & {eps_cond} -> use {use_col}")

# One-way RM ANOVA Start
print("\n=== One-way RM ANOVA ===")
aov_effect = aov.iloc[[0]].copy()
aov_effect['df_denom'] = df_denom
aov_effect['p-GG-corr'] = p_GG
aov_effect['p-HF-corr'] = p_HF
p_col = 'p_unc' if use_col == 'p-unc' else use_col
print(aov_effect[['Source', 'DF', 'df_denom', 'F', p_col]].to_string(index=False, formatters={'F': '{:.6f}'.format, p_col: '{:.6f}'.format}))
print(f"\n→ p-value to report: {p_report:.6f} ({use_col})")

# Post-hoc Analysis Start
print("\n=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===")
pairwise_results = pg.pairwise_tests(dv='value', within='ExpCond', subject=subject_col, data=df, padjust='bonferroni')
print(pairwise_results[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

### 1) Data Preparation

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df = df.melt(id_vars=[subject_col], var_name='ExpCond', value_name='value')
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
=== Normality Test ===
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

All three conditions pass the normality assumption, so we proceed with RM ANOVA. If even one condition fails, the conservative choice is to use a non-parametric alternative ([Friedman's test](/posts?post=260616-friedman-test-python-en)) for the entire dataset.

### 3) Sphericity Check

```python
# run rm_anova first to extract eps needed for GG/HF correction calculations
aov = pg.rm_anova(data=df, dv='value', within='ExpCond', subject=subject_col, detailed=True)
F_val = aov['F'].values[0]
df_num = int(aov['DF'].values[0])
n_subjects = df[subject_col].nunique()
df_denom = (n_subjects - 1) * df_num
eps = aov['eps'].values[0]
p_unc = aov['p_unc'].values[0]
p_GG = stats.f.sf(F_val, df_num * eps, df_denom * eps)
eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
p_HF = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)

if len(conditions) <= 2:
    print("Sphericity: automatically satisfied (only 2 levels)")
    p_report, use_col = p_unc, 'p-unc'
else:
    spher_result = pg.sphericity(data=df, dv='value', within='ExpCond', subject=subject_col)
    W, p_spher = spher_result.W, spher_result.pval
    if p_spher > 0.05:
        p_report, use_col = p_unc, 'p-unc'
    elif eps < 0.75:
        p_report, use_col = p_GG, 'p-GG-corr'
    else:
        p_report, use_col = p_HF, 'p-HF-corr'
    p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
    eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
    print(f"Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}\n{p_cond} & {eps_cond} -> use {use_col}")
```

Output:

```
=== Sphericity Check ===
Sphericity (Mauchly's): W = 0.99, p-sphericity = 0.971, ε = 0.994
p-sphericity > 0.05 & ε ≥ 0.75 -> use p-unc
```

We run `pg.rm_anova()` first to extract `eps` (Greenhouse-Geisser epsilon), checking sphericity and the right p-value to proceed.

- `p-unc`: use when sphericity is satisfied (p-sphericity > 0.05), or when there are only 2 levels (sphericity is automatically satisfied)
- `p-GG-corr`: Greenhouse-Geisser correction, use when sphericity is violated (p-sphericity ≤ 0.05) and ε < 0.75
- `p-HF-corr`: Huynh-Feldt correction, use when sphericity is violated (p-sphericity ≤ 0.05) and ε ≥ 0.75

### 4) One-way Repeated-Measures ANOVA

```python
aov_effect = aov.iloc[[0]].copy()
aov_effect['df_denom'] = df_denom
aov_effect['p-GG-corr'] = p_GG
aov_effect['p-HF-corr'] = p_HF
p_col = 'p_unc' if use_col == 'p-unc' else use_col
print(aov_effect[['Source', 'DF', 'df_denom', 'F', p_col]].to_string(index=False, formatters={'F': '{:.6f}'.format, p_col: '{:.6f}'.format}))
print(f"\n→ p-value to report: {p_report:.6f} ({use_col})")
```

Output:

```
=== One-way RM ANOVA ===
 Source  DF  df_denom        F    p_unc
ExpCond   2        22 4.662527 0.020504

→ p-value to report: 0.020504 (p-unc)
```

A one-way repeated-measures ANOVA revealed a significant main effect of condition, F(2, 22) = 4.66, p < .05.

### 5) Post-hoc Analysis

```python
pairwise_results = pg.pairwise_tests(dv='value', within='ExpCond', subject=subject_col, data=df, padjust='bonferroni')
print(pairwise_results[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

Since the ANOVA is significant, run pairwise comparisons with Bonferroni correction to identify which pairs differ.

Output:

```
=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===
          A           B       T dof    p_unc   p_corr
Condition A Condition B -2.0841  11 0.061266 0.183797
Condition A Condition C -2.8835  11 0.014877 0.044632
Condition B Condition C -0.9698  11 0.352979 1.000000
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
- [pingouin rm_anova](https://pingouin-stats.org/generated/pingouin.rm_anova.html)
- [pingouin pairwise_tests](https://pingouin-stats.org/generated/pingouin.pairwise_tests.html)


# Changelog
- Jun 15, 2026: Post published
