---
title: SPSS (2) Two-way Repeated Measure ANOVA
date: 2020-04-20
tag: Statistics
---

In the [previous post](/posts?post=200203-spss-repeated-measures), I covered One-way RM ANOVA and Friedman's test for experiments with a single independent variable. This post covers Two-way RM ANOVA. (Sorry, all screenshots are based on the Korean language settings)

# Which Test?

My dataset had:

- Number of outcome variables = 1 (Accuracy)
- Outcome variable type = Continuous
- Number of predictor variables = 2 (orientation reference, arm posture)
- Predictor variable type = Categorical
- Same or different entities in each category? = Same (Same = within-subject; Different = between-subject)

If normality is satisfied, use Factorial Repeated Measure ANOVA. If not, use Robust Factorial Repeated Measure ANOVA.

![Toetskeuzeschema Field](img/posts/200420-spss-two-way-anova/decision-tree.png)

What we'll do:

- Test normality
- Run Factorial RM ANOVA
  - Check sphericity
  - Check significant effect between conditions (p-value)
  - Post-hoc analysis

If normality is not satisfied, use [Aligned Rank Transform](/posts?post=210903-aligned-rank-transform) followed by Two-way RM ANOVA.

# 1. Normality Test

## Steps

1. Analyze → Descriptive Statistics → Explore

![|70%](img/posts/200420-spss-two-way-anova/normality-step1.png)

2. Add variables to the Dependent Variable List, then click Statistics

![|50%](img/posts/200420-spss-two-way-anova/normality-step2.png)

3. Set options as shown, click Continue

![|30%](img/posts/200420-spss-two-way-anova/normality-step3.png)

4. Click Plots

![|50%](img/posts/200420-spss-two-way-anova/normality-step4.png)

5. Set options as shown, click Continue

![|40%](img/posts/200420-spss-two-way-anova/normality-step5.png)

6. Click OK

![|50%](img/posts/200420-spss-two-way-anova/normality-step6.png)

## Reading the Output

![|70%](img/posts/200420-spss-two-way-anova/normality-result.png)

```note
Check the normality test table:
- If the Shapiro-Wilk p-value > 0.05, normality is satisfied
- All conditions pass normality in this dataset
```

# 2-1. Factorial RM ANOVA (2-way, 3-way, ...)

This same procedure handles 2-way, 3-way, 4-way, and beyond.

## Steps

1. Analyze → General Linear Model → Repeated Measures

![|70%](img/posts/200420-spss-two-way-anova/anova-step1.png)

2. Add two within-subject factors (for two-way), add a measure name, click Define

![|30%](img/posts/200420-spss-two-way-anova/anova-step2.png)

3. Move all variables from the left into the Within-Subjects Variables box

![|50%](img/posts/200420-spss-two-way-anova/anova-step3.png)

4. Click EM Means. Move all three variables to the right, check Compare main effects, select Bonferroni, click Continue

![|40%](img/posts/200420-spss-two-way-anova/anova-step4.png)

5. Click Options, check Descriptive statistics, click Continue

![|40%](img/posts/200420-spss-two-way-anova/anova-step5.png)

6. Click OK

## Reading the Output

**Sphericity**

![|90%](img/posts/200420-spss-two-way-anova/anova-result-sphericity.png)

```note
- Mauchly's Test: if p > 0.05, sphericity is satisfied
- Sphericity is satisfied in this dataset
- If violated, choose the correction based on Greenhouse-Geisser Epsilon:
  - Epsilon < 0.75: use Greenhouse-Geisser correction
  - Epsilon >= 0.75: use Huynh-Feldt correction
- If a factor has only 2 levels, sphericity is automatically satisfied and does not need to be checked (the case for the orientation variable here)
```

**Significant effect between conditions**

![|80%](img/posts/200420-spss-two-way-anova/anova-result-effect.png)

```note
Since sphericity is satisfied, read the top p-value in each row.
Check the following three things in order:

1. Main effect of orientation
2. Main effect of armpose
3. Interaction effect of orientation x armpose

Only armpose shows p < 0.05, confirming a significant effect. Since the interaction effect is not significant, the main effects of each factor can be interpreted independently. (If the interaction were significant, main effects alone would not be sufficient; pairwise comparisons across condition combinations would be needed in post-hoc. See [this post](/posts?post=200903-interaction-effects-anova) for more on interaction effects.)

"There was a significant main effect of armpose on accuracy (F(2,22)=20.482, p < .001).
The main effect of orientation was not significant.
The interaction between orientation and armpose was not significant."
```

**Post-hoc analysis (Bonferroni correction)**

Post-hoc for orientation: no significant differences found.

![|70%](img/posts/200420-spss-two-way-anova/anova-result-posthoc-orientation.png)

Post-hoc for armpose: significant differences between (armpose 2 vs. armpose 1) and (armpose 2 vs. armpose 3), but not between (armpose 1 vs. armpose 3).

![|70%](img/posts/200420-spss-two-way-anova/anova-result-posthoc-armpose.png)

The post-hoc above applies when main effects are significant. If the interaction effect were significant, main effect post-hoc alone would not be enough; simple effects analysis across condition combinations (e.g., orientation 1 & armpose 1 vs. orientation 1 & armpose 2) would also be needed.

# Changelog
- Apr 20, 2020: Post published
- Dec 1, 2021: Migrated to Velog
- Feb 28, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
