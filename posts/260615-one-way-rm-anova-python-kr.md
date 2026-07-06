---
title: Tutorial: One-way Repeated-Measures ANOVA with Python
date: 2026-06-15
tag: Statistics
---

One-way Repeated-Measures (Within-Subject) ANOVA를 돌리는 파이썬 코드를 공유한다. 실험 조건 중 하나라도 정규성 가정 (normality assumption)이 만족되지 않으면 [Friedman Test](/posts?post=260616-friedman-test-python)를 사용한다 (아래 2-2 참고).

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
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df = df.melt(id_vars=[subject_col], var_name='ExpCond', value_name='value')

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Sphericity Check Start
print("=== Sphericity Check ===")
aov = pg.rm_anova(data=df, dv='value', within='ExpCond', subject=subject_col, detailed=True)
F_val = aov['F'].values[0]
df_num = int(aov['DF'].values[0])
n_subjects = df[subject_col].nunique()
df_denom = (n_subjects - 1) * df_num
eps = aov['eps'].values[0]
p_unc = aov['p_unc'].values[0]
p_GG = stats.f.sf(F_val, df_num * eps, df_denom * eps)
eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
p_HF = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)

if len(conditions) <= 2:
    print("Sphericity: automatically satisfied (only 2 levels)")
    p_report, use_col = p_unc, 'p-unc'
else:
    spher_result = pg.sphericity(data=df, dv='value', within='ExpCond', subject=subject_col)
    W, p_spher = spher_result.W, spher_result.pval
    if p_spher > 0.05:
        p_report, use_col = p_unc, 'p-unc'
    elif eps < 0.75:
        p_report, use_col = p_GG, 'p-GG-corr'
    else:
        p_report, use_col = p_HF, 'p-HF-corr'
    p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
    eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
    print(f"Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}\n{p_cond} & {eps_cond} -> use {use_col}")

# One-way RM ANOVA Start
print("\n=== One-way RM ANOVA ===")
aov_effect = aov.iloc[[0]].copy()
aov_effect['df_denom'] = df_denom
aov_effect['p-GG-corr'] = p_GG
aov_effect['p-HF-corr'] = p_HF
p_col = 'p_unc' if use_col == 'p-unc' else use_col
print(aov_effect[['Source', 'DF', 'df_denom', 'F', p_col]].to_string(index=False, formatters={'F': '{:.6f}'.format, p_col: '{:.6f}'.format}))
print(f"\n→ p-value to report: {p_report:.6f} ({use_col})")

