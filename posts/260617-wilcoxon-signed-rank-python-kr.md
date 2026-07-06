---
title: Tutorial: Wilcoxon Signed-Rank Test with Python
date: 2026-06-17
tag: Statistics
---

Wilcoxon signed-rank test를 돌리는 파이썬 코드를 공유한다. Wilcoxon signed-rank test는 하나 이상의 조건에서 정규성 가정이 만족되지 않을 때 사용한다. 모든 조건에서 정규성이 만족된다면 [대응 표본 t검정 (paired t-test)](/posts?post=260617-paired-t-test-python)을 사용한다 (아래 2-2 참고).

# 1. 데이터 정리

Google Spreadsheet로 데이터를 정리한다 (통계 테스트를 돌리기 전에 각 조건의 평균과 표준편차를 먼저 확인하면서 데이터에 대한 전반적인 감을 잡는다).

![|40%](img/posts/260617-wilcoxon-signed-rank-python/data-table.jpg)

정리된 표를 CSV 파일 (data.csv)로 저장하고, 아래 Python 스크립트 (main.py)와 같은 폴더에 위치시킨다.

<a href="/files/260617-wilcoxon-signed-rank-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Python 스크립트 실행

바로 돌려볼 수 있는 전체 스크립트를 먼저 첨부하였고, 이어서 각 파트에 대한 설명을 추가하였다.

<a href="/files/260617-wilcoxon-signed-rank-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
from scipy.stats import shapiro, wilcoxon

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Wilcoxon Signed-Rank Test Start
print("=== Wilcoxon Signed-Rank Test ===")
result = wilcoxon(df[conditions[0]], df[conditions[1]], method='approx')
print(f"Z = {result.zstatistic:.4f}, P-value = {result.pvalue:.6f}")
```

### 1) 데이터 준비

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
```

`pd.read_csv`로 wide format의 CSV를 불러온다.

### 2) 정규성 검정

```python
for cond in conditions:
    stat, p_value = shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

어떤 테스트를 사용할지 결정하기 전에, Shapiro-Wilk 검정으로 각 조건의 정규성을 확인한다. 귀무가설 (null hypothesis)은 정규분포를 따른다는 것이므로, p > 0.05이면 정규성이 만족된다고 본다.

Output:

```
=== Normality Test ===
ExpCond: Condition A 
Statistic: 0.5588, P-value: 0.0000
Data is not normally distributed (reject H0).

ExpCond: Condition B 
Statistic: 0.9177, P-value: 0.2676
Data is normally distributed (fail to reject H0).
```

Condition A가 정규성 가정을 만족하지 못하므로, 대응 표본 t검정 대신 Wilcoxon signed-rank test를 사용한다. 두 조건 모두 정규성을 만족한다면 [대응 표본 t검정 (paired t-test)](/posts?post=260617-paired-t-test-python)을 사용한다.

### 3) Wilcoxon Signed-Rank Test

```python
result = wilcoxon(df[conditions[0]], df[conditions[1]], method='approx')
print(f"Z = {result.zstatistic:.4f}, P-value = {result.pvalue:.6f}")
```

`method='approx'`는 정규 근사를 사용해 z통계량을 계산한다. Z값을 보고하려면 이 옵션이 필요하다.

Output:

```
=== Wilcoxon Signed-Rank Test ===
Z = -3.0594, P-value = 0.002218
```

두 조건 사이에 유의미한 차이가 확인됐다 (Z = -3.06, p < .01).

# 3. 결과 보고

```note
**Writing for report:** A Wilcoxon signed-rank test revealed a significant difference between Condition A and Condition B (Z = -3.06, p < .01).
```

*Side Note: 몇 년전까지는 [SPSS](/posts?post=200203-spss-repeated-measures)로 통계 분석을 진행했는데, 언제부턴가 Python으로 완전히 넘어왔다. GUI 기반 프로그램들보다 각 스탭들이 더 투명하게 보이고, 가볍고, 확실히 전반적으로 더 편하다. 그리고 무엇보다 무료다.*

# 참고

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [scipy.stats.wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)


# 변경 이력
- 2026년 6월 17일: 글 등록
