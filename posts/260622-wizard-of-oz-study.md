---
title: Wizard of Oz Study: The Spirit of HCI Research
date: 2026-06-22
tag: Reading
---

Wizard of Oz (WoZ) 스터디란 실제로는 완성되지 않은 시스템이 이미 존재하는 것처럼 사용자를 속인 상태에서 관찰하는 실험 방법을 말한다. 유저는 autonomous하게 동작하는 컴퓨터 시스템과 상호작용 한다고 생각하고 있지만, 실제로는 숨겨진 human operator (wizard)가 시스템을 뒤에서 직접 컨트롤하고 있는 상황인 것이다. 오즈의 마법사 내용처럼 사람들은 강력한 마법사가 있다고 믿었지만, 커튼 뒤에는 단지 레버를 조작하는 평범한 사람이 있었다는 그 비유에서 나왔다.

WoZ 스터디는 HCI 학계의 풍토를 보여주는 좋은 예시로, 지금 완성된 기술이 없더라도 미래의 상호작용을  연구할 수 있다는 태도를 보여준다. 이 글에서는 WoZ의 간단한 역사적 배경, 이 접근법이 가지는 unique benefit, 그리고 더 넓은 관점에서 HCI 연구자들이 중요시하는 Proof-of-Concept simulation의 개념을 살펴본다.

# Wizard of Oz 스터디의 역사