# Post-hoc Analysis Start
print("\n=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===")
pairwise_results = pg.pairwise_tests(dv='value', within='ExpCond', subject=subject_col, data=df, padjust='bonferroni')
print(pairwise_results[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

### 1) 데이터 준비

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df = df.melt(id_vars=[subject_col], var_name='ExpCond', value_name='value')
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
=== Normality Test ===
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

세 조건 모두 정규성이 만족됐으므로 RM ANOVA 테스트를 돌릴 수 있다. 조건 중 하나라도 정규성이 만족되지 않으면 [Friedman's test](/posts?post=260616-friedman-test-python)을 사용하는 것이 보수적인 선택이다.

### 3) 구형성 검정 (Sphericity Check)

```python
# Sphericity Check Start
aov = pg.rm_anova(data=df, dv='value', within='ExpCond', subject=subject_col, detailed=True)
F_val = aov['F'].values[0]
df_num = int(aov['DF'].values[0])
n_subjects = df[subject_col].nunique()
df_denom = (n_subjects - 1) * df_num
eps = aov['eps'].values[0]
p_unc = aov['p_unc'].values[0]
p_GG = stats.f.sf(F_val, df_num * eps, df_denom * eps)
eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
p_HF = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)

if len(conditions) <= 2:
    print("Sphericity: automatically satisfied (only 2 levels)")
    p_report, use_col = p_unc, 'p-unc'
else:
    spher_result = pg.sphericity(data=df, dv='value', within='ExpCond', subject=subject_col)
    W, p_spher = spher_result.W, spher_result.pval
    if p_spher > 0.05:
        p_report, use_col = p_unc, 'p-unc'
    elif eps < 0.75:
        p_report, use_col = p_GG, 'p-GG-corr'
    else:
        p_report, use_col = p_HF, 'p-HF-corr'
    p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
    eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
    print(f"Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}\n{p_cond} & {eps_cond} -> use {use_col}")
```

Output:

```
=== Sphericity Check ===
Sphericity (Mauchly's): W = 0.99, p-sphericity = 0.971, ε = 0.994
p-sphericity > 0.05 & ε ≥ 0.75 -> use p-unc
```

`pg.rm_anova()`를 먼저 실행해 `eps` (Greenhouse-Geisser epsilon)를 추출하고, 구형성 검정과 적절한 p-value를 확인한다.

- `p-unc`: 구형성이 만족될 때 (p-sphericity > 0.05), 또는 조건이 2개뿐일 때 (자동으로 구형성 만족)
- `p-GG-corr`: Greenhouse-Geisser 보정, 구형성이 위반됐을 때 (p-sphericity ≤ 0.05) & ε < 0.75
- `p-HF-corr`: Huynh-Feldt 보정, 구형성이 위반됐을 때 (p-sphericity ≤ 0.05) & ε ≥ 0.75

### 4) One-way Repeated Measures ANOVA

```python
aov_effect = aov.iloc[[0]].copy()
aov_effect['df_denom'] = df_denom
aov_effect['p-GG-corr'] = p_GG
aov_effect['p-HF-corr'] = p_HF
p_col = 'p_unc' if use_col == 'p-unc' else use_col
print(aov_effect[['Source', 'DF', 'df_denom', 'F', p_col]].to_string(index=False, formatters={'F': '{:.6f}'.format, p_col: '{:.6f}'.format}))
print(f"\n→ p-value to report: {p_report:.6f} ({use_col})")
```

Output:

```
=== One-way RM ANOVA ===
 Source  DF  df_denom        F    p_unc
ExpCond   2        22 4.662527 0.020504

→ p-value to report: 0.020504 (p-unc)
```

조건의 주효과 (main effect)가 유의한 것으로 확인됐다, F(2, 22) = 4.66, p < .05.

### 5) 사후 분석

```python
pairwise_results = pg.pairwise_tests(dv='value', within='ExpCond', subject=subject_col, data=df, padjust='bonferroni')
print(pairwise_results[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

ANOVA가 유의하므로, Bonferroni correction을 적용한 pairwise 비교로 어떤 조건 쌍에서 차이가 나는지 확인한다.

Output:

```
=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===
          A           B       T dof    p_unc   p_corr
Condition A Condition B -2.0841  11 0.061266 0.183797
Condition A Condition C -2.8835  11 0.014877 0.044632
Condition B Condition C -0.9698  11 0.352979 1.000000
```

Bonferroni correction을 적용한 pairwise 비교 결과, Condition A와 Condition C 사이에 유의미한 차이가 확인됐다 (t = -2.88, p < .05).

```note
**Bonferroni Correction에 관해:** p-value에 Bonferroni correction을 적용을 해야하는가 안해도 되는가는 꽤나 까다로운 문제이고, 결국 연구자 판단의 문제로 귀결된다 (책임도 연구자가 진다). Bonferroni를 적용하는 것은 가장 안전하고 보수적인 선택이며, 리뷰어가 지적할 가능성을 차단한다. 이론적으로 각 비교가 완전히 독립적인 질문이라면, 예를 들어 데이터 수집 이전 단계부터 미리 계획된 비교라면 correction이 필요하지 않다. 즉, 하나의 독립적인 주장을 뒷받침하기 위한 비교는 Bonferroni correction이 필요하지 않지만, 여러 비교가 함께 제시되고 독자가 이를 전체로 해석한다면 correction을 적용하는 것이 더 안전한 선택이다. 지금 상황처럼 "어떤 조건 간에 차이가 있는가?"라는 하나의 질문을 검정하기 위해 ANOVA 수행을 하고, 그 단일 질문에 이어지는 형태로 exploratory post hoc 후속 분석을 위해 3개 쌍에 대한 비교를 하고 있기에, 여기서 만약 correction을 하지 않는다면 지적받을 가능성이 높다. 다른 논리로 설득하려 해볼 수도 있겠지만 애초에 더 안전한 선택을 하는 게 좋다.
```

# 3. 결과 보고

```note
**Writing for report:** A one-way repeated-measures ANOVA revealed a significant main effect of condition (F(2, 22) = 4.66, p < .05). Post-hoc pairwise comparisons with Bonferroni correction showed a significant difference between Condition A and Condition C (t = -2.88, p < .05).
```

*Side Note: 몇 년전까지는 [SPSS](/posts?post=200203-spss-repeated-measures)로 통계 분석을 진행했는데, 언제부턴가 Python으로 완전히 넘어왔다. GUI 기반 프로그램들보다 각 스탭들이 더 투명하게 보이고, 가볍고, 확실히 전반적으로 더 편하다. 그리고 무엇보다 무료다.*

# 참고

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [pingouin rm_anova](https://pingouin-stats.org/generated/pingouin.rm_anova.html)
- [pingouin sphericity](https://pingouin-stats.org/generated/pingouin.sphericity.html)
- [pingouin pairwise_tests](https://pingouin-stats.org/generated/pingouin.pairwise_tests.html)

# 변경 이력
- 2026년 6월 15일: 글 등록
