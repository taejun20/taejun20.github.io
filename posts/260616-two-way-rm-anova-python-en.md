---
title: Tutorial: Two-way Repeated-Measures ANOVA with Python
date: 2026-06-16
tag: Statistics
---

This is a tutorial to run a Two-way Repeated-Measures (Within-Subject) ANOVA with Python. Use this when you have two within-subject factors (= two independent variables). If the normality assumption is not satisfied, use [Aligned Rank Transform](/posts?post=210903-aligned-rank-transform-en) (see 2-2 for normality check).

```note
**Library limitation:** The `pingouin` library used in this tutorial only supports up to two within-subject factors. For three-way or four-way RM ANOVA, use R (`afex` or `ez` package) instead.
```

# 1. Organize Data

Use Google Spreadsheet to organize your data table (Before running any test, first look at the mean and SD for each condition to get an overall sense of the data).

![|80%](img/posts/260616-two-way-rm-anova-python/data-table.jpg)

There are two independent variables A and B. A has two levels (A1, A2) and B has three levels (B1, B2, B3), in total consisting of six experimental conditions (A1_B1, A1_B2, A1_B3, A2_B1, A2_B2, A2_B3). In real use, update the column names to match your own factors and levels. **Use underscores to separate the factor levels in each condition. The script splits on `_` to automatically detect and extract the factors.**

Examples:
- type (Controller, Pinch) x power (5, 10): `Controller_5`, `Pinch_5`, `Controller_10`, `Pinch_10`
- device (Phone, Watch) x size (Small, Large): `Phone_Small`, `Watch_Small`, `Phone_Large`, `Watch_Large`
- difficulty (Easy, Hard) x speed (Slow, Fast): `Easy_Slow`, `Easy_Fast`, `Hard_Slow`, `Hard_Fast`

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
factor_cols = [f'Factor{chr(65+i)}' for i in range(len(conditions[0].split('_')))]
for i, col in enumerate(factor_cols):
    df_long[col] = df_long['Condition'].str.split('_').str[i]

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Sphericity Check Start
print("=== Sphericity Check ===")
aov = pg.rm_anova(data=df_long, dv='value', within=factor_cols, subject=subject_col, detailed=True)
n_subjects = df_long[subject_col].nunique()

use_cols = {}
p_reports = {}

for idx, row in aov.iterrows():
    source = row['Source']
    F_val = row['F']
    df_num = int(row['ddof1'])
    df_denom = int(row['ddof2'])
    eps = row['eps']
    p_unc_val = row['p_unc']
    p_GG_val = row['p_GG_corr']
    eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
    p_HF_val = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)
    aov.at[idx, 'p_HF_corr'] = p_HF_val

    if df_num == 1:
        print(f"[{source}] sphericity automatically satisfied (df = 1) -> use p_unc")
        use_cols[source] = 'p_unc'
        p_reports[source] = p_unc_val
    else:
        within = factor_cols if '*' in source else source
        spher_result = pg.sphericity(data=df_long, dv='value', within=within, subject=subject_col)
        W, p_spher = spher_result.W, spher_result.pval
        if p_spher > 0.05:
            use_cols[source] = 'p_unc'
            p_reports[source] = p_unc_val
        elif eps < 0.75:
            use_cols[source] = 'p_GG_corr'
            p_reports[source] = p_GG_val
        else:
            use_cols[source] = 'p_HF_corr'
            p_reports[source] = p_HF_val
        p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
        eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
        print(f"[{source}] Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}")
        print(f"{p_cond} & {eps_cond} -> use {use_cols[source]}")

# Two-way RM ANOVA Start
print("\n=== Two-way RM ANOVA ===")
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc', 'p_GG_corr', 'p_HF_corr']].to_string(index=False))
print("\n→ p-value to report:")
for source, col in use_cols.items():
    print(f"  [{source}] {p_reports[source]:.6f} ({col})")

# Post-hoc Analysis Start
print("\n=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===")

# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant: main effects post-hoc ===")
print(f"\nPost-hoc {factor_cols[0]}:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print(f"\nPost-hoc {factor_cols[1]} (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))

# 2) when interaction effect IS significant:
#    can't average out; one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print(f"\nSimple effects: {factor_cols[0]} within each {factor_cols[1]} level:")
for b in sorted(df_long[factor_cols[1]].unique()):
    subset = df_long[df_long[factor_cols[1]] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[1]} = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print(f"\nSimple effects: {factor_cols[1]} within each {factor_cols[0]} level (Bonferroni):")
for a in sorted(df_long[factor_cols[0]].unique()):
    subset = df_long[df_long[factor_cols[0]] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[0]} = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

### 1) Data Preparation

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
factor_cols = [f'Factor{chr(65+i)}' for i in range(len(conditions[0].split('_')))]
for i, col in enumerate(factor_cols):
    df_long[col] = df_long['Condition'].str.split('_').str[i]
