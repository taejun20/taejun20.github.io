---
title: Tutorial: Linear Mixed Model with Python - Component Contribution Analysis
date: 2026-06-18
tag: Statistics
---

This is a tutorial to fit a Linear Mixed Model (LMM) for evaluating modular systems with repeated observations from the same participant (or other grouping factor). The mixed model estimates the contribution of each modular component while accounting for variability across participants. 

Let say there is a modular system with component A. There are also components B, C, and D that can be combined with A (A+B, A+C, A+C+D, ...), so there can be many combinations of the final system. We want to know whether each component contributes a statistically significant effect on the performance. Specifically, we do this by fitting a linear mixed model and running a Likelihood Ratio Test (LRT).

```note
**Note:** This post is not about pairwise comparison of final conditions, which can be done with a [paired t-test](http://localhost:3000/posts?post=260617-paired-t-test-python-en) or [Wilcoxon signed-rank test](http://localhost:3000/posts?post=260617-wilcoxon-signed-rank-python-en).
```
# 1. Organize Data

Use Google Spreadsheet to organize your data table (Before running any test, first look at the mean and SD for each condition to get an overall sense of the data).

![|100%](img/posts/260618-lmm-lrt-python/data-table.jpg)

Each row is a participant and each column is a condition. Each condition name represents a combination of modules separated by `+`. In real use, replace the module names to match your own components.

Examples:
- RGB camera, thermal, depth: `RGB`, `RGB+Thermal`, `RGB+Depth`, `RGB+Thermal+Depth`, `Thermal`, `Thermal+Depth`, `Depth`
- face, pose, gaze: `Face`, `Face+Pose`, `Face+Gaze`, `Face+Pose+Gaze`, `Pose`, `Pose+Gaze`, `Gaze`

Save this table as a CSV file (data.csv), and put it in the same folder as the Python script (main.py).

<a href="/files/260618-lmm-lrt-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Run Python Script

Let me first attach the full Python script here, and then explain each part.

<a href="/files/260618-lmm-lrt-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')

all_components = sorted(set(comp for cond in conditions for comp in cond.split('+')))
varying_components = [c for c in all_components if not all(c in cond.split('+') for cond in conditions)]
for comp in all_components:
    df_long[comp] = df_long['Condition'].apply(lambda x: 1 if comp in x.split('+') else 0)

# LMM + LRT Start
print("=== LMM + LRT ===")
full_model = smf.mixedlm("value ~ " + " + ".join(varying_components), data=df_long, groups=df_long[subject_col]).fit(reml=False)
for comp in varying_components:
    others = [c for c in varying_components if c != comp]
    reduced_model = smf.mixedlm("value ~ " + " + ".join(others), data=df_long, groups=df_long[subject_col]).fit(reml=False)
    chi2 = 2 * (full_model.llf - reduced_model.llf)
    p = stats.chi2.sf(chi2, df=1)
    print(f"Component {comp}: χ²(1) = {chi2:.2f}, p = {p:.4f}")
```

### 1) Data Preparation

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
```

`pd.read_csv` reads the CSV as wide format and `melt` reshapes it to long format, which is required by `mixedlm`.

```python
all_components = sorted(set(comp for cond in conditions for comp in cond.split('+')))
varying_components = [c for c in all_components if not all(c in cond.split('+') for cond in conditions)]
for comp in all_components:
    df_long[comp] = df_long['Condition'].apply(lambda x: 1 if comp in x.split('+') else 0)
```

Then it adds one binary column per component to the long-format dataframe, where 1 means the component is present in that condition and 0 means it is absent. `varying_components` filters out any component that appears in every condition (if a component is always present, there is no condition without it to compare against). Only varying components are used as fixed-effect predictors in the model.

```note
df_long after encoding (showing only p1):

| Participant | Condition | value | A | B | C | D |
|---|---|---|---|---|---|---|
| p1 | A | 2.269 | 1 | 0 | 0 | 0 |
| p1 | A+B | 2.905 | 1 | 1 | 0 | 0 |
| p1 | A+C | 2.394 | 1 | 0 | 1 | 0 |
| p1 | A+D | 1.881 | 1 | 0 | 0 | 1 |
| p1 | A+C+D | 2.204 | 1 | 0 | 1 | 1 |
| p1 | C | 1.896 | 0 | 0 | 1 | 0 |
| p1 | C+D | 2.741 | 0 | 0 | 1 | 1 |
| p1 | D | 2.301 | 0 | 0 | 0 | 1 |
```

### 2) LMM + Likelihood Ratio Test (LRT)

The LRT compares a full model (with all varying components) against a reduced model (with one component dropped). The difference in model fit is quantified as a chi-square statistic.

```python
full_model = smf.mixedlm("value ~ " + " + ".join(varying_components), data=df_long, groups=df_long[subject_col]).fit(reml=False)
for comp in varying_components:
    others = [c for c in varying_components if c != comp]
    reduced_model = smf.mixedlm("value ~ " + " + ".join(others), data=df_long, groups=df_long[subject_col]).fit(reml=False)
    chi2 = 2 * (full_model.llf - reduced_model.llf)
    p = stats.chi2.sf(chi2, df=1)
    print(f"Component {comp}: χ²(1) = {chi2:.2f}, p = {p:.4f}")
```

For each varying component, we fit a reduced model that excludes it and compute: χ²(1) = 2 × (full log-likelihood - reduced log-likelihood). A large chi-square means the component improves model fit significantly, which means the component has a significant effect on the outcome.


Output:

```
=== LMM + LRT ===
Component A: χ²(1) = 7.07, p = 0.0078
Component B: χ²(1) = 0.07, p = 0.7920
Component C: χ²(1) = 0.01, p = 0.9319
Component D: χ²(1) = 8.79, p = 0.0030
```

Components A and D contribute significantly to the outcome (A: p < .01; D: p < .005). Components B and C do not.

# 3. Report Results

```note
**Writing for report:** A linear mixed model with likelihood ratio tests revealed that components A (χ²(1) = 7.07, p < .01) and D (χ²(1) = 8.79, p < .005) significantly contributed to the outcome. Components B and C did not reach significance.
```


# Note: Linear Mixed Model for Other Use

While this post used LMM for component contribution analysis, LMM + LRT can also replace paired t-test and RM-ANOVA for standard comparisons. In fact, paired t-test and RM-ANOVA are special cases of LMM.

Two situations that LMM can cover but paired t-test and RM-ANOVA cannot. **(1) LMM handles missing/unbalanced data** (i.e., when some participants are missing data for certain conditions), while paired t-test and RM-ANOVA can't handle. **(2) LMM supports continuous covariates such as age as control variables** (e.g., if older participants tend to score higher regardless of condition, including age lets the model account for that, giving a cleaner estimate of the condition effect). This also means you can examine whether age itself has a significant effect on the outcome.

That said, for the repeated-measures user studies that are most common in HCI research, data is almost certainly complete and balanced, so [paired t-test](https://taejunkim.com/posts?post=260617-paired-t-test-python-en) or [one-way RM-ANOVA](https://taejunkim.com/posts?post=260615-one-way-rm-anova-python-en) works fine most of the time. If you need to handle unbalanced data or control for a continuous covariate like age, use LMM + LRT instead.

# References

- [statsmodels MixedLM](https://www.statsmodels.org/stable/generated/statsmodels.regression.mixed_linear_model.MixedLM.html)
- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [scipy.stats.chi2](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html)


# Changelog
- Jun 18, 2026: Post published
