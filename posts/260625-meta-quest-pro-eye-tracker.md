---
title: Eye Tracker: Meta Quest Pro (How To Use)
date: 2026-07-01
tag: Eye Tracking
---

[Meta Quest Pro](https://www.meta.com/quest/quest-pro/)는 Meta VR 헤드셋 라인 중에 유일하게 시선 트래킹 (eye tracking)을 지원하는 모델이다. 2022년 출시되어 (가격: $1500) 2025년에 단종되었으며, 현재는 중고 시장에서만 구할 수 있다. 정밀한 핸드 트래킹과 시선 트래킹을 동시에 필요로 하는 HCI 연구에 여전히 필요한 장비다.

![Meta Quest Pro headset|80%](img/posts/260625-meta-quest-pro-eye-tracker/quest-pro-setup.jpg)

# 1. PC via Link로 연결하기

먼저 Quest Pro 헤드셋을 Meta Horizon Link를 통해  PC와 연결해야 한다 (Windows PC만 지원).

## 1-1. PC Side Setup

**(1) Meta Horizon Link 다운로드 및 설치:**
[Meta Horizon Link](https://www.meta.com/help/quest/509273027107091/)을 Windows PC에 다운로드한다.

**(2) Meta Horizon Link에서 Eye Tracking 활성화:**
Meta Horizon Link를 열고, Settings → Developer → Eye Tracking over Meta Horizon Link를 활성화한다.

**(3-a) 유선 연결:**
USB-C 3 케이블 (최소 5 Gbps)을 사용해 Meta Quest Pro를 PC에 직접 연결한다.

**(3-b) 무선 연결 (Air Link):**
또는 Air Link를 사용해 무선으로 연결할 수 있다. PC와 Quest Pro가 같은 Wi-Fi 네트워크 (5GHz 권장)에 연결되어 있으면 Meta Horizon Link에서 설정해 연결할 수 있다.

## 1-2. Headset Side Setup

Meta Quest Pro 헤드셋에서 필요한 기능들을 활성화한다:

**(1) Eye Tracking 활성화:**
Settings → Tracking → Eye Tracking 켜기.

**(2) Quest Link 활성화:**
Settings → Link 켜기.

PC와 헤드셋 양쪽 모두 셋팅이 되면 Meta Quest Pro가 Link를 통해 PC로 eye tracking 데이터를 전송할 준비가 완료된 것이다.

# 2. Unity로 프로그래밍하기

다운로드해서 바로 실행해볼 수 있는 [간단한 Unity 데모](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/MetaQuestPro)를 만들어 두었다. 셋팅 환경은 다음과 같다:

- Windows PC
- Unity 2021.3.45f2
- Meta XR Core SDK (간단한 데모를 위해 full Movement SDK 없이 만듦)
- Meta Quest Pro device

![Unity demo: gaze-object collision and printing raw signals.|100%](img/posts/260625-meta-quest-pro-eye-tracker/qpro-demo.gif)

## Tips

우선 먼저 Meta 공식 가이드를 읽자: [Eye Tracking for Movement SDK for Unity](https://developers.meta.com/horizon/documentation/unity/move-eye-tracking/), [Getting Started with Meta XR](https://developers.meta.com/horizon/documentation/unity/move-unity-getting-started/), [Meta Quest Hello World Tutorial](https://developers.meta.com/horizon/documentation/unity/unity-tutorial-hello-vr/).

아래에는 내가 제작한 Unity Demo 프로젝트의 [MetaQuestProEyeDemoController.cs](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/MetaQuestPro/Assets/Scripts/MetaQuestProEyeDemoController.cs)를 간단히 설명한다.

**(1) 눈 오브젝트에 `OVREyeGaze` 부착하기:** OVRCameraRig/TrackingSpace 아래에 empty GameObject를 생성한다. 이것이 눈알이 된다. `OVREyeGaze` component script를 이 오브젝트에 추가한다.

![|80%](img/posts/260625-meta-quest-pro-eye-tracker/ovreyegaze-attach.jpg)

**(2) 코드에서 eye tracking 시그널에 접근하기:**

```csharp
// 좌안과 우안 OVREyeGaze 컴포넌트 가져오기
OVREyeGaze leftEyeGaze = leftEyeGazeTransform.GetComponent<OVREyeGaze>();
OVREyeGaze rightEyeGaze = rightEyeGazeTransform.GetComponent<OVREyeGaze>();

// 양쪽 눈의 gaze ray 합치기
var origin = (leftEyeGazeTransform.position + rightEyeGazeTransform.position) / 2f;
var direction = (leftEyeGazeTransform.forward + rightEyeGazeTransform.forward).normalized;
Ray gazeRay = new Ray(origin, direction);

// Raycast로 gaze-object 충돌 감지
if (Physics.Raycast(gazeRay, out var hit))
{
    GameObject gazedObject = hit.collider.gameObject;
}

// Eye tracking 유효성 확인
if (leftEyeGaze.enabled && leftEyeGaze.EyeTrackingEnabled && leftEyeGaze.Confidence >= leftEyeGaze.ConfidenceThreshold)
{
    // Eye tracking이 활성화되고 신뢰할 수 있음
}
```

# References

- [Eye Tracking for Movement SDK for Unity](https://developers.meta.com/horizon/documentation/unity/move-eye-tracking/)
- [Getting Started with Meta XR](https://developers.meta.com/horizon/documentation/unity/move-unity-getting-started/)
- [Meta Quest Hello World Tutorial](https://developers.meta.com/horizon/documentation/unity/unity-tutorial-hello-vr/)
- [Meta Quest Pro Official Page](https://www.meta.com/quest/quest-pro/)

# 변경 이력

- 2026년 7월 1일: 글 업데이트
