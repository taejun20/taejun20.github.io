---
title: Tutorial: Two-way Repeated-Measures ANOVA with Python
date: 2026-06-16
tag: Statistics
---

This is a tutorial to run a Two-way Repeated-Measures (Within-Subject) ANOVA with Python. Use this when you have two within-subject factors (= two independent variables). If the normality assumption is not satisfied, use [Aligned Rank Transform](/posts?post=210903-aligned-rank-transform-en) (see 2-2 for normality check).

# 1. Organize Data

Use Google Spreadsheet to organize your data table (Before running any test, first look at the mean and SD for each condition to get an overall sense of the data).

![|80%](img/posts/260616-two-way-rm-anova-python/data-table.jpg)

There are two independent variables A and B. A has two levels (A1, A2) and B has three levels (B1, B2, B3), in total consisting of six experimental conditions (A1B1, A1B2, A1B3, A2B1, A2B2, A2B3). In real use, update the column name as it suits more on your data.

Save the data table as a CSV file (data.csv), and put it in the same folder as the Python script (main.py).

<a href="/files/260616-two-way-rm-anova-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Run Python Script

Let me first attach the full Python script here, and then explain each part step-by-step for those who need.

<a href="/files/260616-two-way-rm-anova-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
df_long['FactorA'] = df_long['Condition'].str[:2]
df_long['FactorB'] = df_long['Condition'].str[2:]

# Perform normality test for each condition
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# perform two-way RM ANOVA
aov = pg.rm_anova(data=df_long, dv='value', within=['FactorA', 'FactorB'], subject=subject_col, detailed=True)
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc']].to_string(index=False))

# post-hoc: pairwise t-test with Bonferroni correction

# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant — main effects post-hoc ===")
print("\nPost-hoc FactorA:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within='FactorA', subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print("\nPost-hoc FactorB (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within='FactorB', subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))