첫 사례는 1980년대 초 HCI 연구에서 당시 없던 기술을 있는 것처럼 보이게 하기 위해 인간 오퍼레이터를 숨긴 연구들이었다. [Gould et al.의 "Simulated Listening Typewriter"](http://doi.org/10.1145/2163.358100)와 [John F. Kelley의 1983년 CHI 논문](http://doi.org/10.1145/800045.801609)이 그 예다. 그들은 자연어 (일반적인 인간의 언어)로 소통할 수 있는 인터페이스가 있다면 사용자가 실제로 어떻게 상호작용하는지 알고 싶었다, 하지만 자연어 처리 시스템을 완전히 구현하는 데는 수십년이 걸릴 것이었다. 그래서 인간 오퍼레이터가 대신 (커튼 뒤에서) 사용자의 질문을 듣고 마치 컴퓨터가 자연스럽게 이해한 것처럼 응답하는 방식으로 시스템을 시뮬레이션 했다. 기술이 실현되기 수십년 전에 먼저 사용자의 경험 및 상호작용 (user experience & interaction)을 관찰할 수 있었던 것이다.

![|90%](img/posts/260622-wizard-of-oz-study/wizard-of-oz-example.jpg)

즉, 기술이 존재하기 전에  "타임 머신"을 타고 가서 사용자 경험을 먼저 엿볼 수 있다는 패러다임을 제시한 것이다. 두 연구 이후로 Wizard of Oz, 오즈의마법사 스터디는 HCI 분야의 표준적인 도구 중 하나가 되었다.

# 왜 만들기 전에 시뮬레이션하는가

HCI를 순수 공학과 구별하는 핵심 연구 질문 (research question)이 있다: "이것을 만들 수 있는가?"를 묻기 전에, "이것이 만들어지면 사람들이 어떻게 상호작용할 것인가?"를 먼저 묻는 것이다. 대부분의 공학에서의 일반적인 순서는 이렇다. 요구사항 분석 → 시스템 구축 → 성능 최적화 → 내부 평가 실행 → 실제 사용자에게 배포. 한 사이클이 끝나고 시스템이 완성되는 시점에는 이미 수개월이 지난 후다. 만약 상호작용 모델 및 초기 디자인에 근본적인 문제가 있었다면?

WoZ는 이 순서를 뒤집는다. 사용자가 그런 시스템을 실제로 맞이했을 때 어떻게 행동하고, 무엇을 기대하고, 어디에서 막히는지를 먼저 관찰하는 것이다. **"기술이 가능한가?"보다 먼저 "이 상호작용이 의미가 있는가?"를 묻는 이 태도**는 HCI라는 연구 분야의 시작부터 이어져온 학계의 정신이며, 바로 이것이 HCI 연구가 프로토타입, 시뮬레이션, approximation을 자주 사용하는 이유이다. 그리고 아마도 이 지점이 순수 엔지니어링 분야에 오래 종사했던 사람들에게 불편함을 일으킬 수 있는 지점이다. 목표는 오늘 완성된 제품을 출시하는 것이 아니라, 계속해서 미래를 이해하고 그려내는 것이다. 나는 이것이 비단 우리 분야 뿐만 아니라 "연구 (Research)"라는 것이 일반적으로 추구해야 할 지향점이 아닐까 생각한다.

# HCI의 더 넓은 정신: Proof-of-Concept Simulation

나는 WoZ 스터디를 더 general한 개념의 케이스로 본다. 바로 Proof-of-Concept (PoC) simulation 이다. 일반적으로 WoZ 연구는 인간 오퍼레이터가 autonomous 시스템을 시뮬레이션하는 방식을 지칭할 때만 사용되는데 (대화형 에이전트, 음성 인터페이스 등), 현대 HCI 연구는 시뮬레이션을 훨씬 더 광범위하게, 적극적으로 활용한다. 연구자들은 WoZ를 넘어 다양한 approximation 방법들을 통해 다음과 같은 질문들에 답하려 한다:

* **미래 시스템이 어느 정도 수준의 퍼포먼스와 태스크 부하 (task load)를 불러오는가?**
* **사용자가 정말 이 capability을 원하는가?**
* **시스템이 제대로 동작하지 않거나 에러를 일으킬 때 사용자는 어떻게 반응하는가?**
* **사용자는 디자이너가 의도한 대로 상호작용하는가, 아니면 예상치 못한 방식으로도 행동하는가?**

## 예시 1: [STAR Project](https://arxiv.org/pdf/2511.21143) (Kim et al. UIST 2023)

![|60%](img/posts/260622-wizard-of-oz-study/star-example.jpg)

본 연구에서 던지는 질문은 다음과 같다 - "스마트폰에서  양손 엄지손가락을 이용해 타이핑하는 익숙한 스킬을 맨손 AR 환경으로 이식할 수 있을까?" 우리는 STAR라는 이름의, AR 디스플레이 안경을 통해 사용자의 손 위에 가상 QWERTY 키보드를 띄우고, 터치스크린 대신 손 표면 피부를 타이핑 표면으로 삼아 엄지손가락으로 탭핑하는 아이디어를 냈다. 한편 현재 시점 (당시 2022년)의 AR 글라스 기술로 이를 완벽히 실현하는 것은 어려운 문제였다.

우리는 당시의 현실적인 기술을 최대한 반영하기 위해 홀로렌즈 2 디바이스에서 기본적으로 제공하는 hand tracking 및 디스플레이를 활용했지만, 엄지손가락과 피부의 미세한 접촉을 안정적으로 디텍션하는 것은 불가능한 일이었다. **따라서 완벽한 터치 디텍션을 capacitive tape strip으로 시뮬레이션하였다 (당시 AR 글라스에서는 불가능한 기술이었지만 우리는 미래에 더욱 정교해진 비전 기반 hand tracking, 나아가 스마트 반지와 워치 같은 웨어러블과 결합하면 충분히 가능할 것이라 전망했다. 실제로 3년 뒤 2025년에는 Meta Neural Band가 등장해 매우 안정적인 thumb tap detection을 보여주고 있다).** 결과적으로 우리는 고성능 비전 및 센싱 기술이 시장에 등장할 때까지 기다리지 않고, PoC 프로토타입을 만들어 다음과 같은 질문을 던졌던 것이다. - (1) 사람들이 수십 년 동안 갈고 닦은 스마트폰 타이핑 방식을 AR freehand 환경으로 가져올 수 있을까? (2) 그렇다면 실제 스마트폰 타이핑의 몇 % 정도까지 퍼포먼스가 따라올 수 있을까? 결론적으로 이는 Wizard of Oz 스터디는 아니지만, 정확히 동일한 목적을 갖고 수행된 PoC 시뮬레이션을 한 것이다.

## 예시 2: [HiFiGaze Project](https://arxiv.org/pdf/2603.19588) (Kim et al. CHI 2026)

![|70%](img/posts/260622-wizard-of-oz-study/hifigaze-example.jpg)

본 연구에서는 스마트폰에서 사용될 수 있는 딥러닝  시선 트래킹 (eye tracking) 모델을 제시했다. 그런데 사용자가 스크린 하단 부분을 응시할 때 (전면 카메라 시점에서) 눈꺼풀과 속눈썹이 눈의 feature를 종종 가린다는 사실을 발견했다.

**이에 보충 실험으로 "만약 카메라가 상단에 있지 않고 하단에 있었다면 이 문제를 해결해 성능이 더 개선될까?" 라는 핀포인트 질문을 던졌다.** 하지만 그러한 스마트폰은 현재 존재하지 않으며 아이폰을 분해해서 스크린 하단 쪽에 동일한 성능의 카메라를 하나 더 추가하는 것은 현실적으로 어려운 일이었다. 우리는 복잡하게 가지 않고 폰을 180도 회전해 카메라가 스크린 하단에 오도록 했고, 스크린에 보여지는 디스플레이를 다시 180도 돌려 사용자가 화면을 볼때는 차이가 없도록 했다. 즉, 완전히 새로운 장치가  만들어지기를 기다리지 않고 바로 연구 질문을 탐색할 수 있었던 것이다 (결과는 논문에 상세히 분석되어 있다).  이 경우도 위 STAR 연구의 사례와 마찬가지로 Wizard of Oz 스터디는 아니지만, 동일한  목적 (미래에 충분히 가능할 것으로 전망하는 조건을 현재의 approximation로 시뮬레이션한 후 결과를 측정, 이해를 넓히는 것)을 갖고 수행된 것이다.

# 참고

* Kelley, J. F. An empirical methodology for writing user-friendly natural language computer applications. CHI 1983. https://doi.org/10.1145/800045.801609
* Gould, J. D., Conti, J., & Hovanyecz, T. Composing Letters with a Simulated Listening Typewriter. Communications of the ACM 1983. https://doi.org/10.1145/2163.358100
* Kim, T., Karlson, A., Gupta, A., Grossman, T., Wu, J., Abtahi, P., Collins, C., Glueck, M., & Surale, H. B. STAR: Smartphone-analogous Typing in Augmented Reality. UIST 2023. https://arxiv.org/pdf/2511.21143
* Kim, T., Mollyn, V., Arakawa, R., & Harrison, C. HiFiGaze: Improving Eye Tracking Accuracy Using Screen Content Knowledge. CHI 2026. https://arxiv.org/pdf/2603.19588
* Hyungtae Lim. Wizard of Oz Study. https://limhyungtae.github.io/2026/05/17/hci-note-wizard-of-oz-study/

# 변경 이력

- Jun 22, 2026: Post published
