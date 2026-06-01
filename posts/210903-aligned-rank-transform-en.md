---
title: Aligned Rank Transform: How to use ARTool in R
date: 2021-09-03
tag: Statistics
---

When data from a multi-factor design experiment fails the normality assumption, you can apply Aligned Rank Transform (ART) and then run a parametric test (i.e., Factorial ANOVA). Normality is typically checked with the Shapiro-Wilk test; p < .05 means the normality assumption is rejected. Unlike simple non-parametric tests (e.g., Kruskal-Wallis), the key advantage of ART is that it can also test interaction effects.

Aligned Rank Transform is a two-step data transformation process: (1) Data Alignment, then (2) Rank Transform. The details of each step are described in Wobbrock et al. [3].

# Rank Transform & Data Alignment

Conover and Iman [2] (1981) proposed applying a parametric F-test to rank-transformed data. Later studies [4] found that this approach produced inaccurate interaction effects. Aligned Rank Transform [3] addressed this by adding a data alignment [5] step before the rank transform. The reasons why F-test on ranks is valid and why data alignment fixes the problem are explained in the related papers [2,3,4,5]. I tried to understand it properly but quickly ran into a wall of prerequisite statistical knowledge, so I gave up and decided to just use it.

# ARTool R Package by Wobbrock et al.

[ARTool](http://depts.washington.edu/acelab/proj/art/index.html) is the ART tool released by Wobbrock et al. The Windows GUI executable takes a CSV file in the required format and outputs data after alignment and rank transformation for each factor and combination. But you still have to run the ANOVA tests separately in another tool. I tried it. It's tedious. The R package is much better: just put your data into a dataframe and pass it to the `art()` function, and it gives you all effects at once.

# R Code

## (1) Install and load ARTool

```r
install.packages("ARTool")
library(ARTool)
```

## (2) Prepare the data frame

The format should look like below. The first column is the subject (not used directly in the calculation), the rightmost column is the response, and the columns in between are independent variables stored as factor type. The `group_by()` method from the `dplyr` package makes it easy to build this format.

![data.frame contents for ART process|50%](img/posts/210903-aligned-rank-transform/dataframe.png)

## (3) Run ART and ANOVA

For repeated measures, use `Error(SubjectName/(FactorA*FactorB))`. For between-subjects, omit the error term [7].

```
# Repeated measures
m <- art(Response ~ FactorA * FactorB + Error(Subject/(FactorA*FactorB)), data = df)
anova(m)

# Between-subjects (not repeated measures)
m <- art(Response ~ FactorA * FactorB, data = df)
anova(m)
```

![Results of ART & ANOVA](img/posts/210903-aligned-rank-transform/art-results.png)

# Reporting Results

```note
An aligned-rank transformed repeated-measures ANOVA revealed no significant main effect of MenuType on completion time. In contrast, there was a significant main effect of itemNum, F(1, 11) = 36.45, p < .001. The interaction between MenuType and itemNum was not significant.
```

# References

[1] [ANOVA on ranks – Wikipedia](https://en.wikipedia.org/wiki/ANOVA_on_ranks)  
[2] Conover, W. J., & Iman, R. L. (1981). Rank transformations as a bridge between parametric and nonparametric statistics. *The American Statistician*, 35(3), 124–129.  
[3] Wobbrock, J. O., et al. (2011). The aligned rank transform for nonparametric factorial analyses using only ANOVA procedures. *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems*.  
[4] Salter, K. C., & Fawcett, R. F. (1993). The ART test of interaction: a robust and powerful rank test of interaction in factorial models. *Communications in Statistics-Simulation and Computation*, 22(1), 137–153.  
[5] Hodges, J. L., & Lehmann, E. L. (2012). Rank methods for combination of independent experiments in analysis of variance. *Selected Works of E.L. Lehmann*. Springer.  
[6] [ARTool project page](http://depts.washington.edu/acelab/proj/art/index.html)  
[7] [ARTool CRAN documentation](https://cran.r-project.org/web/packages/ARTool/ARTool.pdf)

# Changelog
- Sep 3, 2021: Post published
- Sep 24, 2021: Content revised
- Dec 1, 2021: Migrated to Velog
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