```

`pd.read_csv` reads the CSV as wide format and `melt` reshapes it to long format.

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
=== Normality Test ===
ExpCond: A1_B1 
Statistic: 0.9489, P-value: 0.6208
Data is normally distributed (fail to reject H0).

ExpCond: A1_B2 
Statistic: 0.9402, P-value: 0.5010
Data is normally distributed (fail to reject H0).

ExpCond: A1_B3 
Statistic: 0.9185, P-value: 0.2738
Data is normally distributed (fail to reject H0).

ExpCond: A2_B1 
Statistic: 0.9781, P-value: 0.9752
Data is normally distributed (fail to reject H0).

ExpCond: A2_B2 
Statistic: 0.9823, P-value: 0.9912
Data is normally distributed (fail to reject H0).

ExpCond: A2_B3 
Statistic: 0.9347, P-value: 0.4327
Data is normally distributed (fail to reject H0).
```

All conditions pass the normality assumption, so we proceed with two-way RM ANOVA. If even one condition fails, use [Aligned Rank Transform](/posts?post=210903-aligned-rank-transform-en) for the entire dataset.

### 3) Sphericity Check

```python
aov = pg.rm_anova(data=df_long, dv='value', within=factor_cols, subject=subject_col, detailed=True)
n_subjects = df_long[subject_col].nunique()

use_cols = {}
p_reports = {}

for idx, row in aov.iterrows():
    source = row['Source']
    F_val = row['F']
    df_num = int(row['ddof1'])
    df_denom = int(row['ddof2'])
    eps = row['eps']
    p_unc_val = row['p_unc']
    p_GG_val = row['p_GG_corr']
    eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
    p_HF_val = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)
    aov.at[idx, 'p_HF_corr'] = p_HF_val

    if df_num == 1:
        print(f"[{source}] sphericity automatically satisfied (df = 1) -> use p_unc")
        use_cols[source] = 'p_unc'
        p_reports[source] = p_unc_val
    else:
        within = factor_cols if '*' in source else source
        spher_result = pg.sphericity(data=df_long, dv='value', within=within, subject=subject_col)
        W, p_spher = spher_result.W, spher_result.pval
        if p_spher > 0.05:
            use_cols[source] = 'p_unc'
            p_reports[source] = p_unc_val
        elif eps < 0.75:
            use_cols[source] = 'p_GG_corr'
            p_reports[source] = p_GG_val
        else:
            use_cols[source] = 'p_HF_corr'
            p_reports[source] = p_HF_val
        p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
        eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
        print(f"[{source}] Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}")
        print(f"{p_cond} & {eps_cond} -> use {use_cols[source]}")
```

Output:

```
=== Sphericity Check ===
[FactorA] sphericity automatically satisfied (df = 1) -> use p_unc
[FactorB] Sphericity (Mauchly's): W = 0.80, p-sphericity = 0.338, ε = 0.837
p-sphericity > 0.05 & ε ≥ 0.75 -> use p_unc
[FactorA * FactorB] Sphericity (Mauchly's): W = 0.99, p-sphericity = 0.937, ε = 0.987
p-sphericity > 0.05 & ε ≥ 0.75 -> use p_unc
```

Sphericity is checked separately for each effect.

- `p_unc`: use when sphericity is satisfied (p-sphericity > 0.05), or automatically met when the factor has only 2 levels
- `p_GG_corr`: Greenhouse-Geisser correction, use when sphericity is violated (p-sphericity ≤ 0.05) and ε < 0.75
- `p_HF_corr`: Huynh-Feldt correction, use when sphericity is violated (p-sphericity ≤ 0.05) and ε ≥ 0.75

### 4) Two-way Repeated-Measures ANOVA

```python
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc', 'p_GG_corr', 'p_HF_corr']].to_string(index=False))
print("\n→ p-value to report:")
for source, col in use_cols.items():
    print(f"  [{source}] {p_reports[source]:.6f} ({col})")
```

Output:

```
=== Two-way RM ANOVA ===
           Source  ddof1  ddof2          F        p_unc    p_GG_corr    p_HF_corr
          FactorA      1     11  83.660621 1.789109e-06 1.789109e-06 1.789109e-06
          FactorB      2     22 285.201389 1.852941e-16 4.233350e-14 5.126377e-16
FactorA * FactorB      2     22   3.019793 6.936843e-02 7.019957e-02 6.936843e-02

→ p-value to report:
  [FactorA] 0.000002 (p_unc)
  [FactorB] 0.000000 (p_unc)
  [FactorA * FactorB] 0.069368 (p_unc)
```

Both main effects are significant. The interaction effect (FactorA * FactorB) is not significant (p = .069). For understanding interaction effects, see [this post](/posts?post=200903-interaction-effects-anova-en).

