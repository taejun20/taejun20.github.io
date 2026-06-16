---
title: Tutorial: Two-way Repeated-Measures ANOVA with Python
date: 2026-06-16
tag: Statistics
---

파이썬으로 Two-way Repeated-Measures (Within-Subject) ANOVA를 돌리는 방법을 공유한다. 두 개의 within-subject factor (= 2개의 독립 변수)이 있을 때 사용한다. 정규성 가정이 만족되지 않는 경우 [Aligned Rank Transform](/posts?post=210903-aligned-rank-transform)을 사용한다 (정규성 검정은 아래 2-2 참고).

```note
**라이브러리 한계점:** 이 튜토리얼에서 사용하는 `pingouin` 라이브러리는 within-subject factor를 최대 두 개까지만 지원한다. Three-way 또는 Four-way RM ANOVA가 필요한 경우 R (`afex` 또는 `ez` 패키지)을 사용하자.
```

# 1. 데이터 정리

Google Spreadsheet로 데이터를 정리한다 (통계 테스트를 돌리기 전에 각 조건의 평균과 표준편차를 먼저 확인하면서 데이터에 대한 전반적인 감을 잡는다).

![|80%](img/posts/260616-two-way-rm-anova-python/data-table.jpg)

독립 변수 (= independent variable = factor) A와 B가 있다. A는 두 개의 levels (A1, A2), B는 세 개의 levels (B1, B2, B3)을 가지며, 따라서 총 여섯 개의 실험 조건 (A1_B1, A1_B2, A1_B3, A2_B1, A2_B2, A2_B3)이 있다. 예제 데이터가 아닌 실제 본인의 데이터를 사용할 때에는 csv 파일의 column 이름을 본인의 factor의 level에 맞게 입력하고 `_`로 구분해서 저장한다 (main.py가 `_`를 기준으로 factor를 구분한다).

예시:
- type (Controller, Pinch) x power (5, 10): `Controller_5`, `Pinch_5`, `Controller_10`, `Pinch_10`
- device (Phone, Watch) x size (Small, Large): `Phone_Small`, `Watch_Small`, `Phone_Large`, `Watch_Large`
- difficulty (Easy, Hard) x speed (Slow, Fast): `Easy_Slow`, `Easy_Fast`, `Hard_Slow`, `Hard_Fast`

정리된 표를 CSV 파일 (data.csv)로 저장하고, 아래 Python 스크립트 (main.py)와 같은 폴더에 위치시킨다.

<a href="/files/260616-two-way-rm-anova-python/data.csv" download="data.csv" class="btn-download">⬇ Download data.csv</a>


# 2. Python 스크립트 실행

바로 돌려볼 수 있는 전체 스크립트를 먼저 첨부하였고, 이어서 각 파트에 대한 단계별 설명을 추가하였다.

<a href="/files/260616-two-way-rm-anova-python/main.py" download="main.py" class="btn-download">⬇ Download main.py</a>

```python
import pandas as pd
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
factor_cols = [f'Factor{chr(65+i)}' for i in range(len(conditions[0].split('_')))]
for i, col in enumerate(factor_cols):
    df_long[col] = df_long['Condition'].str.split('_').str[i]

# Perform normality test for each condition
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

print("=== Two-way RM ANOVA ===")
# perform two-way RM ANOVA
aov = pg.rm_anova(data=df_long, dv='value', within=factor_cols, subject=subject_col, detailed=True)
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc']].to_string(index=False))

print("\n=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===")
# post-hoc: pairwise t-test with Bonferroni correction

# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant: main effects post-hoc ===")
print(f"\nPost-hoc {factor_cols[0]}:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print(f"\nPost-hoc {factor_cols[1]} (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))

# 2) when interaction effect IS significant:
#    can't average out; one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print(f"\nSimple effects: {factor_cols[0]} within each {factor_cols[1]} level:")
for b in sorted(df_long[factor_cols[1]].unique()):
    subset = df_long[df_long[factor_cols[1]] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[1]} = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print(f"\nSimple effects: {factor_cols[1]} within each {factor_cols[0]} level (Bonferroni):")
for a in sorted(df_long[factor_cols[0]].unique()):
    subset = df_long[df_long[factor_cols[0]] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[0]} = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

### 1) 데이터 준비

```python
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
factor_cols = [f'Factor{chr(65+i)}' for i in range(len(conditions[0].split('_')))]
for i, col in enumerate(factor_cols):
    df_long[col] = df_long['Condition'].str.split('_').str[i]
