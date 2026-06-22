---
title: Wizard of Oz Study: The Spirit of HCI Research
date: 2026-06-22
tag: Reading
---

Wizard of Oz (WoZ) 스터디란 아직 실제로는 완성되지 않은 시스템을 사용자에게 이미 존재하는 것처럼 속여 경험하게 만드는 실험 및 연구 방법을 말한다. 유저는 autonomous하게 동작하는 컴퓨터 시스템과 상호작용하고 있지만, 실제로는 숨겨진 human operator (wizard)가 시스템을 뒤에서 직접 컨트롤하고 있는 상황인 것이다. WoZ는 HCI 학계가 이어받은 정신을 보여주는 좋은 예시로, 지금 완성된 기술이 없더라도 미래의 상호작용을 지금 연구할 수 있다는 태도를 보여준다.

이 글에서는 WoZ의 간단한 역사적 배경, 이 접근법이 가지는 unique benefit, 그리고 더 넓은 관점에서 HCI 연구자들이 중요시하는 Proof-of-Concept simulation을 살펴본다.

# Wizard of Oz 스터디의 역사

용어의 유래는 명확한데, 오즈의 마법사처럼 강력한 마법의 존재라고 생각하지만, 커튼 뒤에는 단지 레버를 조작하는 사람이 있었다는 그 비유에서 나왔다.

