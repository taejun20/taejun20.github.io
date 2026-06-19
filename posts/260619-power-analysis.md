---
title: Understanding Power Analysis: Sample Size and Effect Size
date: 2026-06-19
tag: Statistics
---

파워 분석 (power analysis)는 표본 크기 분석 (sample size analysis; "실험에 참가자가 몇 명 필요한가?")와 민감도 분석 (sensitivity analysis; "참가자 수가 이미 결정됐을 때, 안정적으로 감지할 수 있는 최소의 effect size는 어느 정도인가?")를 위한 통계적 프레임워크다.

HCI 연구자에게 파워 분석은 유저 스터디 설계 단계에서도 도움이 되고, 또 이미 수집된 데이터에 대한 리뷰어의 sample size 지적에 대응할 때 필수적으로 알아야 한다.

# 1. 네 가지 파라미터

- **α (유의 수준)**: 실제로 없는 효과를 감지할 확률. About false positive we tolerate. 일반적으로 .05로 설정된다.
- **Power (검정력)**: 실제 효과가 존재할 때 이를 올바르게 감지할 확률. About false negative we tolerate. 일반적으로 .80으로 설정된다 (실제 효과를 놓칠 확률 20%를 허용한다는 의미다).
- **Effect size (효과 크기)**: 조건 간 차이가 얼마나 큰지.
- **n**: 표본 크기. HCI 유저 스터디에서는 피험자 수.

이 네 가지는 수학적으로 연결되어 있어서, 셋을 고정하면 나머지 하나를 구할 수 있다. 나아가 α = .05와 power = .80은 거의 모든 연구에서 사용하는 표준 관례이므로, 실제로는 두 가지로 좁혀진다:

- 예상되는 effect size가 주어졌을 때 → 참가자 (n)가 몇 명 필요한가? (sample size analysis)
- n이 고정되어 있을 때 → 신뢰할 수 있게 감지할 수 있는 최소 effect size는? (sensitivity analysis)

## 효과 크기 (Effect Size)

Effect Size는 조건 간 차이가 얼마나 큰지를 나타낸다. Paired t-test에서는 Cohen's d, RM-ANOVA에서는 Cohen's f, Wilcoxon signed-rank test에서는 rank-biserial correlation (r), Friedman test에서는 Kendall's W를 사용한다.

Cohen's d 기준:

| Effect Size | Cohen's d | 표본 크기 (n) | 의미 |
|-------------|-----------|-----------------|------|
| Small | 0.2 | 199 | 미묘한 차이로, 섬세한 측정 없이는 알아차리기 어려움 |
| Medium | 0.5 | 34 | 중간 수준, 실제로 체감 가능 |
| Large | 0.8 | 15 | 뚜렷한 차이, 확실하게 보임 |

```note
**중요:** effect size와 p-value는 완전히 다른 지표이다. p-value는 차이가 통계적으로 유의미한지를 나타낸다. 효과 크기는 그 차이가 실제로 얼마나 큰지를 나타낸다. 즉, p-value는 차이가 큰지 작은지에 대해서는 아무것도 말하지 않는다. 효과 크기가 그것을 말해준다.

n이 정말 커지면, 아무리 작은 효과 (d = 0.01)도 결국 p < .05가 된다. 통계적으로는 유의하지만 실질적으로는 무의미한 결과인 것이다. 그래서 통계학자들은 p-value와 함께 effect size를 보고할 것을 권장한다.
```

# 2. 표본 크기 분석 (Sample Size Analysis)

Sample Size Analysis는 이 질문에 답한다: 예상 효과 크기가 주어졌을 때, 참가자가 몇 명 필요한가?

가장 어려운 부분은 데이터 수집 전 (HCI에서는 유저 스터디 실행 전)에 예상되는 effect size를 추정하는 것이다. 세 가지 방법이 있다:

1. **선행 연구 참고하기**: 이미 출판된 논문 중에 비슷한 task와 실험 디자인을 가진 연구를 찾는다. 저자들이 Effect size를 직접 보고하지 않았더라도 t, F, Z 값 등 보고된 통계량으로부터 역산할 수 있다:


2. **파일럿 스터디로 근사하기**: 5~10명을 대상으로 먼저 파일럿을 진행하고, 거기서 수집된 데이터로 effect size를 계산한다. 주의해야 할 점은, 적은 sample size를 통해 얻어진 effect size는 불안정하고 실제 효과를 overestimate하는 경향이 있다는 점이 있다 (그래서 좀 더 보수적으로, 예를 들어 얻어진 effect size 값보다 약간 더 작은 값을 사용하는 방식으로 대응하면 안전하다).

3. **Cohen의 중간 효과 크기 기본값 사용**: 효과 크기에 대한 선행 추정치도 없고 파일럿 스터디도 없을 때는 d = 0.5를 기본값으로 사용할 수 있다 (이 경우 자동으로 필요한 sample size가 34명으로 도출된다).

