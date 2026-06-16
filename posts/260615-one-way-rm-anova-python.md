---
title: Tutorial: One-way Repeated-Measures ANOVA with Python
date: 2026-06-15
tag: Statistics
---

파이썬으로 One-way Repeated-Measures (Within-Subject) ANOVA를 돌려보는 튜토리얼을 공유한다. Within-subject 실험은 Between-subject 실험보다 훨씬 적은 피험자 수로 독립 변수의 통계적 유의성을 확인할 수 있다는 장점이 있다.

# 1. 데이터 정리

Google Spreadsheet로 데이터를 정리한다 (통계 테스트를 돌리기 전에 각 조건의 평균과 표준편차를 먼저 확인하면서 데이터에 대한 전반적인 감을 잡는다).

![|50%](img/posts/260615-one-way-rm-anova-python/data-table.jpg)

정리된 표를 CSV 파일 (data.csv)로 저장하고, 아래 Python 스크립트 (main.py)와 같은 폴더에 위치시킨다.

<a href="/files/260615-one-way-rm-anova-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>

# 2. Python 스크립트 실행

바로 돌려볼 수 있는 전체 스크립트를 먼저 첨부하였고, 이어서 각 파트에 대한 단계별 설명을 추가하였다.

<a href="/files/260615-one-way-rm-anova-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
df = df.melt(id_vars=['Participant'], var_name='ExpCond', value_name='value')

# define conditions
conditions = ["Condition A", "Condition B", "Condition C"]

# Perform normality test for each condition
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# perform RM-ANOVA: statsmodels AnovaRM
testingMeasure = 'value'
anovaRM = AnovaRM(data=df, depvar=testingMeasure, subject='Participant', within=['ExpCond'])
res = anovaRM.fit()
print(res)

# post-hoc: pairwise t-test with Bonferroni correction
pairwise_results = pg.pairwise_ttests(dv=testingMeasure, within='ExpCond', subject='Participant', data=df, padjust='bonferroni')
pg.print_table(pairwise_results)
```

### 1) 데이터 준비

```python
df = pd.read_csv("data.csv")
df = df.melt(id_vars=['Participant'], var_name='ExpCond', value_name='value')
```

`pd.read_csv`로 wide format의 CSV를 불러온 뒤, `melt`로 ANOVA 함수가 요구하는 long format으로 변환한다.

### 2) 정규성 검정

```python
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")
```

RM ANOVA 같은 모수 검정 (parametric test)을 돌리기 전에, Shapiro-Wilk 검정으로 각 조건의 정규성을 확인한다. 귀무가설 (null hypothesis)은 정규분포를 따른다는 것이므로, p > 0.05이면 정규성이 만족된다고 본다.

Output:

```
ExpCond: Condition A 
Statistic: 0.9532, P-value: 0.6846
Data is normally distributed (fail to reject H0).

ExpCond: Condition B 
Statistic: 0.9177, P-value: 0.2676
Data is normally distributed (fail to reject H0).

ExpCond: Condition C 
Statistic: 0.9427, P-value: 0.5339
Data is normally distributed (fail to reject H0).
```

세 조건 모두 정규성이 만족됐으므로 RM ANOVA로 넘어간다. 조건 중 하나라도 정규성이 만족되지 않으면, 전체 데이터에 비모수 검정 (Friedman's test)을 사용하는 것이 보수적인 선택이다.

### 3) One-way Repeated Measures ANOVA

```python
testingMeasure = 'value'
anovaRM = AnovaRM(data=df, depvar=testingMeasure, subject='Participant', within=['ExpCond'])
res = anovaRM.fit()
print(res)
```

Output:

```
                Anova
=====================================
        F Value Num DF  Den DF Pr > F
-------------------------------------
ExpCond  4.6625 2.0000 22.0000 0.0205
=====================================
```

조건의 주효과가 유의한 것으로 확인됐다, F(2, 22) = 4.66, p < .05.

### 4) 사후 분석

```python
pairwise_results = pg.pairwise_ttests(dv=testingMeasure, within='ExpCond', subject='Participant', data=df, padjust='bonferroni')
pg.print_table(pairwise_results)
```

ANOVA가 유의하므로, Bonferroni correction을 적용한 pairwise 비교로 어떤 조건 쌍에서 차이가 나는지 확인한다.

Output:

```
Contrast    A            B            Paired    Parametric         T     dof  alternative      p_unc    p_corr  p_adjust      BF10    hedges
----------  -----------  -----------  --------  ------------  ------  ------  -------------  -------  --------  ----------  ------  --------
ExpCond     Condition A  Condition B  True      True          -2.084  11.000  two-sided        0.061     0.184  bonferroni   1.421    -0.800
ExpCond     Condition A  Condition C  True      True          -2.884  11.000  two-sided        0.015     0.045  bonferroni   4.294    -1.266
ExpCond     Condition B  Condition C  True      True          -0.970  11.000  two-sided        0.353     1.000  bonferroni   0.426    -0.440
```

Bonferroni correction을 적용한 pairwise 비교 결과, Condition A와 Condition C 사이에 유의미한 차이가 확인됐다 (t = -2.88, p < .05).

# 3. 결과 보고

```note
**Writing for report:** A one-way repeated-measures ANOVA revealed a significant main effect of condition (F(2, 22) = 4.66, p < .05). Post-hoc pairwise comparisons with Bonferroni correction showed a significant difference between Condition A and Condition C (t = -2.88, p < .05).
```

*Side Note: 몇 년전까지는 SPSS로 통계 분석을 진행했는데, 언제부턴가 Python으로 완전히 넘어왔다. GUI 기반 프로그램들보다 각 스탭들이 더 투명하게 보이고, 가볍고, 확실히 전반적으로 더 편하다. 그리고 무엇보다 무료다.*

# 참고

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [statsmodels AnovaRM](https://www.statsmodels.org/stable/generated/statsmodels.stats.anova.AnovaRM.html)
- [pingouin pairwise_tests](https://pingouin-stats.org/generated/pingouin.pairwise_tests.html)

# 변경 이력
- 2026년 6월 15일: 글 등록
