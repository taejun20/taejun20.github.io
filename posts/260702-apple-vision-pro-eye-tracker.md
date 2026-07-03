---
title: Eye Tracker: Apple Vision Pro (How To Use)
date: 2026-07-02
tag: Eye Tracking
---

[Apple Vision Pro](https://www.apple.com/apple-vision-pro/)는 Apple의 XR 헤드셋으로 시선 트래킹 (eye tracking) 기능을 탑재하고 있다. 2024년 출시되었으며, 꽤나 정확한 eye tracking을 제공하며 이를 상호작용 모델에 적극적으로 활용하고 있다.

```note
**Key Limitation:** 아쉽지만 Apple Vision Pro에서 eye tracking signal에 대한 접근은 상당히 제한되어 있다. 원본 gaze ray 데이터를 제약없이 제공하는 [Meta Quest Pro](/p/260625-meta-quest-pro-eye-tracker)와 [FOVE VR](/p/260625-fove-vr-eye-tracker)와 달리, Apple은 개발자가 사용자의 시선 정보에 접근하는 것을 엄격하게 차단해두었다. 앱은 raw gaze ray에 접근할 수 없으며, 사용자가 어느 오브젝트를 보고 있는지도 사용자가 핀치 제스처를 수행하기 전까지는 알 수 없다.
```

![|80%](img/posts/260702-apple-vision-pro-eye-tracker/vision-pro-demo.jpg)

# 1. Mac과 연결하기

먼저 Vision Pro 헤드셋을 Mac과 연결해야 한다.

## 1-1. Mac 측 설정

**(1) Xcode 설정:**
Mac에서 Xcode를 설정한다. XCode - Settings - Components에서 Vision OS Platform을 다운로드하고, 비어있는 visionOS 프로젝트를 생성한다. Vision Pro 기기를 빌드 타겟으로 선택했는지 확인하고, 최소 배포 OS 버전을 올바르게 설정한다.

![|100%](img/posts/260702-apple-vision-pro-eye-tracker/xcode-setup.png)

**(2) 기기 페어링:**
Xcode를 사용해 Vision Pro를 Mac에 무선으로 (또는 USB-C로) 연결한다.

## 1-2. Vision Pro 헤드셋 측 설정

**(1) 개발자 모드 활성화:**
Settings → About → Developer Mode에서 켜기.

**(2) 시선 트래킹 활성화:**
Settings → Accessibility → Eye Tracking에서 켜기.

# 2. Xcode로 프로그래밍하기

다운로드해서 바로 실행해볼 수 있는 [간단한 데모](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/AppleVisionPro)를 만들어 두었다. 셋팅 환경은 다음과 같다:

- Mac Air (M3)
- macOS 26.5.2
- Xcode 26.4.1
- visionOS Xcode SDK 26.4
- Apple Vision Pro 기기

![|100%](img/posts/260702-apple-vision-pro-eye-tracker/vision-pro-demo.gif)

## Tips

우선 먼저 Apple 공식 visionOS 문서를 읽자: [visionOS Get Started](https://developer.apple.com/visionos/get-started/), [Eyes & Interaction](https://developer.apple.com/design/human-interface-guidelines/eyes), [RealityKit Documentation](https://developer.apple.com/documentation/realitykit), [visionOS Documentation](https://developer.apple.com/documentation/visionos).

아래에는 내가 제작한 Xcode 프로젝트의 [ImmersiveView.swift](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/AppleVisionPro/AppleVisionPro/ImmersiveView.swift)를 간단히 설명한다.

**(1) RealityKit 씬 + 시선 반응 오브젝트 설정:**
[ImmersiveView.swift](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/AppleVisionPro/AppleVisionPro/ImmersiveView.swift)에서 `RealityView` (RealityKit에서 제공)와 루트로서의 `AnchorEntity`를 생성했다. 상호작용이 가능하게 하려는 각 오브젝트에 `InputTargetComponent`와 `HoverEffectComponent`를 추가한다. 이를 통해 Apple 시스템의 internal gaze detection과 시선이 도달했을 때의 hover 피드백이 활성화된다.

```swift
let sphere = ModelEntity(mesh: mesh, materials: [material])
sphere.components.set(InputTargetComponent())
sphere.components.set(HoverEffectComponent())
sphere.components.set(CollisionComponent(shapes: [.generateSphere(radius: 0.15)]))
```

**(2) Pinch 및 Pinch시 응시됐던 오브젝트 감지:**
`SpatialTapGesture()`를 사용해 사용자가 오브젝트에 핀치하는 순간을 감지한다. 이때만 사용자가 특정 오브젝트를 응시하고 있었는지 여부를 알 수 있다. 이 Pinch 상호작용 이전에는 시스템이 gaze 관련 데이터를 접근할 수 없게 해두었다.

```swift
.gesture(
    SpatialTapGesture()
        .targetedToAnyEntity()
        .onEnded { value in
            if let indexStr = value.entity.name.split(separator: "_").last,
               let index = Int(indexStr) {
                highlightedIndex = index
                eyeTrackingModel.updateGazedObject(name: value.entity.name)
            }
        }
)
```

**(3) 실시간 material 업데이트:**
RealityView의 `update` closure를 사용해 gaze+pinch가 이뤄진 오브젝트를 초록색으로 업데이트한다. Material 업데이트 외에 다른 액션들도 이런 방식으로 eventhandling을 할 수 있다.

```swift
} update: { content in
    for (index, sphere) in sphereEntities.enumerated() {
        let isHighlighted = index == highlightedIndex
        let color: UIColor = isHighlighted ? .green : .gray
        var material = SimpleMaterial(color: color, isMetallic: false)
        sphere.model?.materials = [material]
    }
}
```

# 참고자료

- [visionOS Get Started](https://developer.apple.com/visionos/get-started/)
- [Eyes & Interaction](https://developer.apple.com/design/human-interface-guidelines/eyes)
- [RealityKit Documentation](https://developer.apple.com/documentation/realitykit)
- [visionOS Documentation](https://developer.apple.com/documentation/visionos)

# 변경사항

- Jul 2, 2026: 게시물 작성
