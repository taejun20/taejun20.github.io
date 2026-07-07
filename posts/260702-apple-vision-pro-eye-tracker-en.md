---
title: Eye Tracker: Apple Vision Pro (How To Use)
date: 2026-07-02
tag: Eye Tracking
---

[Apple Vision Pro](https://www.apple.com/apple-vision-pro/) XR headset has eye tracking capabilities. Released in 2024, it provides quite accurate eye tracking and uses it as a core feature for interaction and gaze-aware experiences.

```note
**Key Limitation:** Unfortunately, access to eye tracking signals on Apple Vision Pro is very restricted. Unlike [Meta Quest Pro](/p/260625-meta-quest-pro-eye-tracker-en) and [FOVE VR](/p/260625-fove-vr-eye-tracker-en) (which provide raw gaze ray data), Apple explicitly blocks developers from accessing raw eye tracking information. Instead, applications interact with gaze through high-level system APIs (focus, hover, and selection) on target object-basis. This is an intentional privacy-focused design by Apple.
```

![|80%](img/posts/260702-apple-vision-pro-eye-tracker/vision-pro-demo.jpg)

# 1. Connect with Mac

First, establish a connection between your Vision Pro and your Mac.

## 1-1. PC Side Setup

**(1) Configure Xcode:**
Set up Xcode on your Mac. Download the Vision OS Platform at XCode - Settings - Components, and create an empty visionOS project. Make sure your Vision Pro device is selected as a build target, and minimum deployment OS version properly set.

![|100%](img/posts/260702-apple-vision-pro-eye-tracker/xcode-setup.png)

**(2) Pair Device:**
Connect Vision Pro to your Mac wirelessly (or with USB-C) using Xcode.

## 1-2. Vision Pro Side Setup

**(1) Enable Developer Mode:**
Settings → About → Developer Mode. Turn on.

**(2) Enable Eye Tracking:**
Settings → Accessibility → Eye Tracking. Turn on.

# 2. Program with Xcode

I made a [simple demo](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/AppleVisionPro) that you can clone and run directly. Settings used:

- Mac Air (M3)
- macOS 26.5.2
- Xcode 26.4.1
- visionOS Xcode SDK 26.4
- Apple Vision Pro device

![|100%](img/posts/260702-apple-vision-pro-eye-tracker/vision-pro-demo.gif)

## Tips

First, read the official Apple visionOS documentation: [visionOS Get Started](https://developer.apple.com/visionos/get-started/), [Eyes & Interaction](https://developer.apple.com/design/human-interface-guidelines/eyes), [RealityKit Documentation](https://developer.apple.com/documentation/realitykit), and [visionOS Documentation](https://developer.apple.com/documentation/visionos).

Let me briefly describe some key components in my Xcode project: [ImmersiveView.swift](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/AppleVisionPro/AppleVisionPro/ImmersiveView.swift)

**(1) RealityKit scene + gaze-reactive objects setup:**
In [ImmersiveView.swift](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/AppleVisionPro/AppleVisionPro/ImmersiveView.swift), I created a `RealityView` (from RealityKit) with an `AnchorEntity` as the root. Add `InputTargetComponent` and `HoverEffectComponent` to each entity you want to make interactive. This enables the system's built-in gaze detection and hover visual feedback.

```swift
let sphere = ModelEntity(mesh: mesh, materials: [material])
sphere.components.set(InputTargetComponent())
sphere.components.set(HoverEffectComponent())
sphere.components.set(CollisionComponent(shapes: [.generateSphere(radius: 0.15)]))
```

**(2) Pinch and gazed-at-pinch-time object detection:**
Use `SpatialTapGesture()` to detect the moment the user pinches on an object. Only then can you determine if the user was gazing at that specific object. Before this pinch interaction, the system prevents access to any gaze-related data.

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

**(3) Real-time material updates:**
Use the RealityView's `update` closure to update gazed+pinched objects to green. You can ofc involve other actions than material updates this way.

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

# References

- [visionOS Get Started](https://developer.apple.com/visionos/get-started/)
- [Eyes & Interaction](https://developer.apple.com/design/human-interface-guidelines/eyes)
- [RealityKit Documentation](https://developer.apple.com/documentation/realitykit)
- [visionOS Documentation](https://developer.apple.com/documentation/visionos)

# Changelog

- Jul 2, 2026: Post published