### 5) Post-hoc Analysis

**Case 1: interaction effect is NOT significant.** Average over the other factor and compare main effects. Since the interaction is not significant, we interpret the main effects separately and run pairwise comparisons for each factor.

Factor A has only two levels, so no correction is needed. Factor B has three levels, so Bonferroni correction is applied across the 3 pairwise comparisons:

```python
# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant: main effects post-hoc ===")
print(f"\nPost-hoc {factor_cols[0]}:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print(f"\nPost-hoc {factor_cols[1]} (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

Output:

```
=== Case 1: Interaction NOT significant: main effects post-hoc ===

Post-hoc FactorA:
 A  B      T dof    p_unc
A1 A2 9.1466  11 0.000002

Post-hoc FactorB (Bonferroni):
 A  B        T dof    p_unc   p_corr
B1 B2 -12.8856  11 0.000000 0.000000
B1 B3 -19.8949  11 0.000000 0.000000
B2 B3 -14.0944  11 0.000000 0.000000
```

All pairwise comparisons for Factor B are significant after Bonferroni correction.

**Case 2: interaction effect is significant.** Can't average out, because one factor's effect depends on the level of the other. Fix one factor's level and compare the other (simple effects).

```python
# 2) when interaction effect IS significant:
#    can't average out; one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print(f"\nSimple effects: {factor_cols[0]} within each {factor_cols[1]} level:")
for b in sorted(df_long[factor_cols[1]].unique()):
    subset = df_long[df_long[factor_cols[1]] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[1]} = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print(f"\nSimple effects: {factor_cols[1]} within each {factor_cols[0]} level (Bonferroni):")
for a in sorted(df_long[factor_cols[0]].unique()):
    subset = df_long[df_long[factor_cols[0]] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[0]} = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

Output:

```
=== Case 2: Interaction IS significant — simple effects ===

Simple effects: FactorA within each FactorB level:
  FactorB = B1:
 A  B      T dof    p_unc
A1 A2 3.0580  11 0.010890
  FactorB = B2:
 A  B      T dof    p_unc
A1 A2 3.9275  11 0.002362
  FactorB = B3:
 A  B      T dof    p_unc
A1 A2 6.8099  11 0.000029

Simple effects: FactorB within each FactorA level (Bonferroni):
  FactorA = A1:
 A  B        T dof    p_unc   p_corr
B1 B2  -7.5889  11 0.000011 0.000032
B1 B3 -17.2285  11 0.000000 0.000000
B2 B3  -7.6518  11 0.000010 0.000030
  FactorA = A2:
 A  B       T dof    p_unc   p_corr
B1 B2 -6.2209  11 0.000065 0.000196
B1 B3 -9.3722  11 0.000001 0.000004
B2 B3 -7.9306  11 0.000007 0.000021
```

```note
**Note on Bonferroni Correction:** Whether to apply Bonferroni correction to p-values is ultimately a judgment call. This is kind of a tricky point. Applying Bonferroni is the conservative choice and safe from reviewer pushback. Theoretically, if each comparison were a genuinely independent question, e.g., comparisons planned before data collection rather than exploratory post-hoc, correction would not be needed. A separate question that supports one separate claim does not technically require Bonferroni correction, but if the comparisons are presented together and the reader interprets them as a whole, applying correction is still the safer choice. The ANOVA itself tests one question, "do any conditions differ?", and the post-hoc comparisons are follow-ups to that single question. This is a strong counter-logic against skipping the correction. Let's make safer move.
```

# 3. Report Results

While we showed both Case 1 and Case 2, in the example data case, Case 1 applies since the interaction effect was not significant. The writing below is based on Case 1 analysis:

```note
**Writing for report:** A two-way repeated-measures ANOVA revealed a significant main effect of Factor A (F(1, 11) = 83.66, p < .001) and a significant main effect of Factor B (F(2, 22) = 285.20, p < .001). The interaction effect was not significant. Post-hoc pairwise comparisons showed that A1 was significantly slower than A2 (t = 9.15, p < .001). For Factor B, all pairwise comparisons were significant after Bonferroni correction: B1 vs B2 (t = -12.89, p < .001), B1 vs B3 (t = -19.89, p < .001), and B2 vs B3 (t = -14.09, p < .001).
```

*Side Note: I previously used [SPSS](/posts?post=200420-spss-two-way-anova-en) for the test but switched entirely to using Python, which I feel is more simpler and transparent (and it's even free!).*

# References

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [pingouin rm_anova](https://pingouin-stats.org/generated/pingouin.rm_anova.html)
- [pingouin sphericity](https://pingouin-stats.org/generated/pingouin.sphericity.html)
- [pingouin pairwise_tests](https://pingouin-stats.org/generated/pingouin.pairwise_tests.html)


# Changelog
- Jun 16, 2026: Post published
