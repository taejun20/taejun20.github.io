---
title: Transistor (1): Basics
date: 2019-11-12
tag: Electronics
---

[Heterogeneous Stroke](https://github.com/taejun20/HeterogeneousStroke) 프로젝트를 진행하며 ERM 진동 모터 4개에 안정적인 전압을 제공해주면서 독립적으로 컨트롤하기 위해 [2N2369 트랜지스터](https://www.elektronik-kompendium.de/public/schaerer/FILES/2n2369.pdf)를 회로에 추가했다. 트랜지스터의 역할, 원리 등에 대해 정리해보자.

![2N2369 트랜지스터 (NPN)|40%](img/posts/191112-transistor-basics/transistor-2n2369.png)

트랜지스터에는 크게 두 종류: BJT(Bipolar Junction Transistor)와 FET(Field Effect Transistor)가 있다. 기본적으로 증폭과 스위칭을 수행하는 메커니즘은 같다. BJT 트랜지스터는 전류 입력을 통해 수도꼭지 (Base)가 조절되고, FET 트랜지스터는 전류가 없이 전압 입력만으로도 수도꼭지 (Gate)가 조절된다는 점이 다르다. 이후 설명은 모두 BJT 트랜지스터를 기준으로 서술한다.

# 트랜지스터의 역할

트랜지스터의 역할은 크게 1) 증폭과 2) 스위칭이다. 증폭/스위칭이 어떤 원리로 이뤄지는 것일까? (여기서 증폭이란 에너지를 새로 만들어내는 것이 아니다. 외부 전원(VCC)에서 오는 에너지를 바탕으로, 베이스에 입력되는 작은 전류 변화를 컬렉터에서 그보다 훨씬 큰 전류 변화로 재현하는 것이다. VCC가 상한선이며, 트랜지스터는 그 범위 안에서 신호의 크기를 키워주는 밸브 역할을 한다.)

NPN 트랜지스터의 경우로 설명하면, Collector는 물이 들어가는 입구, Emitter는 물이 나오는 출구, Base는 밸브 수도꼭지로 비유할 수 있다. 수도꼭지가 더 많이 열리면 Base→Emitter로 흐르는 전류가 커지는 것이다.

![PNP/NPN 트랜지스터 회로 기호와 수도꼭지 비유](img/posts/191112-transistor-basics/pnp-npn-valve.png)

Base→Emitter로 흐르는 전류 크기에 따라 아래와 같은 (Collector-Emitter Voltage: V_CE, Collector Current: I_C) 관계의 분포가 형성된다. 그리고 3개의 구분되는 Region이 생긴다.

![Practical Electronics For Inventors (2nd Edition), Figure 4.47, 442p](img/posts/191112-transistor-basics/iv-curve.png)

1. **Cut-off Region**: Base Current (I_B)가 0일 때 = 밸브가 잠겨 있을 때. 이 때 트랜지스터는 Collector와 Emitter 사이의 열린 스위치와 비슷한 역할을 한다. 그래프의 I_B = 0 mA 에서 Collector-Emitter Voltage (V_CE)가 아무리 커도 Collector에는 전류 (I_C)가 사실상 흐르지 않는다. 실제로는 무시할 수 있을 정도의 아주 작은 Leakage Current가 흐르긴 한다고 한다.

2. **Active Region**: 밸브가 열리는 만큼 Collector-Emitter 사이로 흐르는 물의 양이 조절되는 상태. Active Region은 트랜지스터가 증폭기로서 작동하는 영역이 된다. 같은 5V Collector-Emitter 전위차 (V_CE)에서 Base Current (I_B)를 0 mA → 0.4 mA로 점점 올리면 Collector에 흐르는 전류 (I_C)의 양이 계속 증가한다. 이 관계를 수식으로 표현하면 I_C = β × I_B 이다. β가 바로 전류증폭률 = Current Gain = h_FE로, 베이스 전류가 컬렉터 전류로 몇 배 재현되는지를 나타낸다. 예를 들어 β = 100인 트랜지스터에 I_B = 1mA를 흘리면 I_C = 100mA가 흐른다. 단, 이 100mA는 트랜지스터가 만들어내는 것이 아니라 VCC에 연결된 외부 전원에서 오는 것이다. 트랜지스터는 그 흐름을 I_B의 크기에 비례해서 열어주는 역할을 할 뿐이다. β는 트랜지스터마다 고유한 값을 가지며 대략 10–500 사이이고, 보통 고정된 값으로 취급하지만 실제로는 온도 등에 따라 약간 달라질 수 있다.

