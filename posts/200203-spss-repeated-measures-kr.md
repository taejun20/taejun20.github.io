---
title: SPSS (1) One-way Repeated Measure ANOVA & Friedman test
date: 2020-02-03
tag: Statistics
---

Within-Subject 실험 디자인은 비교적 적은 사람 수로 Independent variable이 미치는 통계적 유의성을 확인할 수 있게 해준다. SPSS 프로그램으로 Repeated Measure (Within-Subject) ANOVA 테스트를 돌려보는 과정을 정리해보자.

![IBM SPSS Statistics 25버전|100%](img/posts/200203-spss-repeated-measures/overview.jpg)

# 어떤 통계 테스트?

SPSS로 들어가기 전에, 잘 정리된 수형도를 보자. 가장 최근 내가 분석한 데이터는

- Outcome variable 개수 = 1개 (Accuracy)
- Outcome variable type = Continuous
- Predictor variable 개수 = 1개 (착용한 디바이스 종류)
- Predictor variable type = Categorical
- How many categories? = More than two (3개, 디바이스 종류)
- Same or different entities in each category? = Same (이 조건이 Same이면 within-subject, Different면 between-subject 디자인이다)

마지막으로 정규성 검정을 통과한다면 One-way Repeated Measures ANOVA를 하면 되고, 통과하지 못하면 Bootstrapped ANOVA 혹은 Friedman's ANOVA를 하면 된다.

![Toetskeuzeschema Field](img/posts/200203-spss-repeated-measures/decision-tree.jpg)

지금부터 SPSS로 할 것은 다음과 같다:

