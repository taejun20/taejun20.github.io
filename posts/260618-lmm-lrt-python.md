---
title: Tutorial: Linear Mixed Model with Python - Component Contribution Analysis
date: 2026-06-18
tag: Statistics
---

Component Contribution Analysis를 위해 Linear Mixed Model (LMM)을 fitting하는 파이썬 코드를 공유한다. 이는 특정 modular system이 있을 때, 그리고 각 피험자로부터 여러 모듈의 조합에 대해 repeated observations을 수집한 경우에 각 modular component가 결과 퍼포먼스에 significant한 기여를 했는가를 통계적으로 확인할 때 사용된다. 말이 너무 복잡한데, 아래 예시를 보면 좀 더 쉽게 이해할 수 있다. 

예를 들어, modular system의 가장 기본 modular component A가 있고, 이 A와 조합해서 추가할 수 있는 컴포넌트 B, C, D가 있다고 하자 (가능한 최종 시스템 경우의 수: A+B, A+C, A+C+D 등). 이처럼 A, B, C, D 모듈로 구성할 수 있는 시스템의 조합이 여러 가지 존재할 때, 각 컴포넌트의 추가가 결과 퍼포먼스에 통계적으로 유의미한 효과를 갖는지 알고 싶은 것이다. 조합의 경우가 많아서 직관적으로 생각하기 어려울 때, B라는 컴포넌트를 추가한 것은  의미있는 개선을 불러왔는가? 아니면 사실상 영향을 주지 못했나?에 대한 답을 내릴 수 있다.

구체적으로, linear mixed model을 fitting하고 Likelihood Ratio Test (LRT)를 실행해 이 질문들을 검정한다.

```note
**Note:** modular component들의 조합을 통해 최종적으로 만들어진 final system들 간의 paired 비교는 이 포스트에서 다루는 케이스가 아니며, 해당 경우에는 [대응 표본 t검정 (paired t-test)](http://localhost:3000/posts?post=260617-paired-t-test-python) 또는 [Wilcoxon signed-rank test](http://localhost:3000/posts?post=260617-wilcoxon-signed-rank-python)를 통해 쉽게 대답할 수 있다.
```
# 1. 데이터 정리

Google Spreadsheet로 데이터를 정리한다 (통계 테스트를 돌리기 전에 각 조건의 평균과 표준편차를 먼저 확인하면서 데이터에 대한 전반적인 감을 잡는다).

![|100%](img/posts/260618-lmm-lrt-python/data-table.jpg)

각 행은 피험자이고 각 열은 조건이다. 각 조건 이름 (csv 파일 상 column의 이름)은 `+`로 구분하여 입력해야 한다.

예시:
- RGB 카메라, 열화상, 뎁스: `RGB`, `RGB+Thermal`, `RGB+Depth`, `RGB+Thermal+Depth`, `Thermal`, `Thermal+Depth`, `Depth`
- 얼굴, 포즈, 시선: `Face`, `Face+Pose`, `Face+Gaze`, `Face+Pose+Gaze`, `Pose`, `Pose+Gaze`, `Gaze`

이 표를 CSV 파일 (data.csv)로 저장하고, 아래 Python 스크립트 (main.py)와 같은 폴더에 위치시킨다.

<a href="/files/260618-lmm-lrt-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Python 스크립트 실행

바로 돌려볼 수 있는 전체 스크립트를 먼저 첨부하였고, 이어서 각 파트에 대한 설명을 추가하였다.

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

### 1) 데이터 준비

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
```

`pd.read_csv`로 wide format의 CSV를 불러오고, `melt`로 long format으로 변환한다. `mixedlm`에는 long format이 필요하다.

```python
all_components = sorted(set(comp for cond in conditions for comp in cond.split('+')))
varying_components = [c for c in all_components if not all(c in cond.split('+') for cond in conditions)]
for comp in all_components:
    df_long[comp] = df_long['Condition'].apply(lambda x: 1 if comp in x.split('+') else 0)