```

`pd.read_csv`로 wide format의 CSV를 불러오고, `melt`로 long format으로 변환한다. 이후 각 조건 이름을 `_` 기준으로 분리해 요인을 자동으로 추출한다. 예를 들어 `Controller_Easy`는 FactorA=`Controller`, FactorB=`Easy`가 된다.

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

모수 검정을 진행하기 전에 Shapiro-Wilk 검정으로 각 조건의 정규성을 확인한다. 귀무가설은 정규분포를 따른다는 것이므로, p > 0.05이면 정규성이 만족된다고 본다.

Output:

```
=== Normality Test ===
ExpCond: A1_B1 
Statistic: 0.9489, P-value: 0.6208
Data is normally distributed (fail to reject H0).

ExpCond: A1_B2 
Statistic: 0.9402, P-value: 0.5010
Data is normally distributed (fail to reject H0).

ExpCond: A1_B3 
Statistic: 0.9185, P-value: 0.2738
Data is normally distributed (fail to reject H0).

ExpCond: A2_B1 
Statistic: 0.9781, P-value: 0.9752
Data is normally distributed (fail to reject H0).

ExpCond: A2_B2 
Statistic: 0.9823, P-value: 0.9912
Data is normally distributed (fail to reject H0).

ExpCond: A2_B3 
Statistic: 0.9347, P-value: 0.4327
Data is normally distributed (fail to reject H0).
```

모든 조건이 정규성 가정을 만족하므로 Two-way RM ANOVA를 진행한다.

### 3) Two-way Repeated-Measures ANOVA

```python
aov = pg.rm_anova(data=df_long, dv='value', within=factor_cols, subject=subject_col, detailed=True)
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc']].to_string(index=False))
```

Output:

```
=== Two-way RM ANOVA ===
          Source  ddof1  ddof2           F         p_unc
         FactorA      1     11   83.660621  1.789109e-06
         FactorB      2     22  285.201389  1.852941e-16
 FactorA * FactorB      2     22    3.019793  6.936843e-02
