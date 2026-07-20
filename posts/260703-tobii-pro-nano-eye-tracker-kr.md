---
title: Eye Tracker: Tobii Pro Nano/Spark/Fusion (How To Use)
date: 2026-07-03
tag: Eye Tracking
---

[Tobii Pro](https://www.tobii.com/products/eye-trackers/screen-based) 시리즈는 연구용 목적으로 사용될 수 있는 고성능의 시선 트래커 (eye tracker)이다.

```note
Tobii Pro 디바이스 (Nano, Spark, Fusion, Spectrum)는 **기기 자체에 license가 내재**되어 있다. 공장에서 제작될 때 바로 하드웨어 자체에 포함시켜서 출고하기 때문에 제품을 받은 뒤 추가 등록이나 라이선스 활성화 없이 PC에 연결하고 바로 쓰면 된다.
```

![Tobii Pro Nano (now discontinued, replaced by Tobii Pro Spark)|100%](img/posts/260703-tobii-pro-nano-eye-tracker/tobii-nano-etm.jpg)

# 1. Install, Mount, and Configure

먼저 Tobii 공식 문서를 읽자: [Tobii Pro Eye Tracker Manager 프로그램 설치](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US) & [기기 마운트](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US) & [프로그램 내 기기 설정.](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US)

**(1) Tobii Pro Eye Tracker Manager 설치:** 기기를 PC에 USB로 연결하고 (나는 보통 Windows PC를 사용한다), [Tobii Pro Eye Tracker Manager](https://connect.tobii.com/s/etm-downloads?language=en_US)를 다운로드해 설치한다.

![|80%](img/posts/260703-tobii-pro-nano-eye-tracker/tobii-etm-calibration.jpg)

**(2) Tracker 모니터에 마운트:** [오피셜 마운팅 가이드](https://connect.tobii.com/s/article/Mount-Tobii-Pro-Fusion-on-the-screen-Step-2?language=en_US)에 따라 기기를 모니터 하단에 부착한다.

**(3) Tracker 설정:** 마운트 및 기기 연결 후 Tobii Pro Eye Tracker Manager 프로그램에서 [기기 설정](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US)을 진행한다.

# 2. Python으로 프로그래밍하기

다운로드해서 바로 실행해볼 수 있는 [간단한 Python 데모](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/TobiiProNano)를 만들어 두었다. 셋팅 환경은 다음과 같다:

- Windows
- Python 3.10 (conda env)
- Tobii Pro SDK (conda env: pip install tobii_research)
- Tobii Pro Nano 기기

![|100%](img/posts/260703-tobii-pro-nano-eye-tracker/tobii-nano-demo.gif)

## Tips

먼저 Tobii 공식 문서를 읽자: [Tobii Pro SDK](https://developer.tobiipro.com/index.html), [Python Getting Started](https://developer.tobiipro.com/python/python-getting-started.html), [Official Python Code Samples](https://developer.tobiipro.com/c/c-sdk-reference-guide.html)

아래에는 내가 제작한 파이썬 데모의 [app.py](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/TobiiProNano/app.py)를 간단히 설명한다.

**(1) Connect to tracker:** Tobii tracker를 찾아서 변수로 할당한 뒤 실시간 gaze 업데이트를 구독한다.

```python
def discover_trackers():
    trackers = list(tobii_research.find_all_eyetrackers())
    return trackers[0]

# ExperimentWindow.__init__에서:
self.tracker = discover_trackers()
self.tracker.subscribe_to(tobii_research.EYETRACKER_GAZE_DATA, self.gaze_callback, as_dictionary=True)
self.subscribed = True
```

**(2) Process gaze data:** left eye과 right eye에서 gaze point를 추출하고 트래킹의 순간 validity를 체크한다.

```python
def center_gaze(gaze_data) -> GazeState:
    left, left_valid = read_eye_point(gaze_data, "left")
    right, right_valid = read_eye_point(gaze_data, "right")
    
    if left_valid and right_valid:
        center = ((left[0] + right[0]) * 0.5, (left[1] + right[1]) * 0.5)
    elif left_valid:
        center = left
    elif right_valid:
        center = right
    else:
        center = None
    
    return GazeState(point_norm=center, left_norm=left, right_norm=right, ...)
```

**(3) Detect gaze hit:** 시선이 원 안에 들어왔는지 detect한다.

```python
def hit_target(self, gaze_pixel: tuple[int, int] | None):
    if gaze_pixel is None:
        return "", False
    
    gx, gy = gaze_pixel
    for name, center, radius in self.target_specs():
        if math.dist((gx, gy), (center.x(), center.y())) <= radius:
            return name, True
    return "", False
```

# 참고

- [Tobii Pro](https://www.tobii.com/products/eye-trackers/screen-based)
- [Tobii Pro SDK](https://developer.tobiipro.com/index.html)

# 변경 이력

- Jul 3, 2026: 게시물 작성