```

그리고 이 부분에서 long format 데이터프레임에 0/1값을 갖는 column을 컴포넌트당 하나씩 추가한다. 해당 조건에 그 컴포넌트가 포함되면 1, 포함되지 않으면 0이다. `varying_components`는 모든 조건에 항상 포함된 컴포넌트를 제외한다. 항상 존재하는 컴포넌트는 그 컴포넌트가 포함되지 않은 condition이 없어 비교가 불가능하므로, varying component만 fixed effects predictor로 사용한다.

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

LRT는 full model (모든 varying component 포함)과 reduced model (컴포넌트 하나 제거) 간의 fit 차이를 비교한다. 이 차이를 카이제곱 (chi-square) 통계량으로 계산한다.

```python
full_model = smf.mixedlm("value ~ " + " + ".join(varying_components), data=df_long, groups=df_long[subject_col]).fit(reml=False)
for comp in varying_components:
    others = [c for c in varying_components if c != comp]
    reduced_model = smf.mixedlm("value ~ " + " + ".join(others), data=df_long, groups=df_long[subject_col]).fit(reml=False)
    chi2 = 2 * (full_model.llf - reduced_model.llf)
    p = stats.chi2.sf(chi2, df=1)
    print(f"Component {comp}: χ²(1) = {chi2:.2f}, p = {p:.4f}")
```

각 varying component에 대해 해당 컴포넌트를 제외한 reduced model을 fitting하고 다음을 계산한다: χ²(1) = 2 × (full log-likelihood − reduced log-likelihood). 이 chi-square 값이 클수록 해당 컴포넌트가 model fit을 유의미하게 향상시킨다는 의미이며, 이는 해당 컴포넌트가 결과에 significant effect를 미친다는 것을 의미한다.


Output:

```
=== LMM + LRT ===
Component A: χ²(1) = 7.07, p = 0.0078
Component B: χ²(1) = 0.07, p = 0.7920
Component C: χ²(1) = 0.01, p = 0.9319
Component D: χ²(1) = 8.79, p = 0.0030
```

컴포넌트 A와 D가 significant effect가 있다 (A: p < .01; D: p < .005). 컴포넌트 B와 C는 significant한 영향이 없다.

# 3. 결과 보고

```note
**Writing for report:** A linear mixed model with likelihood ratio tests revealed that components A (χ²(1) = 7.07, p < .01) and D (χ²(1) = 8.79, p < .005) significantly contributed to the outcome. Components B and C did not reach significance.
```


# Note: Linear Mixed Model의 다른 활용

이 포스트에서는 LMM을 component contribution analysis에 사용했지만, 사실 LMM + LRT를 paired t-test와 RM-ANOVA 대신 사용하는 것도 가능하다. 실제로 paired t-test와 RM-ANOVA는 LMM의 special case이다.

LMM은 paired t-test와 RM-ANOVA가 처리하지 못하는 두 가지 상황을 커버한다. **(1) LMM은 missing/unbalanced data를 처리할 수 있다** (즉, 특정 참가자에서 특정 조건의 데이터가 없는 경우). paired t-test와 RM-ANOVA는 이 경우를 처리할 수 없다. **(2) LMM은 나이와 같은 continuous covariates을 control variable로 설정할 수 있다** (예: 나이가 많은 참가자가 조건과 무관하게 더 높은 점수를 내는 경향이 있다면, 나이를 포함시켜 모델이 이를 보정하게 함으로써 조건 효과를 더 정확하게 추정할 수 있다). 반대로 말하면, 원래 보고자 했던 main effect / pairwise comparison을 체크하면서 동시에 나이라는 factor의 significant effect까지도 함께 확인할 수 있다는 뜻이 된다. 즉, 상당히 유용한 분석을 가능하게 해준다는 점.

다만, HCI 연구에서 repeated-measures 유저 스터디로 데이터를 수집하게 되면 데이터 누락이 없는 balanced data를 확보하는 경우가 대부분이기 때문에, [paired t-test](https://taejunkim.com/posts?post=260617-paired-t-test-python)나 [one-way RM-ANOVA](https://taejunkim.com/posts?post=260615-one-way-rm-anova-python)로도 충분하다. Unbalanced data를 처리하거나 나이와 같은 continuous covariate를 통제해야 한다면 LMM + LRT를 사용해야 한다.

# 참고

- [statsmodels MixedLM](https://www.statsmodels.org/stable/generated/statsmodels.regression.mixed_linear_model.MixedLM.html)
- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [scipy.stats.chi2](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html)


# 변경 이력
- 2026년 6월 18일: 글 등록