```

두 factor의 main effect 모두 유의하다. 인터랙션 효과 (FactorA * FactorB)는 유의하지 않다 (p = .069). 인터랙션 효과 (interaction effects)에 대해서는 [이 포스트](/posts?post=200903-interaction-effects-anova) 참고.

### 4) 사후 분석

**Case 1: 인터랙션 효과가 유의하지 않은 경우.** 인터랙션 효과가 유의하지 않으므로 각 factor의 main effect를 독립적으로 해석할 수 있다. 다른 factor에 대해 평균을 내고 원하는 factor의 주 효과를 비교하는 main effects 분석을 수행한다.

Factor A는 수준이 두 개뿐이므로 correction이 필요하지 않다. Factor B는 수준이 세 개이므로 3개의 pairwise 비교에 Bonferroni correction을 적용한다:

```python
# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant: main effects post-hoc ===")
print(f"\nPost-hoc {factor_cols[0]}:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print(f"\nPost-hoc {factor_cols[1]} (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

Output:

```
=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===

=== Case 1: Interaction NOT significant: main effects post-hoc ===

Post-hoc FactorA:
 A  B      T dof    p_unc
A1 A2 9.1466  11 0.000002

Post-hoc FactorB (Bonferroni):
 A  B        T dof    p_unc   p_corr
B1 B2 -12.8856  11 0.000000 0.000000
B1 B3 -19.8949  11 0.000000 0.000000
B2 B3 -14.0944  11 0.000000 0.000000
```

Factor B의 모든 pairwise 비교가 Bonferroni correction 적용 후에도 유의하다.

**Case 2: 인터랙션 효과가 유의한 경우.** 한 factor의 효과가 다른 factor의 level에 따라 달라지므로 평균을 낼 수 없다. 한 factor의 level을 고정하고 다른 factor내 level을 비교하는 단순 효과 (simple effects) 분석을 수행한다.

```python
# 2) when interaction effect IS significant:
#    can't average out; one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print(f"\nSimple effects: {factor_cols[0]} within each {factor_cols[1]} level:")
for b in sorted(df_long[factor_cols[1]].unique()):
    subset = df_long[df_long[factor_cols[1]] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[1]} = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print(f"\nSimple effects: {factor_cols[1]} within each {factor_cols[0]} level (Bonferroni):")
for a in sorted(df_long[factor_cols[0]].unique()):
    subset = df_long[df_long[factor_cols[0]] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[0]} = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
```

Output:

```
=== Case 2: Interaction IS significant — simple effects ===

Simple effects: FactorA within each FactorB level:
  FactorB = B1:
 A  B      T dof    p_unc
A1 A2 3.0580  11 0.010890
  FactorB = B2:
 A  B      T dof    p_unc
A1 A2 3.9275  11 0.002362
  FactorB = B3:
 A  B      T dof    p_unc
A1 A2 6.8099  11 0.000029

Simple effects: FactorB within each FactorA level (Bonferroni):
  FactorA = A1:
 A  B        T dof    p_unc   p_corr
B1 B2  -7.5889  11 0.000011 0.000032
B1 B3 -17.2285  11 0.000000 0.000000
B2 B3  -7.6518  11 0.000010 0.000030
  FactorA = A2:
 A  B       T dof    p_unc   p_corr
B1 B2 -6.2209  11 0.000065 0.000196
B1 B3 -9.3722  11 0.000001 0.000004
B2 B3 -7.9306  11 0.000007 0.000021
```

```note
**Bonferroni Correction에 관해:** p-value에 Bonferroni correction을 적용을 해야하는가 안해도 되는가는 꽤나 까다로운 문제이고, 결국 연구자 판단의 문제로 귀결된다 (책임도 연구자가 진다). Bonferroni를 적용하는 것은 가장 안전하고 보수적인 선택이며, 리뷰어가 지적할 가능성을 차단한다. 이론적으로 각 비교가 완전히 독립적인 질문이라면, 예를 들어 데이터 수집 이전 단계부터 미리 계획된 비교라면 correction이 필요하지 않다. 즉, 하나의 독립적인 주장을 뒷받침하기 위한 비교는 Bonferroni correction이 필요하지 않지만, 여러 비교가 함께 제시되고 독자가 이를 전체로 해석한다면 correction을 적용하는 것이 더 안전한 선택이다. ANOVA 자체는 "어떤 조건 간에 차이가 있는가?"라는 하나의 질문을 검정하고, post-hoc 비교는 그 단일 질문에 이어지는 후속 분석이다. 이는 correction을 생략하는 것에 대한 강력한 반론이 된다. 더 안전한 선택을 하는 게 좋다.
```

# 3. 결과 보고

Case 1과 Case 2를 모두 보여주었지만, 본 예제에서 사용된 데이터의 경우 인터랙션 효과가 유의하지 않으므로 Case 1이 적용된다. 아래 writing은 Case 1 분석을 기반으로 작성했다:

```note
**Writing for report:** A two-way repeated-measures ANOVA revealed a significant main effect of Factor A (F(1, 11) = 83.66, p < .001) and a significant main effect of Factor B (F(2, 22) = 285.20, p < .001). The interaction effect was not significant. Post-hoc pairwise comparisons showed that A1 was significantly slower than A2 (t = 9.15, p < .001). For Factor B, all pairwise comparisons were significant after Bonferroni correction: B1 vs B2 (t = -12.89, p < .001), B1 vs B3 (t = -19.89, p < .001), and B2 vs B3 (t = -14.09, p < .001).
```

*Side Note: 몇 년전까지는 [SPSS](/posts?post=200420-spss-two-way-anova)로 통계 분석을 진행했는데, 언제부턴가 Python으로 완전히 넘어왔다. GUI 기반 프로그램들보다 각 스탭들이 더 투명하게 보이고, 가볍고, 확실히 전반적으로 더 편하다. 그리고 무엇보다 무료다.*

# 참고

- [scipy.stats.shapiro](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html)
- [pingouin rm_anova](https://pingouin-stats.org/generated/pingouin.rm_anova.html)
- [pingouin pairwise_tests](https://pingouin-stats.org/generated/pingouin.pairwise_tests.html)

# 변경 이력
- 2026년 6월 16일: 글 등록
