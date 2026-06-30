---
title: Eye Tracker: FOVE VR (How To Use)
date: 2026-06-30
tag: Eye Tracking
---

[FOVE](https://fove-inc.com/product/fove0/)는 시선 트래킹 (eye tracking) 기능이 탑재된 VR 헤드셋이다. 가장 처음으로 일반 소비자들이 구매할 수 있게 commercialize한 eye tracking VR 헤드셋으로 알려져 있으며, 무려 **2016년**부터 판매되었다. 오늘날 Meta와 HTC가 Quest Pro, Vive Pro Eye를, 또 Apple이 Vision Pro 같은 고성능 제품들로 시장을 리드하고 있지만, 나는 여전히 FOVE 헤드셋이 가진 유니크한 장점이 있다고 생각한다. 시스템이 전반적으로 훨씬 lightweight하다는 점이다.

하드웨어 구조가 매우 단순하고 [시스템 소스 코드](https://github.com/FoveHMD)가 공개되어 있다. 반면에 Apple Vision Pro나 Meta Quest Pro 등에는 핸드 트래킹, 3차원 주변 공간 스캐닝 등의 여러 복잡한 기술이 합쳐져 있어 매우 무겁다. FOVE는 그런 것들을 모두 들어내고 그래픽 렌더링과 시선 트래킹 두 가지에만 집중한다. 가볍게 돌아가면서 실시간 눈 영상, 시선 벡터, 눈 깜빡임 여부, 동공 간 거리 등을 간단히 접근할 수 있게 해준다. 이러한 데이터를 제공하는 다른 연구용 장비들 중에는 천만원을 넘기는 제품들도 많다. FOVE는 $1,500이다.

![FOVE 0 headset|80%](img/posts/260625-fove-vr-eye-tracker/fove1.jpg)


# 1. FOVE VR Platform (Desktop App) 설치

**(1) 설치파일 요청:** [공식 문의 폼](https://fove-inc.com/fove-vr-platform-contact/)을 작성하면 FOVE VR Platform (데스크탑 앱) `.msi` 설치 파일과 라이선스 키 `.txt` 파일을 이메일로 보내준다. 응답이 꽤 빠르다.

**(2) 설치:** `.msi` 파일로 설치한다. 설치가 완료되면 라이선스 활성화 창이 뜬다. `.txt` 파일의 라이선스 키를 복사해 붙여넣는다.

# 2. FOVE VR Platform 살펴보기

설치 후 Windows 시작 메뉴에서 "FOVE VR" 앱을 찾을 수 있다. 켜면 화면 오른쪽 하단에 뜨며, Debug Tool 등 여러 기능을 실행할 수 있다 (아래 참고).

### (1) Debug Tool

![FOVE VR 데스크탑 앱: 디버그 툴|100%](img/posts/260625-fove-vr-eye-tracker/fove2.jpg)



이것만으로도 여러 유용한 정보를 바로 확인할 수 있다. 실시간 눈 영상, 머리 회전 및 이동 상태, 시선 추적 신호, 그리고 **캘리브레이션** 시작 버튼이 있다. 중간 중간 헤드셋 및 시선 트래킹이 정상적으로 동작하는지 확인하고, 사용자 연구에서 참가자별 calibration을 진행할 때 이 기능을 자주 사용하게 된다.

### (2) Mirror Client View

![FOVE VR 데스크탑 앱: 미러 클라이언트|100%](img/posts/260625-fove-vr-eye-tracker/fove3.jpg)

미러 클라이언트 뷰는 (binocular) 헤드셋에 렌더링되고 있는 그래픽, 즉 사용자가 실시간으로 보고 있는 장면을 보여준다.

# 3. Unity로 프로그래밍하기

다운로드해서 바로 실행해볼 수 있는 [간단한 Unity 데모](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/FOVE)를 만들어 두었다. 셋팅 환경은 다음과 같다:

- Windows
- Unity 2021.3.45f2
- FOVE 0 device

![간단 Unity 데모: 시선 ray 시각화, 시선-오브젝트 충돌, raw signal 출력|100%](img/posts/260625-fove-vr-eye-tracker/fove5.gif)

## Tips

우선 먼저 FOVE 공식 가이드를 참고하자: [Unity Plugin Guide](https://github.com/FoveHMD/UnityPlugin/blob/master/PluginGuide.md), [Quick Start Guide](https://github.com/FoveHMD/UnityPlugin/blob/master/QuickStart.md).

아래에는 내가 제작한 Unity Demo 프로젝트의 [FoveGazeDemoController.cs](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/FOVE/Assets/Scripts/FoveGazeDemoController.cs)를 간단히 설명한다.

**(1) 가장 먼저 FOVE 모듈을 상단에 include한다:**

```csharp
using Fove;
using Fove.Unity;
```

**(2) 그리고 원하는 시선 트래킹 데이터의 종류를 register한다:**

```csharp
FoveManager.RegisterCapabilities(ClientCapabilities.EyeTracking |
    ClientCapabilities.GazedObjectDetection |
    ClientCapabilities.UserIPD |
    ClientCapabilities.EyeBlink);
```

**(3) 이후 메인 loop (e.g., `Update`, `LateUpdate`)에서 각 데이터에 접근한다:**

```csharp
Result<Ray> ray = foveInterface.GetCombinedGazeRay();
Result<GameObject> gazed = FoveManager.GetGazedObject();
Result<bool> leftBlink  = FoveManager.IsEyeBlinking(Eye.Left);
Result<bool> rightBlink = FoveManager.IsEyeBlinking(Eye.Right);
```

항상 `Result<T>`형태로 return한다. `.value` 로 값에 접근하기 전에 `.IsValid`를 먼저 확인하는 방식으로 코드를 짠다.

**(4) 액세스 가능한 전체 데이터 목록:**

```csharp
// 시선 레이 (월드 좌표 — FoveInterface 경유)
Result<Ray> combinedRay = foveInterface.GetCombinedGazeRay();
Result<Ray> leftRay     = foveInterface.GetGazeRay(Eye.Left);
Result<Ray> rightRay    = foveInterface.GetGazeRay(Eye.Right);
Result<float> gazeDepth = foveInterface.GetCombinedGazeDepth(); // 좌우 시선 레이가 수렴하는 거리

// 응시 오브젝트
Result<GameObject> gazed = FoveManager.GetGazedObject();

// 눈 깜빡임
Result<bool> leftBlink       = FoveManager.IsEyeBlinking(Eye.Left);
Result<bool> rightBlink      = FoveManager.IsEyeBlinking(Eye.Right);

// 눈 상태 & 주의 이동
Result<EyeState> leftState  = FoveManager.GetEyeState(Eye.Left);  // Opened / Closed / NotDetected — IsEyeBlinking보다 세분화
Result<EyeState> rightState = FoveManager.GetEyeState(Eye.Right);
Result<bool> shiftingAttn   = FoveManager.IsUserShiftingAttention(); // 단속 운동(saccade) 중 true; 안정적 응시 데이터만 원할 때 필터링

// 눈 기하학적 정보
Result<float> ipd              = FoveManager.GetUserIPD();
Result<float> iod              = FoveManager.GetUserIOD();
Result<float> pupilRadiusLeft  = FoveManager.GetPupilRadius(Eye.Left);
Result<float> pupilRadiusRight = FoveManager.GetPupilRadius(Eye.Right);
Result<float> irisRadiusLeft   = FoveManager.GetIrisRadius(Eye.Left);
Result<float> irisRadiusRight  = FoveManager.GetIrisRadius(Eye.Right);
Result<float> eyeballRadiusLeft  = FoveManager.GetEyeballRadius(Eye.Left);
Result<float> eyeballRadiusRight = FoveManager.GetEyeballRadius(Eye.Right);
Result<float> torsionLeft  = FoveManager.GetEyeTorsion(Eye.Left);
Result<float> torsionRight = FoveManager.GetEyeTorsion(Eye.Right);
Result<EyeShape>   eyeShapeLeft    = FoveManager.GetEyeShape(Eye.Left);
Result<EyeShape>   eyeShapeRight   = FoveManager.GetEyeShape(Eye.Right);
Result<PupilShape> pupilShapeLeft  = FoveManager.GetPupilShape(Eye.Left);
Result<PupilShape> pupilShapeRight = FoveManager.GetPupilShape(Eye.Right);

// 눈 카메라 이미지
Result<Texture2D> eyesImage = FoveManager.GetEyesImage();

// 헤드 포즈
Result<Quaternion> hmdRotation = FoveManager.GetHmdRotation();
Result<Vector3>    hmdPosition = FoveManager.GetHmdPosition(isUserStanding: true);

// 타임스탬프
Result<FrameTimestamp> eyeDataTimestamp = FoveManager.GetEyeTrackingDataTimestamp();
```

# 참고

- [FOVE 공식 사이트](https://fove-inc.com/)
- [Getting Started With FOVE – 공식 가이드](https://support.fove-inc.com/Getting-Started-With-FOVE-6e81882b908446d4b4f100ceb70eeab0)

# 변경 이력
- 2026년 6월 30일: 글 등록
