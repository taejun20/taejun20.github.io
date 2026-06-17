---
title: Tutorial: Paired T-Test with Python
date: 2026-06-17
tag: Statistics
---

파이썬으로 대응 표본 t검정 (Paired T-Test)을 돌리는 방법을 공유한다. 같은 피험자로부터 두 조건을 측정하는 경우 (within-subject 디자인, 2개 조건)에 사용한다. 하나라도 정규성 가정이 만족되지 않으면 [Wilcoxon signed-rank test](/posts?post=260617-wilcoxon-signed-rank-python)를 사용한다 (아래 2-2 참고).

# 1. 데이터 정리

Google Spreadsheet로 데이터를 정리한다 (통계 테스트를 돌리기 전에 각 조건의 평균과 표준편차를 먼저 확인하면서 데이터에 대한 전반적인 감을 잡는다).

![|40%](img/posts/260617-paired-t-test-python/data-table.jpg)

정리된 표를 CSV 파일 (data.csv)로 저장하고, 아래 Python 스크립트 (main.py)와 같은 폴더에 위치시킨다.

<a href="/files/260617-paired-t-test-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Python 스크립트 실행

바로 돌려볼 수 있는 전체 스크립트를 먼저 첨부하였고, 이어서 각 파트에 대한 설명을 추가하였다.

<a href="/files/260617-paired-t-test-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
import pingouin as pg
from scipy import stats

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Paired T-Test Start
print("=== Paired T-Test ===")
result = pg.ttest(df[conditions[0]], df[conditions[1]], paired=True)
print(result[['T', 'dof', 'p_val', 'cohen_d']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_val': '{:.6f}'.format, 'cohen_d': '{:.4f}'.format}))
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
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

Paired t-test 같은 모수 검정 (parametric test)을 돌리기 전에, Shapiro-Wilk 검정으로 각 조건의 정규성을 확인한다. 귀무가설 (null hypothesis)은 정규분포를 따른다는 것이므로, p > 0.05이면 정규성이 만족된다고 본다.

Output:

```
=== Normality Test ===
ExpCond: Condition A 
Statistic: 0.9762, P-value: 0.9637
Data is normally distributed (fail to reject H0).

ExpCond: Condition B 
Statistic: 0.9561, P-value: 0.7264
Data is normally distributed (fail to reject H0).
```

두 조건 모두 정규성이 만족됐으므로 paired t-test를 진행한다. 조건 중 하나라도 정규성이 만족되지 않으면 [Wilcoxon signed-rank test](/posts?post=260617-wilcoxon-signed-rank-python)를 사용하는 것이 보수적인 선택이다.

### 3) 대응 표본 t검정 (Paired T-Test)

```python
result = pg.ttest(df[conditions[0]], df[conditions[1]], paired=True)
print(result[['T', 'dof', 'p_val', 'cohen_d']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_val': '{:.6f}'.format, 'cohen_d': '{:.4f}'.format}))
```

`pg.ttest()`에 `paired=True`를 설정하면 대응 표본 t검정을 실행한다. t통계량, 자유도 (dof = n - 1), p-value, 그리고 효과 크기인 Cohen's d를 출력한다.

Output:

```
=== Paired T-Test ===
      T dof    p_val cohen_d
-6.9663  11 0.000024  0.9860
```

두 조건 사이에 유의미한 차이가 확인됐다, t(11) = -6.97, p < .001, d = 0.99.

# 3. 결과 보고

```note
**Writing for report:** A paired t-test revealed a significant difference between Condition A and Condition B (t(11) = -6.97, p < .001).
```

*Side Note: 몇 년전까지는 [SPSS](/posts?post=200203-spss-repeated-measures)로 통계 분석을 진행했는데, 언제부턴가 Python으로 완전히 넘어왔다. GUI 기반 프로그램들보다 각 스탭들이 더 투명하게 보이고, 가볍고, 확실히 전반적으로 더 편하다. 그리고 무엇보다 무료다.*

# 참고

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [pingouin ttest](https://pingouin-stats.org/generated/pingouin.ttest.html)


# 변경 이력
- 2026년 6월 17일: 글 등록
