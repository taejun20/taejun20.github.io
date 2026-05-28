---
title: Aligned Rank Transform: How to use ARTool in R
date: 2021-09-03
tag: Statistics
---

Multi-factor design experiment의 데이터가 정규성을 만족하지 못할 때, 데이터에 Aligned Rank Transform을 수행한 다음 parametric test (i.e., Factorial ANOVA)를 수행할 수 있다. 정규성 검정은 주로 Shapiro-Wilk test로 확인하며, p < .05이면 정규성 가정이 기각된다. 단순 비모수 검정(Kruskal-Wallis 등)과 달리, ART는 interaction effect까지 검정할 수 있다는 점이 핵심적인 장점이다. 

Aligned Rank Transform은 (1) Data Alignment, (2) Rank Transform 순서로 Data Transform이 이뤄지는 과정이며 Wobbrock et al.의 논문 [3]에 각 세부 과정이 설명되어 있다.

# Rank Transform & Data Alignment

Conover and Iman [2] (1981)이 rank transformed data에 parametric F-test를 수행하는 방법을 제안했고, 이후 연구들 [4]에서 이 방식이 부정확한 interaction effect를 도출함을 확인했다고 한다. 그 후 Aligned Rank Transform [3]이 rank transform 이전에 data alignment [5] 과정을 거치는 방식으로 이러한 문제를 보완했다고 한다. F-test on rank가 valid한 이유, data alignment process가 기존의 문제를 보완하는 이유 등은 관련 논문들 [2,3,4,5]에 설명이 되어 있다. 사실 제대로 이해해보려고 뛰어들었다가 먼저 알아야 하는 선행 통계 지식들이 너무 많이 엮여 있어서 포기하고 그냥 사용하기로 했다.

# ARTool R Package by Wobbrock et al.

[ARTool](http://depts.washington.edu/acelab/proj/art/index.html)는 Wobbrock et al.이 배포한 ART 툴이다. 윈도우 버전 GUI Executable 프로그램은 데이터를 규격에 맞춰 csv 파일로 준비하면 각 factor 및 factor의 조합 별로 Data Alignment & Rank Transform을 데이터에 수행한 값들을 뽑아준다. 하지만 각 main effect 및 interaction effect를 확인하기 위한 여러 번의 ANOVA는 직접 다른 소프트웨어에서 수행해야 한다. 직접 해봤는데 매우 귀찮다. 그래서 GUI 프로그램보다는 R 패키지를 쓰는게 좋다. R에서는 데이터만 dataframe으로 만들어서 `art()` 함수에 넣어주면 모든 effect를 한 번에 뽑아준다.

# R Codes

## (1) ARTool 패키지 설치 및 로드

```r
install.packages("ARTool")
library(ARTool)
```

## (2) data frame 준비

아래와 같은 규격이 되어야 한다. 1번째 column은 subject (실제 계산에 사용되지는 않는다), 가장 오른쪽 column은 response, 그 사이는 independent variable이 factor 자료형으로 준비되어야 한다. `dplyr` 패키지의 `group_by()` 메소드를 사용하면 아래 규격을 만들기 쉽다.

![data.frame contents for ART process|50%](img/posts/210903-aligned-rank-transform/dataframe.png)

## (3) ART 및 ANOVA 메소드 수행

Repeated measures의 경우 아래와 같이 `Error(SubjectName/(MenuType*itemNum))`, Repeated measures가 아닌 경우는 `(1|SubjectName)`으로 입력하면 된다 [7].

```
# Repeated measures
m <- art(Response ~ FactorA * FactorB + Error(Subject/(FactorA*FactorB)), data = df)
anova(m)

# Between-subjects (not repeated measures)
m <- art(Response ~ FactorA * FactorB + (1|Subject), data = df)
anova(m)
```
![Results of ART & ANOVA](img/posts/210903-aligned-rank-transform/art-results.png)

# 통계 분석 결과 리포트

```note
An aligned-rank transformed repeated-measures ANOVA revealed no significant main effect of MenuType on completion time. In contrast, there was a significant main effect of itemNum, F(1, 11) = 36.45, p < .001. The interaction between MenuType and itemNum was not significant.

An aligned-rank transformed repeated-measures ANOVA 결과, MenuType의 주효과는 완료 시간에 대해 유의하지 않았으며, itemNum의 주효과는 유의하였다 (F(1, 11) = 36.45, p < .001). MenuType과 itemNum 간 상호작용 효과는 유의하지 않았다.
```

# 참고

[1] [ANOVA on ranks – Wikipedia](https://en.wikipedia.org/wiki/ANOVA_on_ranks)  
[2] Conover, W. J., & Iman, R. L. (1981). Rank transformations as a bridge between parametric and nonparametric statistics. *The American Statistician*, 35(3), 124–129.  
[3] Wobbrock, J. O., et al. (2011). The aligned rank transform for nonparametric factorial analyses using only ANOVA procedures. *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems*.  
[4] Salter, K. C., & Fawcett, R. F. (1993). The ART test of interaction: a robust and powerful rank test of interaction in factorial models. *Communications in Statistics-Simulation and Computation*, 22(1), 137–153.  
[5] Hodges, J. L., & Lehmann, E. L. (2012). Rank methods for combination of independent experiments in analysis of variance. *Selected Works of E.L. Lehmann*. Springer.  
[6] [ARTool project page](http://depts.washington.edu/acelab/proj/art/index.html)  
[7] [ARTool CRAN documentation](https://cran.r-project.org/web/packages/ARTool/ARTool.pdf)

# 변경 이력
- 2021년 9월 3일: 글 등록
- 2021년 9월 24일: 글 보완
- 2021년 12월 1일: Velog로 이전
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
