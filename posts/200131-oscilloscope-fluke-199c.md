---
title: Oscilloscope (Fluke 199C): How to Use
date: 2020-01-31
tag: Electronics
---

오실로스코프는 전압 신호의 변화를 시간 축 그래프로 보여주는 장치다. 멀티미터가 전압·전류·저항의 크기를 숫자로만 보여준다면, 오실로스코프는 신호의 파형(모양, 주기, 진폭)까지 시각적으로 확인할 수 있다는 점에서 다르다. 연구실에 있는 Fluke 199C 스코프미터의 간단한 사용법을 정리해보자.

![Fluke 199C 스코프미터|60%](img/posts/200131-oscilloscope-fluke-199c/overview.png)

Fluke 199C 스코프미터는 (오실로)스코프도 되고 (멀티)미터도 된다. 노란색 첫번째 Scope 버튼을 누르면 스코프모드, 그 아래 Meter 버튼을 누르면 멀티미터모드가 된다.

# Scope 모드

![|60%](img/posts/200131-oscilloscope-fluke-199c/scope-screen.png)

- 세로 눈금: 한 칸 = 20V / 가로 눈금: 한 칸 = 2ms (위 예시는 약 60V 교류 전원)
- Trig (화면 하단 중앙): 트리거링 정보. 트리거가 잡히지 않으면 흐리게 표시된다.
- Probe 10:1: 10:1 프로브를 사용 중임을 나타낸다. 프로브 내부에서 신호를 1/10로 줄이지만, 스코프가 자동으로 10배 보정하기 때문에 화면에 표시되는 전압은 실제 신호 전압이다.
- AUTO 모드: 세로 눈금, 가로 눈금, 트리거링을 모두 자동으로 설정한다. 청록색 Auto/Manual 버튼으로 전환.
- 추가
  - 보라색 Hold/Run 버튼을 누르면 화면을 캡처할 수 있다.
  - Scope의 모든 설정을 리셋하려면 우선 전원을 끄고, 오른쪽 아래 User 버튼을 누른 상태로 다시 전원을 키면 경보음이 두 번(삐- 삐-)울리면서 리셋된다.

## Scope 모드 키 레이블 메뉴

![|70%](img/posts/200131-oscilloscope-fluke-199c/scope-menu.png)

Scope 버튼을 한 번 더 누르면 레이블을 숨길 수 있다. 가장 오른쪽 Clear menu 버튼을 눌러도 된다.

- **F1버튼 (Readings on/off)**: Reading 표시를 on/off할 수 있다.
- **F2, F3버튼 (Readings 1, 2)**: Reading 1 / 2 각각 어떤 수치(V, Vpp, A, Hz, W 등)를 표시할 지 선택한다. 하나만 사용할 수도 있고 둘 다 사용할 수도 있다.
- **F4버튼 (Waveform Options...)**: 파형의 여러 조건들을 설정한다.
  - Average 섹션: 예를 들어 Average 64를 선택하면 64번에 걸쳐 얻은 값을 평균내서 noise를 줄이고, 파형을 smoothing한다.
  - 외에 Glitch Detection, Mathematics(Input A/B 파형 덧셈 등) 등의 옵션이 있다.

# Meter 모드

![|60%](img/posts/200131-oscilloscope-fluke-199c/meter-screen.png)

미터 모드 화면은 비교적 간단하다. 가장 중요한 측정 값, 그리고 아래에 막대그래프 정도가 있다. Manual은 수동으로 범위(0~50kΩ)가 설정되는 모드라는 것.

## Meter 모드 키 레이블 메뉴

![|70%](img/posts/200131-oscilloscope-fluke-199c/meter-menu.png)

마찬가지로 Meter 버튼을 한 번 더 누르면 레이블을 숨길 수 있다.

- **F1버튼 (Measure...)**: 어떤 수치를 측정할 건지 선택한다 (kΩ, V, A 등).
- **F2버튼 (Relative on/off)**: 이 버튼을 누른 순간의 측정값에 대한 상대값 (+, -)을 보여준다.
- **F3, F4버튼 (Auto, Manual)**: 디폴트는 Auto다. 자동으로 측정값의 범위를 잡아준다. (측정값 아래 막대 그래프에 범위가 있다). Manual로 선택해서 수동 범위를 지정할수도 있다. F3, F4버튼 혹은 청록색 Auto/Manual 버튼으로 스위치된다.
- 마찬가지로 보라색 Hold/Run 버튼으로 화면을 캡처할 수 있다.

# 이 외에는

Scope, Meter 외에 Recorder 모드도 있다. Cursor, Zoom, Replay와 같은 기능들도 있는데 사용할 일이 생기면 후에 알아보고 내용을 추가하자.

# 변경 이력
- 2020년 1월 31일: 글 등록
- 2021년 12월 1일: Velog로 이전
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
