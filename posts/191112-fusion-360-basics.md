---
title: Fusion 360 기초 사용법
date: 2019-11-12
tag: 3D Modeling
---

간단한 수준의 [Fusion 360](https://www.autodesk.co.kr/products/fusion-360/overview) 사용법을 까먹지 않게 기록해보려 한다. 상단 Navigation Bar에서 자주 쓰는 기능들을 골라서 설명한다. 고급 기능보다는 스케치 → 솔리드 모델링 → STL 출력까지의 기본 흐름을 익히는 데 초점을 맞췄다.

![2019.11.14 기준 Fusion 360 overview](img/posts/191112-fusion-360-basics/overview.png)

# SOLID 탭

![](img/posts/191112-fusion-360-basics/solid-tab.png)


Default로 설정되어 있는 탭. 기본 워크플로우는 다음과 같다. 1) Create Sketch 클릭 → SKETCH 탭 진입. 2) 2차원 도형을 그린 후 Finish Sketch로 복귀. 3) Extrude 등을 이용해 3차원 구조 생성. 대부분의 모델링 작업은 이 사이클을 반복하는 것이다.

## CREATE

- **Extrude** — Beginner들은 주로 이것만 쓴다고 보면 된다. 스케치한 면을 선택하고 Extrude를 눌러서 Depth를 주면 2차원 면이 튀어나와 입체도형이 된다. Operation 옵션에서 Join(기존 바디에 합치기), Cut(기존 바디에서 파내기), New Body(독립된 새 바디 생성)를 선택할 수 있어서, 구멍을 뚫거나 부품을 합치는 작업도 전부 Extrude 하나로 처리된다.
- **Revolve** — 최근에 처음 써봤다. 면을 선택하고, 회전 축이 될 기준 선을 클릭하고, 각도를 주면 면이 축을 기준으로 회전하면서 입체도형이 된다.
- **Box, Cylinder, Sphere 등** — 2차원 도형들을 스케치하지 않고 여기서 바로 3차원 입체 도형을 만들수도 있다.

## MODIFY

- **Fillet** — Modify 메뉴도 거의 Fillet을 주로 쓰는 것 같다. 모서리 선분을 누르고 Fillet을 누르면 그 모서리에 곡률을 줄 수 있다. 아래는 Fillet의 예시.

![|30%](img/posts/191112-fusion-360-basics/fillet.png)

- **Scale** — 입체도형을 전체 비율을 유지하면서 사이즈만 줄여준다. 말 그대로 Scale.

## CONSTRUCT

기준이 되는 2차원 Sketch 평면을 원하는 위치에 생성하는 역할을 한다. 이미 있는 만들어 놓은 입체도형의 면, 혹은 그 면에서 일정 거리 떨어진 위치에 새로운 sketch plane을 만들어 준다. 만드는 모델이 복잡해질 수록 더욱 필요한 기능으로 보인다.

## INSPECT

- INSPECT를 누르고 특정 지점, 그 다음 특정 지점을 찍으면 그 사이의 거리를 알려준다.
  - 점과 점사이, 점과 선사이, 점과 면사이(최단 거리), 면과 면(수직 거리) 등의 정보를 알 수 있다.
- 사용 빈도가 꽤나 높다.

# SKETCH 탭

![](img/posts/191112-fusion-360-basics/sketch-tab.png)

## CREATE

- **Line(L), Circle(C), Rectangle(R)** — 제일 많이 쓰는 3가지. 괄호 안은 단축키. 생성하려 하는 도형에 필요한 reference point들을 클릭하면 도형을 만들어준다.
- **Arc, Polygon, Spline 등** — 아주 가끔 쓴다. Spline은 아직 안써봤다.

## CONSTRUCTION

Construction 토글을 켜면 도형이 실선이 아닌 점선(보조선)으로 그려진다. 실제 모델에는 영향을 주지 않고 참조 기준선 역할만 한다. 예를 들어 원 중심에서 40mm 떨어진 위치에 다른 원을 배치할 때 이 보조선으로 간격을 잡으면 편하다.

![|40%](img/posts/191112-fusion-360-basics/constraints.png)

## FINISH SKETCH

SKETCH를 끝내준다. 간단한 기능인데, 적절히 사용하여 Timeline을 깔끔하게 정리하는 것이 중요하다.

# Timeline과 Component 트리

## Component 트리

만들어진 좌표축 기준점(Origin), 모델 바디(Bodies), 스케치(Sketches)가 저장된다. 각 element 왼쪽에 눈 모양을 클릭하면 보이게/안보이게 할 수 있다. 이 component들을 기준으로 Timeline이 자동 생성된다.

![|40%](img/posts/191112-fusion-360-basics/component-tree.png)

## Timeline

화면 가장 하단에 Timeline이 있다. 프로젝트 규모가 커질수록 협업할 일이 많아지기 때문에, 누군가 실수를 하면 Github commit처럼 roll-back이 가능하도록 버전 관리를 깔끔하게 해야한다. Timeline을 잘 짜는게 Fusion 360에서 매우 중요한 부분인 것 같다. 

![](img/posts/191112-fusion-360-basics/timeline.png)

예) Body, Sketch등 만들어진 component는 시간 순서대로 Timeline에 있다. 스케치를 하고 도형을 만들다가 다시 예전에 스케치를 했던 평면에서 도형을 그리려고 하면 새로 스케치 평면을 만들지 말고 Component 트리에 있는 예전 Sketch를 찾아서 더블 클릭 후에 거기다가 만들어야 Timeline이 안 꼬인다. 스케치 이름을 더블클릭해서 직접 바꿔두면(Sketch1 → base_profile 등) 나중에 타임라인에서 찾기가 더 편하다.

# TOOLS 탭

![](img/posts/191112-fusion-360-basics/tools-tab.png)

`.stl` 파일로 export하는 단계다. 순서는 다음과 같다. 1). Component 트리 또는 뷰포트에서 출력할 Body 선택. 2) 상단 메뉴 TOOLS → MAKE → 3D Print 클릭. 3) 우측 패널에서 Send to 3D Print Utility 체크 해제 (외부 프로그램으로 바로 넘기지 않고 파일로 저장할 경우). 4) OK → 저장 경로 지정 후 완료

# 변경 이력
- 2019년 11월 12일: 글 작성
- 2021년 12월 1일: Velog로 이전
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
