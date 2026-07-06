---
title: Understanding F-test (ANOVA): Hands-on Calculation
date: 2021-09-23
tag: Statistics
---

Analysis of Variance (ANOVA) uses the F-test to determine whether the means of three or more groups differ significantly from each other (for two groups, use a [t-test](/posts?post=260617-paired-t-test-python-en)). In this post, I'll calculate the F-value by hand to build an intuition for what it means.

![Right-tail F-distribution|90%](img/posts/210923-anova-ftest/f-distribution.jpg)

# One-way ANOVA (F-test): Hands-on Calculation

The F-value formula is:

![|60%](img/posts/210923-anova-ftest/f-value-formula.jpg)

Below is the F-value calculation on a dataset I made up for a one-way between-subjects design with three factor levels (A, B, C).

![](img/posts/210923-anova-ftest/f-value-calculation.jpg)

![F(2,9)-distribution from StatDistributions.com](img/posts/210923-anova-ftest/f-distribution-29.jpg)

# Interpretation

The F-value is defined as (variance between groups / variance within groups). A larger F-value means greater differences between groups. If the calculated F-value exceeds the critical F-value, the differences between groups are considered statistically significant. The critical F-value is set so that the right-tail area of the F-distribution equals 5% of the total area (p = 0.05).

As shown above, the critical F(2, 9) = 4.257. The two numbers in **F(2, 9)** are the degrees of freedom. The critical F-value changes with the degrees of freedom, so make sure to use the value that matches your experimental design. The F-value calculated from the example data is 15.14. Therefore:

```note
Null Hypothesis: "Mean response of group A = group B = group C"  
F-value > Critical F-value (p < .05). Reject the null hypothesis.  
The F-test confirms a statistically significant difference among the means of the three groups.
```

Note that the F-test only tells you that "at least one group mean is different." It does not tell you which specific pairs differ. To find out which pairs are significantly different, a post-hoc test is needed, such as [pairwise t-tests with Bonferroni correction](/posts?post=260617-paired-t-test-python-en).

# References

- [One Way ANOVA – YouTube](https://www.youtube.com/watch?v=WUjsSB7E-ko)
- [F-test – Statistics How To](https://www.statisticshowto.com/probability-and-statistics/hypothesis-testing/f-test/#hand)
- [F-test – Wikipedia](https://en.wikipedia.org/wiki/F-test)
- [StatDistributions.com](http://www.statdistributions.com/f/)

# Changelog
- Sep 23, 2021: Post published
- Dec 1, 2021: Migrated to Velog
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
- Jul 6, 2026: Fixed a typo in the F formula in the image, found and kindly reported by [Zheming Yin](https://scholar.google.com/citations?user=sM512LgAAAAJ&hl=ko&oi=ao)