3. **Saturation Region**: 주어진 Collector-Emitter Voltage (V_CE)에서 Collector에 흐를 수 있는 최대 크기의 전류 (I_C max)가 흐르고 있는 상황. 이 때는 Base Current (I_B)를 더 키운다고 해도 Collector에 흐르는 전류의 양이 더 커지지 않는다.

Active Region 범위의 Base Current (I_B), Collector-Emitter Voltage (V_CE) 내에서 트랜지스터를 사용하면 증폭기로서 트랜지스터를 사용할 수 있고, Cut-off Region(꺼짐)과 Saturation Region(최대로 켜짐) 두 상태를 빠르게 전환하면 스위치로서 트랜지스터를 사용할 수 있다. 이 글의 도입부에서 언급한 ERM 모터 제어가 바로 이 스위칭 방식이다 — Arduino의 디지털 출력으로 Base를 켜고 끄면서 모터를 독립적으로 제어한다.

# 트랜지스터의 물리적 구성 원리

부도체인 실리콘(Si)에 붕소(B)나 인(P)을 첨가하면 반도체가 된다. 붕소(B)를 첨가하면 전자가 부족해져 정공으로 이뤄진 P형 반도체가 되고, 인(P)을 첨가하면 잉여 전자가 발생하며 N형 반도체가 된다. P형 반도체, N형 반도체를 붙여놓으면 P형에서 N형으로 전류가 흐르게 된다. 반대로 N형에서 P형으로는 전류가 거의 흐르지 않는다. 이를 **정류작용(rectification)**이라 한다. 이런 특성을 이용해 P-N접합 다이오드가 만들어지기도 한다. 아무튼 P, N, P형 반도체를 순서대로 붙이면 PNP 트랜지스터, 반대로 N, P, N을 붙이면 NPN 트랜지스터가 된다.

![NPN 트랜지스터의 이해를 돕기 위한 회로 예시|70%](img/posts/191112-transistor-basics/npn-circuit.png)

위 예시 그림에서 오른쪽의 역방향 전압은 n형→p형 방향이기 때문에 전류가 흐르지 않는다. 왼쪽의 순방향 전압(n형에 (-)가 걸리고 p형에 (+)가 걸림)의 경우 p형의 정공이 (+)에 의해 서로 반발해서 n형으로 이동하게 되고, n형의 전자들은 (-)에 의해 서로 반발해 p형으로 이동하게 되어 전류가 흐르게 된다. 결결국 이미터(N형)에서 출발한 전자들 중 일부만 베이스(P형) 정공과 결합하는데, 이것이 베이스 전류(I_B)가 된다. 나머지 대부분의 전자들은 베이스 층이 매우 얇아서 그냥 통과해 컬렉터로 넘어가는데, 이것이 컬렉터 전류(I_C)가 된다. 베이스로 유입되는 전자 수를 조금 늘리면(I_B 증가) 컬렉터로 넘어가는 전자 수도 그에 비례해 크게 늘어난다. 이 비율이 바로 Current Gain(β = I_C / I_B)이며, 베이스의 작은 전류 변화가 컬렉터의 큰 전류 변화로 재현되는 원리다.

이어지는 글: [Transistor (2): Transistor with Arduino](/posts?post=220309-transistor-arduino)

# 참고

- Paul Scherz. 2006. Practical Electronics for Inventors (2nd. ed.). McGraw-Hill, Inc., USA.
- [트랜지스터 정리 – Naver Blog](https://m.blog.naver.com/okseods1/220949581522)
- [트랜지스터 – Tistory](https://gigawatt.tistory.com/124)

# 변경 이력
- 2019년 11월 12일: 글 등록
- 2021년 12월 1일: Velog로 이전
- 2022년 2월 28일: 글 보충
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