아래는 paired t-test에 대한 power analysis을 실행하는 Python 코드를 공유한다:

```python
from statsmodels.stats.power import TTestPower
import math

analysis = TTestPower()

d = 0.5  # 예상 Cohen's d (medium)
n = analysis.solve_power(effect_size=d, alpha=0.05, power=0.80, alternative='two-sided')
print(f"필요한 n: {math.ceil(n)}")
```

Output:

```
필요한 n: 34
```

effect size가 작을수록 statistical significance를 보기 위해 더 많은 참가자가 필요하다. 작은 effect size (d = 0.2)에서는 약 200명이나 필요하다는 것을 알 수 있다.

# 3. 민감도 분석 (Sensitivity Analysis)

민감도 분석은 이 질문에 답한다: n이 고정되어 있을 때, 신뢰할 수 있게 감지할 수 있는 최소 효과 크기 (MDES, Minimum Detectable Effect Size)는?

표본 크기가 이미 고정된 경우에 유용하다. MDES를 계산하여 실험의 통계적 검정력이 충분한지 판단한다.

```python
from statsmodels.stats.power import TTestPower
import math

analysis = TTestPower()

n = 12
mdes = analysis.solve_power(nobs=n, alpha=0.05, power=0.80, alternative='two-sided')
print(f"Minimum Detectable Effect Size (MDES) for n={n}: d = {mdes:.2f}")
```

Output:

```
n=12일 때 Minimum Detectable Effect Size (MDES): d = 0.89
```

```note
표본 크기 (참가자 수)별 Minimum Detectable Effect Size (MDES):

| n | MDES (Cohen's d) |
|---|------------------|
| 10 | 1.00 |
| 12 | 0.89 |
| 15 | 0.78 |
| 20 | 0.66 |
| 34 | 0.50 |

HCI 논문에서는 새로운 아이디어를 빠르게 검증하는 proof-of-concept 테스팅을 위해 10~20명 정도의 참가자를 통해 구인하는 것이 일반적이다. 그런데 이는 통계적 취약점을 가져온다. 예를 들어 n = 12는 통계적으로 매우 큰 차이 (d = 0.89)만 감지할 수 있다. 중간 크기의 효과 (많은 PoC 시스템이 만들어낼 수 있는)는 이 n=12 표본 크기에서 감지되지 못할 수 있다.
```

# 4. 리뷰어 대응

HCI 논문 투고 과정에서 만날 수 있는 리뷰어 지적: *"참가자 수 (n = X)가 충분한 statistical power를 갖기에 너무 적어 보입니다. power analysis를 했나요?"*

**실험 전에 power analysis을 진행했다면,** 그냥 보고하면 된다. 가정된 effect size와 그 때 도출되었던 sample size (n)을 보고한다.

**진행하지 않았다면** (또는 필요한 n만큼 모집하지 못했다면), sensitivity analysis을 실행하고 상황을 파악, 전략을 수립한다.

### Case 1: 실제 효과 크기 ≥ 민감도 분석의 MDES (good)

예를 들어 n = 12 (Minimum Detectable Effect Size = 0.89)이고 데이터에서 d = 1.1이 나왔다. 이건 쉬운 상황이다. 이렇게 대응할 수 있다:

```note
A post-hoc sensitivity analysis (α = .05, power = .80) showed that n = 12 is sufficient to detect effects of d ≥ 0.89. The observed effect size in our study was d = 1.1, indicating our sample was adequate for the effect size present.
```

### Case 2: 실제 효과 크기 < 민감도 분석의 MDES (tough spot)

n = 12 (MDES = 0.89)인데 실제 d = 0.5라면, 진정으로 실험의 통계적 검정력이 부족했던 것이다. 방어하기가 쉽지 않다. 선택지가 몇 가지 있다:

- **(1) 깔끔하게 인정하기**: "We acknowledge the study may be underpowered for medium effects, and the observed effect size from the study data suggests a potentially meaningful effect that warrants investigation in a larger follow-up study."
- **(2) 파일럿 실험으로 reframe 하기**: 통계 결과가 논문의 main contribution이 아니라면, 해당 실험이 엄밀하고 결정적인 테스트가 아니라 preliminary evidence를 위한 가벼운 실험으로 reframe하겠다고 말한다.
- **(3) 데이터 추가 수집하기**: revision 타임라인이 허용한다면, 추가 참가자를 모집해 실험을 더 한다.
- **(4) 대응 피하기**: rebuttal에서 언급하지 않고 그냥 넘어간다. 리뷰어가 statistical power를 논문의 치명적인 결함으로 본다면 궁색한 변명으로 대응하더라도 어차피 논문은 리젝될거다. 기도한다.
# 참고

- Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum.
- [statsmodels TTestPower](https://www.statsmodels.org/stable/generated/statsmodels.stats.power.TTestPower.html)

# 변경 이력
- 2026년 6월 19일: 글 등록
