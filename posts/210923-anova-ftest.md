---
title: Understanding F-test (ANOVA): Hands-on Calculation
date: 2021-09-23
tag: Statistics
---

Analysis of Variance (ANOVA)는 F-test를 통해 세 집단 이상의 평균이 서로 유의미하게 다른지 확인한다 (두 집단 비교에는 t-test). 본 글에서는 F-value를 직접 손으로 계산해보며 그 의미를 이해해본다.

![Right-tail F-distribution|90%](img/posts/210923-anova-ftest/f-distribution.png)

# One way ANOVA (F-test) Hands on Calculation

F-value formula는 아래와 같다.

![|60%](img/posts/210923-anova-ftest/f-value-formula.png)

아래는 내가 임의로 만든 One way between-subjects 디자인 (Factor Levels: A, B, C) 실험의 데이터에서 F-value를 계산해본 결과이다.

![](img/posts/210923-anova-ftest/f-value-calculation.png)

![F(2,9)-distribution from StatDistributions.com](img/posts/210923-anova-ftest/f-distribution-29.png)

# Interpretation

F-value는 (집단 간의 분산 정도 / 집단 내 분산 정도)로 정의된다. 즉 F-value가 크다는 것은 집단 간의 차이가 크다는 것을 의미한다. 계산된 F-value가 Critical F-value보다 크면 집단 간의 차이가 통계적으로 유의미한 것으로 본다. F-distribution에서 오른쪽 적분 값이 전체 면적의 5% (p=0.05)가 되도록 Critical F-value는 설정된다.

위의 그림에서 보여지듯이 Critical F(2, 9) = 4.257이다. 여기서 **F(2, 9)**의 두 숫자는 자유도(degrees of freedom)다. 자유도가 달라지면 Critical F-value도 달라지므로, 실험 설계에 맞는 값을 사용해야 한다. 그리고 예시 데이터 상황에서 계산된 F-value = 15.14이다. 따라서 F-test의 결과는 다음과 같다.

```note
Null Hypothesis: "Mean response of group A = .. B = .. C"  
F-value > Critical F-value (p < .05). Reject the null hypothesis.  
F-test를 통해 세 집단의 평균 사이에 통계적으로 유의미한 차이가 있음을 확인했다.
```

단, F-test는 "적어도 하나의 집단 평균이 다르다"는 것만 알려줄 뿐, 어느 집단 사이에 차이가 있는지는 알려주지 않는다. 구체적으로 어떤 쌍(pair)이 유의미하게 다른지 확인하려면 Paired t-test with Bonferroni correction 등의 사후 검정(Post-hoc test)이 필요하다.


# 참고

- [One Way ANOVA – YouTube](https://www.youtube.com/watch?v=WUjsSB7E-ko)
- [F-test – Statistics How To](https://www.statisticshowto.com/probability-and-statistics/hypothesis-testing/f-test/#hand)
- [F-test – Wikipedia](https://en.wikipedia.org/wiki/F-test)
- [StatDistributions.com](http://www.statdistributions.com/f/)

# 변경 이력
- 2021년 9월 23일: 글 등록
- 2021년 12월 1일: Velog로 이전
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
