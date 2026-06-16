---
title: Tutorial: Friedman Test with Python
date: 2026-06-16
tag: Statistics
---

파이썬으로 Friedman test를 돌리는 방법을 공유한다. Friedman test는 하나 이상의 실험 조건의 데이터가 정규성 가정을 만족하지 못할 때 사용한다. 모든 실험 조건에서 정규성을 만족한다면 [RM ANOVA](/posts?post=260615-one-way-rm-anova-python)를 사용한다 (아래 2-2 참고).

# 1. 데이터 정리

Google Spreadsheet로 데이터를 정리한다 (통계 테스트를 돌리기 전에 각 조건의 평균과 표준편차를 먼저 확인하면서 데이터에 대한 전반적인 감을 잡는다).

![|50%](img/posts/260616-friedman-test-python/data-table.jpg)

정리된 표를 CSV 파일 (data.csv)로 저장하고, 아래 Python 스크립트 (main.py)와 같은 폴더에 위치시킨다.

<a href="/files/260616-friedman-test-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>

# 2. Python 스크립트 실행

바로 돌려볼 수 있는 전체 스크립트를 먼저 첨부하였고, 이어서 각 파트에 대한 단계별 설명을 추가하였다.

<a href="/files/260616-friedman-test-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
from itertools import combinations
from scipy.stats import shapiro, friedmanchisquare, wilcoxon
from statsmodels.stats.multitest import multipletests

# read csv (wide format)
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Perform normality test for each condition
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = shapiro(df[cond].values)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

print("=== Friedman Test ===")
# perform Friedman test
stat, p_value = friedmanchisquare(*[df[cond].values for cond in conditions])
df_val = len(conditions) - 1
print(f"Friedman Test \ndf: {df_val}, Statistic (chi-square): {stat:.4f}, P-value: {p_value:.6f}")
if p_value < 0.05:
    print("There is a statistically significant difference between conditions.")
else:
    print("No statistically significant difference between conditions.")

print("\n=== Post-hoc Analysis (Wilcoxon signed-rank test with Bonferroni correction) ===")
# post-hoc: Wilcoxon signed-rank test with Bonferroni correction
pairwise_p = []
pairwise_z = []
comparisons = list(combinations(range(len(conditions)), 2))

for i, j in comparisons:
    res = wilcoxon(df[conditions[i]].values, df[conditions[j]].values, method='approx')
    pairwise_p.append(res.pvalue)
    pairwise_z.append(res.zstatistic)

corrected_pvals = multipletests(pairwise_p, method='bonferroni')[1]

for (i, j), z, p_val in zip(comparisons, pairwise_z, corrected_pvals):
    print(f"{conditions[i]} vs {conditions[j]}: Z = {z:.4f}, Adjusted P-value = {p_val:.6f}")
```

### 1) 데이터 준비

```python
# read csv (wide format)
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
```

`pd.read_csv`로 wide format의 CSV를 불러온다.

### 2) 정규성 검정

```python
for cond in conditions:
    stat, p_value = shapiro(df[cond].values)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

어떤 검정을 사용할지 결정하기 전에, Shapiro-Wilk 검정으로 각 조건의 정규성을 확인한다. 귀무가설 (null hypothesis)은 정규분포를 따른다는 것이므로, p > 0.05이면 정규성이 만족된다고 본다.

Output:

```
=== Normality Test ===
ExpCond: Condition A 
Statistic: 0.5588, P-value: 0.0000
Data is not normally distributed (reject H0).

ExpCond: Condition B 
Statistic: 0.9177, P-value: 0.2676
Data is normally distributed (fail to reject H0).

ExpCond: Condition C 
Statistic: 0.9427, P-value: 0.5339
Data is normally distributed (fail to reject H0).
```

Condition A가 정규성을 만족하지 못하므로, RM ANOVA 대신 전체 데이터에 Friedman test를 적용한다.

### 3) Friedman Test

```python
stat, p_value = friedmanchisquare(*[df[cond].values for cond in conditions])
df_val = len(conditions) - 1
print(f"Friedman Test \ndf: {df_val}, Statistic (chi-square): {stat:.4f}, P-value: {p_value:.6f}")
if p_value < 0.05:
    print("There is a statistically significant difference between conditions.")
else:
    print("No statistically significant difference between conditions.")
```