- 데이터의 정규성 검정
- 각 테스트 (One-way RM ANOVA / Friedman's ANOVA)
  - 구형성 체크
  - 방법 간 차이의 significant effect (p-value) 체크
  - post-hoc 분석

# 1. 정규성(Normality) 검정

## 프로그램 사용

1. 분석 → 기술통계량 → 데이터 탐색 클릭

![|70%](img/posts/200203-spss-repeated-measures/normality-step1.jpg)

2. 검사하려는 변수를 종속변수에 추가한 후 '통계량' 클릭

![|60%](img/posts/200203-spss-repeated-measures/normality-step2.jpg)

3. 아래 옵션으로 설정 후 '계속' 클릭

![|30%](img/posts/200203-spss-repeated-measures/normality-step3.jpg)

4. 도표 클릭

![|60%](img/posts/200203-spss-repeated-measures/normality-step4.jpg)

5. 아래 옵션으로 설정 후 '계속' 클릭

![|40%](img/posts/200203-spss-repeated-measures/normality-step5.jpg)

6. '확인' 클릭

![|60%](img/posts/200203-spss-repeated-measures/normality-step6.jpg)

## 결과 분석

![|70%](img/posts/200203-spss-repeated-measures/normality-result.jpg)

```note
정규성 검정 표 확인
- Shapiro-Wilk Test의 유의확률(p-value)이 0.05보다 크면 정규성 성립
- VAR 1는 정규성이 성립하지 않고 VAR 2, 3는 성립함을 알 수 있음
- 조건 중 하나라도 정규성이 만족되지 않으면 전체 데이터에 대해 비모수 검정(Friedman's test)을 사용하는 것이 보수적인 선택이다
```

# 2-1. One-way Repeated Measure ANOVA

이 글에서 가장 중요한 부분이고 앞으로 가장 많이 쓰게 될 테스트다.

## 프로그램 사용

1. 분석 → 일반선형모델 → 반복측도 클릭

![|80%](img/posts/200203-spss-repeated-measures/anova-step1.jpg)

2. 요인 이름, 측도 이름을 임의로 정함. 수준 수에는 조건 개수 입력. 추가한 뒤 '정의' 클릭

![|40%](img/posts/200203-spss-repeated-measures/anova-step2.jpg)

3. 왼쪽의 Column들을 개체-내 변수로 이동

![|50%](img/posts/200203-spss-repeated-measures/anova-step3.jpg)

4. 'EM 평균' 클릭. 독립 변수를 오른쪽으로 옮기고 '주효과 비교' 체크, 아래는 Bonferroni 선택

![|50%](img/posts/200203-spss-repeated-measures/anova-step4.jpg)

5. '옵션' 클릭. '기술통계량' 체크

![|40%](img/posts/200203-spss-repeated-measures/anova-step5.jpg)

6. '확인' 클릭

## 결과 분석

**구형성 확인**

![|80%](img/posts/200203-spss-repeated-measures/anova-result-sphericity.jpg)

```note
- Mauchly's Test에서 유의 확률(p-value)이 0.05보다 크면 구형성 만족
- 본 데이터는 구형성이 만족됨
- 구형성이 만족되지 않으면 Greenhouse-Geisser Epsilon 값에 따라 다른 보정 결과를 사용한다.
  - Epsilon < 0.75: Greenhouse-Geisser 보정 결과 사용
  - Epsilon ≥ 0.75: Huynh-Feldt 보정 결과 사용
- Repeated Measure의 level이 여기서는 3개지만, 2개라면 자동으로 구형성이 만족되어 체크할 필요가 없다.
```

**방법 간 차이의 significant effect 체크**

![|80%](img/posts/200203-spss-repeated-measures/anova-result-effect.jpg)

```note
구형성 가정이 만족됐기 때문에 가장 위의 유의확률(p-value)를 보면 된다. p < 0.05로 방법 간 차이의 significant effect가 확인됨.

"There was a significant effect of type of device on accuracy (F(2,20)=11.639, p<.001)"
```

**사후 분석 (post-hoc analysis w/ Bonferroni Correction)**

![|80%](img/posts/200203-spss-repeated-measures/anova-result-posthoc.jpg)

```note
아래 표를 확인해보면 (device 1 − device 2), (device 3 − device 2) 사이에는 유의미한 차이가 있고, (device 1 − device 3) 사이에는 유의미한 차이가 없음을 확인할 수 있다.
```

# 2-2. Friedman's test

Friedman's test의 사후분석은 비모수검정(non-parametric test)의 post-hoc 분석에 쓰일 수 있는 Wilcoxon Signed-Rank Test를 따로 사용해야 하기 때문에 섹션을 나눈다.

## 프로그램 사용 (1)

1. 분석 → 비모수 검정 → 레거시 대화상자 → K-대응표본 클릭

![|90%](img/posts/200203-spss-repeated-measures/friedman-step1.jpg)

2. 왼쪽의 Column들을 검정 변수로 이동. 아래 Friedman에 체크된 것 확인

![|50%](img/posts/200203-spss-repeated-measures/friedman-step2.jpg)

3. '통계량' 클릭 → '사분위수' 체크 후 '계속' 클릭

![|30%](img/posts/200203-spss-repeated-measures/friedman-step3.jpg)

4. '확인' 클릭

## 결과 분석 (1)

![|30%](img/posts/200203-spss-repeated-measures/friedman-result.jpg)

```note
검정 통계량의 근사 유의확률이 0.05보다 작으므로 significant effect가 있다.  
"A Friedman test revealed a significant effect of type of device on accuracy (χ²(2) = 12.182, p < .005)"
```

## 프로그램 사용 (2) — 사후 분석 (Wilcoxon signed-rank test)

1. 분석 → 비모수 검정 → 레거시 대화상자 → 2-대응표본 클릭

![|80%](img/posts/200203-spss-repeated-measures/wilcoxon-step1.jpg)

2. 비교하고 싶은 변수의 pair를 모두 오른쪽으로 옮긴다

![|60%](img/posts/200203-spss-repeated-measures/wilcoxon-step2.jpg)

3. '옵션' 클릭 → '기술통계', '사분위수' 체크 후 '계속' 클릭

![|30%](img/posts/200203-spss-repeated-measures/wilcoxon-step3.jpg)

4. '확인' 클릭

## 결과 분석 (2) — 사후 분석 (Wilcoxon signed-rank test)

![|50%](img/posts/200203-spss-repeated-measures/wilcoxon-result.jpg)

```note
검정 통계량의 유의 확률이 0.05보다 작다면 각 pair 사이에는 유의미한 차이가 있다. 검정 통계량의 유의 확률이 0.05보다 작다면 각 pair 사이에는 유의미한 차이가 있다. 단, 여러 pair를 동시에 검정하면 다중 비교 문제로 1종 오류(false positive)가 증가하므로 Bonferroni correction을 적용한다. 조건이 3개라면 pair는 3쌍이므로 p 값에 3을 곱하여 판단한다 (유의수준을 α / 3 = 0.05 / 3 ≈ 0.017로 낮춰서 판단하기 위해).
```

# 변경 이력
- 2020년 2월 3일: 글 등록
- 2021년 12월 1일: "그래프 그리기" 섹션 삭제, Velog로 이전
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