# 2) when interaction effect IS significant:
#    can't average out — one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print("\nSimple effects: FactorA within each FactorB level:")
for b in sorted(df_long['FactorB'].unique()):
    subset = df_long[df_long['FactorB'] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within='FactorA', subject=subject_col, padjust='bonferroni')
    print(f"  FactorB = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print("\nSimple effects: FactorB within each FactorA level (Bonferroni):")
for a in sorted(df_long['FactorA'].unique()):
    subset = df_long[df_long['FactorA'] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within='FactorB', subject=subject_col, padjust='bonferroni')
    print(f"  FactorA = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

### 1) Data Preparation

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
df_long['FactorA'] = df_long['Condition'].str[:2]
df_long['FactorB'] = df_long['Condition'].str[2:]
```

`pd.read_csv` reads the CSV as wide format and `melt` reshapes it to long format. The two factors are then extracted from the condition name: the first two characters become FactorA and the remaining characters become FactorB.

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

Check normality for each condition using the Shapiro-Wilk test before running a parametric test. p > 0.05 means normality is assumed.

Output:

```
ExpCond: A1B1 
Statistic: 0.9489, P-value: 0.6208
Data is normally distributed (fail to reject H0).

ExpCond: A1B2 
Statistic: 0.9402, P-value: 0.5010
Data is normally distributed (fail to reject H0).

ExpCond: A1B3 
Statistic: 0.9185, P-value: 0.2738
Data is normally distributed (fail to reject H0).

ExpCond: A2B1 
Statistic: 0.9781, P-value: 0.9752
Data is normally distributed (fail to reject H0).

ExpCond: A2B2 
Statistic: 0.9823, P-value: 0.9912
Data is normally distributed (fail to reject H0).

ExpCond: A2B3 
Statistic: 0.9347, P-value: 0.4327
Data is normally distributed (fail to reject H0).
```

All conditions pass the normality assumption, so we proceed with two-way RM ANOVA.

### 3) Two-way Repeated-Measures ANOVA

```python
aov = pg.rm_anova(data=df_long, dv='value', within=['FactorA', 'FactorB'], subject=subject_col, detailed=True)
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc']].to_string(index=False))
```

Output:

```
          Source  ddof1  ddof2           F         p_unc
         FactorA      1     11   83.660621  1.789109e-06
         FactorB      2     22  285.201389  1.852941e-16
 FactorA * FactorB      2     22    3.019793  6.936843e-02
```

Both main effects are significant. The interaction effect (FactorA * FactorB) is not significant (p = .069), meaning the effect of Factor B does not significantly differ across levels of Factor A.

### 4) Post-hoc Analysis

**Case 1: interaction effect is NOT significant** — average over the other factor and compare main effects (1+3=4 comparisons).

Since the interaction is not significant (p = .069), we interpret the main effects separately and run pairwise comparisons for each factor.

Factor A has only two levels, so no correction is needed:

```python
# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant — main effects post-hoc ===")
print("\nPost-hoc FactorA:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within='FactorA', subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print("\nPost-hoc FactorB (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within='FactorB', subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

Output:

```
Post-hoc FactorA:
A     B     T          dof    p_unc
----  ----  ---------  -----  -----------
A1    A2    9.14662    11     1.78911e-06

Post-hoc FactorB (Bonferroni):
A     B     T           dof    p_unc         p_corr
----  ----  ----------  -----  ------------  ------------
B1    B2    -12.8856    11     5.577e-08     1.6731e-07
B1    B3    -19.8949    11     5.65494e-10   1.69648e-09
B2    B3    -14.0944    11     2.1911e-08    6.57329e-08
```

All pairwise comparisons for Factor B are significant after Bonferroni correction.

**Case 2: interaction effect IS significant** — can't average out, because one factor's effect depends on the level of the other. Fix one factor's level and compare the other (simple effects, 3+6=9 comparisons).

```python
# 2) when interaction effect IS significant:
#    can't average out — one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print("\nSimple effects: FactorA within each FactorB level:")
for b in sorted(df_long['FactorB'].unique()):
    subset = df_long[df_long['FactorB'] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within='FactorA', subject=subject_col, padjust='bonferroni')
    print(f"  FactorB = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print("\nSimple effects: FactorB within each FactorA level (Bonferroni):")
for a in sorted(df_long['FactorA'].unique()):
    subset = df_long[df_long['FactorA'] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within='FactorB', subject=subject_col, padjust='bonferroni')
    print(f"  FactorA = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

Output:

```
Simple effects: FactorA within each FactorB level:
  FactorB = B1:
A1   A2   3.058  11.000    0.011
  FactorB = B2:
A1   A2   3.927  11.000    0.002
  FactorB = B3:
A1   A2   6.810  11.000    0.000

Simple effects: FactorB within each FactorA level (Bonferroni):
  FactorA = A1:
B1   B2    -7.589  11.000    0.000     0.000
B1   B3   -17.228  11.000    0.000     0.000
B2   B3    -7.652  11.000    0.000     0.000
  FactorA = A2:
B1   B2   -6.221  11.000    0.000     0.000
B1   B3   -9.372  11.000    0.000     0.000
B2   B3   -7.931  11.000    0.000     0.000
```

```note
**Note on Bonferroni Correction:** Whether to apply Bonferroni correction to p-values is ultimately a judgment call. This is kind of a tricky point. Applying Bonferroni is the conservative choice and safe from reviewer pushback. Theoretically, if each comparison were a genuinely independent question, e.g., comparisons planned before data collection rather than exploratory post-hoc, correction would not be needed. A separate question that supports one separate claim does not technically require Bonferroni correction, but if the comparisons are presented together and the reader interprets them as a whole, applying correction is still the safer choice. The ANOVA itself tests one question, "do any conditions differ?", and the post-hoc comparisons are follow-ups to that single question. This is a strong counter-logic against skipping the correction. Let's make safer move.
```

# 3. Report Results

```note
**Writing for report:** A two-way repeated-measures ANOVA revealed a significant main effect of Factor A (F(1, 11) = 83.66, p < .001) and a significant main effect of Factor B (F(2, 22) = 285.20, p < .001). The interaction effect was not significant (F(2, 22) = 3.02, p = .069). Post-hoc pairwise comparisons showed that A1 was significantly slower than A2 (t(11) = 9.15, p < .001). For Factor B, all pairwise comparisons were significant after Bonferroni correction: B1 vs B2 (t(11) = -12.89, p < .001), B1 vs B3 (t(11) = -19.89, p < .001), and B2 vs B3 (t(11) = -14.09, p < .001).
```

*Side Note: I previously used [SPSS](/posts?post=200203-spss-repeated-measures) for the test but switched entirely to using Python, which I feel is more simpler and transparent (and it's even free!).*

# References

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [pingouin rm_anova](https://pingouin-stats.org/generated/pingouin.rm_anova.html)
- [pingouin pairwise_tests](https://pingouin-stats.org/generated/pingouin.pairwise_tests.html)


# Changelog
- Jun 16, 2026: Post published