자유도 (df) = 조건 수 − 1.

Output:

```
=== Friedman Test ===
Friedman Test 
df: 2, Statistic (chi-square): 18.1667, P-value: 0.000114
There is a statistically significant difference between conditions.
```

조건의 주효과가 유의한 것으로 확인됐다, χ²(2) = 18.17, p < .001.

### 4) 사후 분석

```python
pairwise_p = []
pairwise_z = []
comparisons = list(combinations(range(len(conditions)), 2))

for i, j in comparisons:
    res = wilcoxon(df[conditions[i]].values, df[conditions[j]].values, method='approx')
    pairwise_p.append(res.pvalue)
    pairwise_z.append(res.zstatistic)

corrected_pvals = multipletests(pairwise_p, method='bonferroni')[1]

for (i, j), z, p_val in zip(comparisons, pairwise_z, corrected_pvals):
    print(f"{conditions[i]} vs {conditions[j]}: Z = {z:.4f}, Adjusted P-value = {p_val:.6f}")
```

주효과가 유의하므로, Bonferroni correction을 적용한 pairwise Wilcoxon signed-rank test로 어떤 조건 쌍에서 차이가 나는지 확인한다.

Output:

```
=== Post-hoc Analysis (Wilcoxon signed-rank test with Bonferroni correction) ===
Condition A vs Condition B: Z = -3.0594, Adjusted P-value = 0.006653
Condition A vs Condition C: Z = -3.0594, Adjusted P-value = 0.006653
Condition B vs Condition C: Z = -1.1767, Adjusted P-value = 0.717950
```

Bonferroni correction을 적용한 pairwise 비교 결과, Condition A와 Condition B (Z = -3.06, p < .01), Condition A와 Condition C (Z = -3.06, p < .01) 사이에 유의미한 차이가 확인됐다.

```note
**Bonferroni Correction에 관해:** p-value에 Bonferroni correction을 적용을 해야하는가 안해도 되는가는 꽤나 까다로운 문제이고, 결국 연구자 판단의 문제로 귀결된다 (책임도 연구자가 진다). Bonferroni를 적용하는 것은 가장 안전하고 보수적인 선택이며, 리뷰어가 지적할 가능성을 차단한다. 이론적으로 각 비교가 완전히 독립적인 질문이라면, 예를 들어 데이터 수집 이전 단계부터 미리 계획된 비교라면 correction이 필요하지 않다. 즉, 하나의 독립적인 주장을 뒷받침하기 위한 비교는 Bonferroni correction이 필요하지 않지만, 여러 비교가 함께 제시되고 독자가 이를 전체로 해석한다면 correction을 적용하는 것이 더 안전한 선택이다. 지금 상황처럼 "어떤 조건 간에 차이가 있는가?"라는 하나의 질문을 검정하기 위해 Friedman test 수행을 하고, 그 단일 질문에 이어지는 형태로 exploratory post hoc 후속 분석을 위해 3개 쌍에 대한 비교를 하고 있기에, 여기서 만약 correction을 하지 않는다면 지적받을 가능성이 높다. 다른 논리로 설득하려 해볼 수도 있겠지만 애초에 더 안전한 선택을 하는 게 좋다.
```

# 3. 결과 보고

```note
**Writing for report:** A Friedman test revealed a significant effect of condition (χ²(2) = 18.17, p < .001). Post-hoc pairwise Wilcoxon signed-rank tests with Bonferroni correction showed significant differences between Condition A and Condition B (Z = -3.06, p < .01), and between Condition A and Condition C (Z = -3.06, p < .01).
```

*Side Note: 몇 년전까지는 [SPSS](/posts?post=200203-spss-repeated-measures)로 통계 분석을 진행했는데, 언제부턴가 Python으로 완전히 넘어왔다. GUI 기반 프로그램들보다 각 스탭들이 더 투명하게 보이고, 가볍고, 확실히 전반적으로 더 편하다. 그리고 무엇보다 무료다.*

# 참고

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [scipy.stats.friedmanchisquare](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.friedmanchisquare.html)
- [scipy.stats.wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)
- [statsmodels multipletests](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)

# 변경 이력
- 2026년 6월 16일: 글 등록