첫 사례는 1980년대 초 HCI에서 인간 오퍼레이터를 숨긴 연구들이었다. [Gould et al.의 "Simulated Listening Typewriter"](http://doi.org/10.1145/2163.358100)와 ["OZ 패러다임"을 소개한 John F. Kelley의 1983년 CHI 논문](http://doi.org/10.1145/800045.801609)이 그 예다. 그들은 자연어 인터페이스와 사용자가 어떻게 상호작용하는지 알고 싶었지만 자연어 처리 시스템을 완전히 구현하는 데는 수십년이 걸릴 것이었다. 대신 인간 오퍼레이터가 (커튼 뒤에서) 사용자의 질문을 듣고 마치 컴퓨터가 자연스럽게 이해한 것처럼 응답했다. 이런 방식으로 기술이 실현되기 수십년 전에 먼저 사용자 행동을 관찰할 수 있었던 것이다.

![|90%](img/posts/260622-wizard-of-oz-study/wizard-of-oz-example.jpg)

핵심 인사이트는 구현 기술이 아니라 상호작용 패턴을 먼저 이해해야 한다는 것. 기술이 존재하기 전에 사용자 경험을 "시간 여행"하며 먼저 경험해볼 수 있다는 패러다임을 제시한 것. 두 논문 이후로 WoZ 스터디는 HCI의 표준적인 도구 중 하나가 되었다.

# 왜 만들기 전에 시뮬레이션하는가

HCI를 순수 공학과 구별하는 핵심 연구 질문이 있다: "이것을 만들 수 있는가?"를 묻기 전에, "사람들이 이것과 어떻게 상호작용할 것인가?"를 먼저 묻는다. 대부분의 공학에서의 전형적인 경로는 이렇다: 시스템 구축 → 성능 최적화 → 평가 실행 → 사용자가 이를 원하는지 확인한다. 사이클이 끝나고 시스템이 완성되는 시점에는 이미 수개월이 지난 후다. 만약 상호작용 모델 및 디자인에 근본적으로 결함이 있다면? 너무 늦는다.

WoZ는 이 순서를 뒤집는다. 미래 시스템을 신중하게 시뮬레이션함으로써 완전체 시스템 구현에 돌입하기 전에 먼저 사용자 행동을 관찰한다. 사용자가 그런 시스템이 실제로 존재할 때 어떻게 행동하고, 무엇을 기대하고, 어디에서 막히는지를 먼저 관찰하는 것이다. 즉, WoZ 연구는 "기술이 가능한가?"보다 먼저 "이 상호작용이 의미가 있는가?"를 묻는다. 이것은 HCI 연구의 시작부터 이어져온 학계의 정신이며, 방법론적으로 프로토타입, 시뮬레이션, approximation을 자주 이용하는 이유이다. 그리고 아마도 이것이 순수 엔지니어링 분야에 오래 종사했던 사람들이 불편함을 느낄 수 있는 지점이다. 목표는 오늘 완성된 제품을 출시하는 것이 아니다. 더 미래를 이해하고 그려내는 것이다. 이것이 내가 생각하기에 "연구"가 나아가야 할 true direction이다.

# HCI의 더 넓은 정신: Proof-of-Concept Simulation

나는 WoZ 스터디를 더 큰 개념의 한 가지 케이스로 본다. 바로 Proof-of-Concept (PoC) simulation 이다. 일반적으로 WoZ 연구는 인간 오퍼레이터가 autonomous 시스템을 시뮬레이션하는 방법을 의미하는데 (예. 대화형 에이전트, 음성 인터페이스), 한편 현대 HCI 연구는 시뮬레이션을 훨씬 더 광범위하게 사용한다. WoZ를 넘어서, 연구자들은 이용 가능한 다양한 approximation 방법들을 사용하여 미래 시스템을 시뮬레이션한다. 이를 통해 다음과 같은 중요 질문들에 답할 수 있다:

* **시스템이 처리해야 하는 성능 수준과 실제 작업 부하는 무엇인가?**
* **사용자가 정말 이 기능을 원하는가?**
* **시스템이 실패했을 때 사용자는 어떻게 반응하는가?**
* **사용자가 의도한 대로 상호작용하는가, 아니면 예상치 못한 방식으로 사용하는가?**

시뮬레이션 환경에서 실제 사용자 행동을 관찰함으로써, 연구자들은 완성된 시스템이 기술적으로 실현되기 어려울 때에도 이러한 질문들에 답할 수 있다. 이것이 바로 HCI 연구의 pionieer들로부터 내려온 학계의 정신이라고 나는 느끼고 있다. 우리 팀에서 수행한 연구들로 몇 가지 예시로 덧붙이겠다:

## 예시 1: [STAR Project](https://arxiv.org/pdf/2511.21143) (Kim et al. UIST 2023)

![|60%](img/posts/260622-wizard-of-oz-study/star-example.jpg)

본 연구는 한 가지 중요한 질문을 던진다. 스마트폰에서 익숙한 양손 엄지손가락 타이핑을 맨손 AR 환경으로 이식할 수 있을까? 우리는 AR 안경을 통해 사용자의 손 위에 가상 QWERTY 키보드를 띄우고, 피부에 닿는 엄지손가락의 터치에 반응하는 타이핑 시스템을 만드는 것이었다. 하지만 이를 현재 시점에서 완벽히 실현하는 것은 현 시점 일반적인 AR 셋업으로는 어려웠다 (정확한 핸드 트래킹, 고성능 AR 디스플레이, 그리고 안정적인 엄지 손가락의 피부 터치 detection).

그래서 우리는 손가락-피부 tap detection을 capacitive tape strip으로 시뮬레이션했다 (현재 AR 안경에는 없는 기술이나 2022년 당시 미래의 반지와 워치 같은 웨어러블과 결합해 가능할 것으로 보았다. 실제로 2025년에는 Meta Neural Band가 등장해 매우 안정적인 tap detection을 보여주었다). 결과적으로 우리는 고성능 센서가 시장에 등장할 때까지 기다리기 전에 PoC 프로토타입을 만들어 다음과 같은 질문을 던질 수 있었다 - **(1) 사람들이 스마트폰에서 배운 타이핑 방식을 AR에서도 그대로 적용할 수 있을까? (2) 그렇다면 실제 스마트폰과 비교했을 때 입력 속도는 어느 정도일까?** 엄밀히 말해 이는 WoZ는 아니지만, 같은 목적을 갖고 일어난 시뮬레이션이다. 미래 환경을 지금 만들어내고, 사용자의 행동과 경험을 관찰하는 것.

## 예시 2: [HiFiGaze Project](https://arxiv.org/pdf/2603.19588) (Kim et al. CHI 2026)

![|70%](img/posts/260622-wizard-of-oz-study/hifigaze-example.jpg)

본 연구는 스마트폰에 탑재된 전면 카메라를 사용하는 새로운 딥러닝 기반 시선 추정 모델을 제시했다. 그런데 성능 평가에서 사용자가 특히 화면 하단 근처의 대상을 응시할 때 윗눈꺼풀과 속눈썹이 우리가 제안한 model이 원하는 눈의 feature를 가릴 수 있다는 것을 발견했다.

만약 카메라가 하단에 있다면 이 문제를 피하고 성능을 한층 더 개선시킬 수 있을까? 라는 질문을 던졌다. 하지만 그러한 스마트폰은 존재하지 않으며, 실험 기기였던 iPhone을 해체해서 스크린 하단 쪽에 같은 성능의 카메라를 하나 더 추가하는 것은 현실적으로 어려운 일이다. 대신 폰을 180도 뒤집어 카메라를 하단에 위치하도록 했고, 디스플레이를 반전시켜 사용자가 화면을 볼때는 똑같지만 카메라가 아래로 오도록 했다. 즉, 새로운 장치를 프로토타이핑할 필요 없이 중요한 연구 질문을 탐색할 수 있었던 것이다 (결과는 논문에 첨부되어 있다). 여전히 이 경우도, WoZ는 아니지만, 같은 목적 (미래에 충분히 가능할 하드웨어 조건을 현재의 approximation로 시뮬레이션한 후 결과를 측정, 이해를 넓히는 것)을 이뤄낼 수 있었던 것이다.

# References

* Kelley, J. F. An empirical methodology for writing user-friendly natural language computer applications. CHI 1983. https://doi.org/10.1145/800045.801609
* Gould, J. D., Conti, J., & Hovanyecz, T. Composing Letters with a Simulated Listening Typewriter. Communications of the ACM 1983. https://doi.org/10.1145/2163.358100
* Kim, T., Karlson, A., Gupta, A., Grossman, T., Wu, J., Abtahi, P., Collins, C., Glueck, M., & Surale, H. B. STAR: Smartphone-analogous Typing in Augmented Reality. UIST 2023. https://arxiv.org/pdf/2511.21143
* Kim, T., Mollyn, V., Arakawa, R., & Harrison, C. HiFiGaze: Improving Eye Tracking Accuracy Using Screen Content Knowledge. CHI 2026. https://arxiv.org/pdf/2603.19588
* Hyungtae Lim. Wizard of Oz Study. https://limhyungtae.github.io/2026/05/17/hci-note-wizard-of-oz-study/

# Changelog

- Jun 22, 2026: Post published
