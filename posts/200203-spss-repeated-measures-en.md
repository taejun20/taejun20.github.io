---
title: SPSS (1) One-way Repeated Measure ANOVA & Friedman test
date: 2020-02-03
tag: Statistics
---

A within-subject design lets you detect the statistical significance of an independent variable with a relatively small number of participants. Here's how to run a Repeated Measure (Within-Subject) ANOVA in SPSS. (Sorry, all screenshots are based on the Korean language settings)

![IBM SPSS Statistics version 25|100%](img/posts/200203-spss-repeated-measures/overview.jpg)

# Which Statistical Test?

Before opening SPSS, let's use a decision tree. My recent dataset had:

- Number of outcome variables = 1 (Accuracy)
- Outcome variable type = Continuous
- Number of predictor variables = 1 (type of device worn)
- Predictor variable type = Categorical
- How many categories? = More than two (3 device types)
- Same or different entities in each category? = Same (Same = within-subject; Different = between-subject)

If the data passes a normality test, use One-way Repeated Measures ANOVA. If not, use Bootstrapped ANOVA or Friedman's ANOVA.

![Toetskeuzeschema Field](img/posts/200203-spss-repeated-measures/decision-tree.jpg)

Here's what we'll do in SPSS:

- Test normality
- Run each test (One-way RM ANOVA / Friedman's ANOVA)
  - Check sphericity
  - Check significant effect between conditions (p-value)
  - Post-hoc analysis

# 1. Normality Test

## Steps

1. Analyze → Descriptive Statistics → Explore

![|70%](img/posts/200203-spss-repeated-measures/normality-step1.jpg)

2. Add variables to the Dependent Variable List, then click Statistics

![|60%](img/posts/200203-spss-repeated-measures/normality-step2.jpg)

3. Set options as shown, click Continue

![|30%](img/posts/200203-spss-repeated-measures/normality-step3.jpg)

4. Click Plots

![|60%](img/posts/200203-spss-repeated-measures/normality-step4.jpg)

5. Set options as shown, click Continue

![|40%](img/posts/200203-spss-repeated-measures/normality-step5.jpg)

6. Click OK

![|60%](img/posts/200203-spss-repeated-measures/normality-step6.jpg)

## Reading the Output

![|70%](img/posts/200203-spss-repeated-measures/normality-result.jpg)

```note
Check the normality test table:
- If the Shapiro-Wilk p-value > 0.05, normality is satisfied
- In this example, VAR 1 fails normality; VAR 2 and 3 pass
- If even one condition fails normality, the conservative choice is to use a non-parametric test (Friedman's test) for the entire dataset
```

# 2-1. One-way Repeated Measure ANOVA

The most important part of this post, and the test I'll use most going forward.

## Steps

1. Analyze → General Linear Model → Repeated Measures

![|80%](img/posts/200203-spss-repeated-measures/anova-step1.jpg)

2. Name the within-subject factor and measure. Enter the number of levels (conditions), click Add, then Define

![|40%](img/posts/200203-spss-repeated-measures/anova-step2.jpg)

3. Move the columns from the left into the Within-Subjects Variables box

![|50%](img/posts/200203-spss-repeated-measures/anova-step3.jpg)

4. Click EM Means. Move the independent variable to the right, check Compare main effects, select Bonferroni below

![|50%](img/posts/200203-spss-repeated-measures/anova-step4.jpg)

5. Click Options, check Descriptive statistics

![|40%](img/posts/200203-spss-repeated-measures/anova-step5.jpg)

6. Click OK

## Reading the Output

**Sphericity**

![|80%](img/posts/200203-spss-repeated-measures/anova-result-sphericity.jpg)

```note
- Mauchly's Test: if p > 0.05, sphericity is satisfied
- Sphericity is satisfied in this dataset
- If sphericity is violated, choose the correction based on Greenhouse-Geisser Epsilon:
  - Epsilon < 0.75: use Greenhouse-Geisser correction
  - Epsilon >= 0.75: use Huynh-Feldt correction
- If there are only 2 levels, sphericity is automatically satisfied and does not need to be checked
```

**Significant effect between conditions**

![|80%](img/posts/200203-spss-repeated-measures/anova-result-effect.jpg)

```note
Since sphericity is satisfied, read the top row p-value. p < 0.05 confirms a significant effect.

"There was a significant effect of type of device on accuracy (F(2,20)=11.639, p<.001)"
```

**Post-hoc analysis (Bonferroni correction)**

![|80%](img/posts/200203-spss-repeated-measures/anova-result-posthoc.jpg)

```note
The table shows a significant difference between (device 1 vs. device 2) and (device 3 vs. device 2), but not between (device 1 vs. device 3).
```

# 2-2. Friedman's Test

Friedman's test requires a separate post-hoc step using the Wilcoxon Signed-Rank Test, so it gets its own section.

## Steps (1)

1. Analyze → Nonparametric Tests → Legacy Dialogs → K Related Samples

![|90%](img/posts/200203-spss-repeated-measures/friedman-step1.jpg)

2. Move the columns into the Test Variables box. Confirm Friedman is checked below

![|50%](img/posts/200203-spss-repeated-measures/friedman-step2.jpg)

3. Click Statistics, check Quartiles, click Continue

![|30%](img/posts/200203-spss-repeated-measures/friedman-step3.jpg)

4. Click OK

## Reading the Output (1)

![|30%](img/posts/200203-spss-repeated-measures/friedman-result.jpg)

```note
The asymptotic significance is less than 0.05, so there is a significant effect.
"A Friedman test revealed a significant effect of type of device on accuracy (χ²(2) = 12.182, p < .005)"
```

## Steps (2): Post-hoc (Wilcoxon Signed-Rank Test)

1. Analyze → Nonparametric Tests → Legacy Dialogs → 2 Related Samples

![|80%](img/posts/200203-spss-repeated-measures/wilcoxon-step1.jpg)

2. Move all pairs you want to compare to the right

![|60%](img/posts/200203-spss-repeated-measures/wilcoxon-step2.jpg)

3. Click Options, check Descriptive and Quartiles, click Continue

![|30%](img/posts/200203-spss-repeated-measures/wilcoxon-step3.jpg)

4. Click OK

## Reading the Output (2): Post-hoc (Wilcoxon Signed-Rank Test)

![|50%](img/posts/200203-spss-repeated-measures/wilcoxon-result.jpg)

```note
If the significance value for a pair is less than 0.05, there is a significant difference between them. However, testing multiple pairs simultaneously inflates the Type I error rate (false positives), so apply Bonferroni correction: multiply each p-value by the number of pairs. With 3 conditions there are 3 pairs, so multiply p by 3 (equivalent to using a threshold of α / 3 = 0.05 / 3 ≈ 0.017).
```

# Changelog
- Feb 3, 2020: Post published
- Dec 1, 2021: Removed "Plotting graphs" section, migrated to Velog
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
