---
title: SPSS (2) Two-way Repeated Measure ANOVA
date: 2020-04-20
tag: Statistics
---

[이전 포스트](/posts?post=200203-spss-repeated-measures)에서는 독립 변수가 하나인 실험에서 One-way RM ANOVA와 Friedman Test를 정리했다. 이번에는 Two-way RM ANOVA 테스트를 돌려보자.

# 어떤 테스트?

내가 분석해야 할 데이터는

- Outcome variable 개수 = 1개 (Accuracy)
- Outcome variable type = Continuous
- Predictor variable 개수 = 2개 (방위 기준, 팔의 자세)
- Predictor variable type = Categorical
- Same or different entities in each category? = Same (이 조건이 Same이면 within-subject, Different면 between-subject 디자인)

마지막으로 정규성 검정을 통과하면 Factorial Repeated Measure ANOVA, 통과하지 못하면 Robust Factorial Repeated Measure ANOVA를 한다.

![Toetskeuzeschema Field](img/posts/200420-spss-two-way-anova/decision-tree.jpg)

지금부터의 목차는 다음과 같다:

- 데이터의 정규성 검정
- 테스트 (Factorial RM ANOVA)
  - 구형성 체크
  - 방법 간 차이의 significant effect (p-value) 체크
  - post-hoc 분석

정규성이 만족되지 않는 경우에는 [Aligned Rank Transform](/posts?post=210903-aligned-rank-transform) 이후 Two-way RM ANOVA를 사용한다.



# 1. 정규성(Normality) 검정

## 프로그램 사용

1. 분석 → 기술통계량 → 데이터 탐색 클릭

![|70%](img/posts/200420-spss-two-way-anova/normality-step1.jpg)

2. 검사하려는 변수를 종속변수에 추가한 후 '통계량' 클릭

![|50%](img/posts/200420-spss-two-way-anova/normality-step2.jpg)

3. 아래 옵션으로 설정 후 '계속' 클릭

![|30%](img/posts/200420-spss-two-way-anova/normality-step3.jpg)

4. 도표 클릭

![|50%](img/posts/200420-spss-two-way-anova/normality-step4.jpg)

5. 아래 옵션으로 설정 후 '계속' 클릭

![|40%](img/posts/200420-spss-two-way-anova/normality-step5.jpg)

6. '확인' 클릭

![|50%](img/posts/200420-spss-two-way-anova/normality-step6.jpg)

## 결과 분석

![|70%](img/posts/200420-spss-two-way-anova/normality-result.jpg)

```note
정규성 검정 표 확인
- Shapiro-Wilk normality Test의 유의확률(p-value)이 0.05보다 크면 정규성 성립
- 모든 조건의 데이터에서 정규성이 만족하는 것을 알 수 있음
```

# 2-1. Factorial RM ANOVA (2-way, 3-way, ...)

2-way, 3-way, 4-way, … 모두 Factorial RM ANOVA 테스트로 한다.

## 프로그램 사용

1. 분석 → 일반선형모델 → 반복측도 클릭

![|70%](img/posts/200420-spss-two-way-anova/anova-step1.jpg)

2. 요인 2개(two-way)를 추가, 측도도 추가한 뒤 '정의' 클릭

![|30%](img/posts/200420-spss-two-way-anova/anova-step2.jpg)

3. 왼쪽의 모든 변수를 개체-내 변수 박스로 이동

![|50%](img/posts/200420-spss-two-way-anova/anova-step3.jpg)

4. 'EM 평균' 클릭. 변수 3개를 모두 오른쪽으로 옮기고 '주효과 비교' 체크, 아래는 Bonferroni 선택. '계속' 클릭

![|40%](img/posts/200420-spss-two-way-anova/anova-step4.jpg)

5. '옵션' 클릭. 기술통계량 체크. '계속' 클릭.

![|40%](img/posts/200420-spss-two-way-anova/anova-step5.jpg)

6. '확인' 클릭

## 결과 분석

**구형성 검정**

![|90%](img/posts/200420-spss-two-way-anova/anova-result-sphericity.jpg)

```note
- Mauchly's Test에서 유의 확률(p-value)이 0.05보다 크면 구형성 만족
- 본 데이터는 구형성이 만족됨
구형성이 만족되지 않으면 Greenhouse-Geisser Epsilon 값에 따라 다른 보정 결과를 사용한다.
  - Epsilon < 0.75: Greenhouse-Geisser 보정 결과 사용
  - Epsilon ≥ 0.75: Huynh-Feldt 보정 결과 사용
- 독립 변수의 level이 2개라면 자동으로 구형성이 만족되어 체크할 필요가 없다. (변수 orientation의 케이스)
```

**방법 간 차이의 significant effect 체크**

![|80%](img/posts/200420-spss-two-way-anova/anova-result-effect.jpg)

```note
구형성 가정이 만족됐기 때문에 각 행의 가장 위 유의확률(p-value)를 보면 된다.
결과 표에는 아래 세 가지를 순서대로 확인해야 한다.

1. orientation의 main effect
2. armpose의 main effect
3. orientation × armpose의 interaction effect

armpose에서만 p < 0.05로 significant effect가 확인됐다. Interaction effect가 유의미하지 않으므로 각 factor의 main effect를 독립적으로 해석할 수 있다. (만약 interaction effect가 유의미했다면 main effect만으로 결론을 내릴 수 없고, 사후 분석에서 조건 조합별 비교가 필요하다. Interaction effect에 관해서는 [이 글](/posts?post=200903-interaction-effects-anova) 참고.)

"There was a significant main effect of armpose on accuracy (F(2,22)=20.482, p < .001).
The main effect of orientation was not significant.
The interaction between orientation and armpose was not significant."
```

**사후 분석 (post-hoc analysis w/ Bonferroni Correction)**

orientation에 대한 사후 분석. 유의미한 차이가 없음을 알 수 있다.

![|70%](img/posts/200420-spss-two-way-anova/anova-result-posthoc-orientation.jpg)

armpose에 대한 사후 분석. (armpose 2 − armpose 1), (armpose 2 − armpose 3) 사이에 유의미한 차이가 있고, (armpose 1 − armpose 3) 사이에는 유의미한 차이가 없음을 알 수 있다.

![|70%](img/posts/200420-spss-two-way-anova/anova-result-posthoc-armpose.jpg)

위 사후 분석은 main effect가 유의미한 경우에 해당한다. 만약 interaction effect가 유의미하게 나왔다면 main effect post-hoc만으로는 부족하고, 각 조건 조합(예: orientation 1 & armpose 1 vs orientation 1 & armpose 2 등)에 대한 simple effects 분석이 추가로 필요하다.

# 변경 이력
- 2020년 4월 20일: 글 등록
- 2021년 12월 1일: Velog로 이전
- 2026년 2월 28일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
