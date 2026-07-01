---
title: Eye Tracker: Meta Quest Pro (How To Use)
date: 2026-07-01
tag: Eye Tracking
---

[Meta Quest Pro](https://www.meta.com/quest/quest-pro/) is the only Meta VR headset with eye tracking support. Released in 2022 ($1500) and discontinued in 2025, now available through secondhand. It is still a leading device for HCI research requiring both fine hand tracking and eye tracking simultaneously.

![Meta Quest Pro headset|80%](img/posts/260625-meta-quest-pro-eye-tracker/quest-pro-setup.jpg)

# 1. Connect with PC via Link

First, establish a connection between your Quest Pro headset and your PC using Horizon Link (only Windows PC supported).

## 1-1. PC Side Setup

**(1) Download and Install Meta Horizon Link:**
Download the [Meta Horizon Link app](https://www.meta.com/help/quest/509273027107091/) in your Windows PC.

**(2) Enable Eye Tracking in Meta Horizon Link:**
Open Meta Horizon Link. Go to Settings → Developer. Enable Eye Tracking over Meta Horizon Link

**(3-a) Wired Connection:**
Use a USB-C 3 cable (minimum 5 Gbps) to connect your Meta Quest Pro directly to your PC.

**(3-b) Wireless Connection (Air Link):**
Alternatively, you can use Air Link for wireless connectivity. Put your PC and Quest Pro are on the same Wi-Fi network (should be fast, 5 GHz) and set up in the Meta Horizon Link.

## 1-2. Headset Side Setup

On your Meta Quest Pro headset, enable the necessary tracking features:

**(1) Enable Eye Tracking:**
Go to Settings → Tracking → Eye Tracking. Turn on.

**(2) Enable Quest Link:**
Go to Settings → Link. Turn on.

Once both sides are configured, your Meta Quest Pro will be ready to send eye tracking data to your PC via Link.

# 2. Program with Unity

I made a [simple Unity demo](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/MetaQuestPro) that you can clone and run directly. Settings used:

- Windows PC
- Unity 2021.3.45f2
- Meta XR Core SDK (not the full Movement SDK for a simple demo)
- Meta Quest Pro device

![Unity demo: gaze-object collision and printing raw signals.|100%](img/posts/260625-meta-quest-pro-eye-tracker/qpro-demo.gif)

## Tips

First and foremost, read the Meta official guides: [Eye Tracking for Movement SDK for Unity](https://developers.meta.com/horizon/documentation/unity/move-eye-tracking/), [Getting Started with Meta XR](https://developers.meta.com/horizon/documentation/unity/move-unity-getting-started/), [Meta Quest Hello World Tutorial](https://developers.meta.com/horizon/documentation/unity/unity-tutorial-hello-vr/).

Let me briefly describe the [MetaQuestProEyeDemoController.cs](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/MetaQuestPro/Assets/Scripts/MetaQuestProEyeDemoController.cs) in my demo Unity project.

**(1) Attach `OVREyeGaze` to the eyeball:** Create empty GameObject and place it under the OVRCameraRig/TrackingSpace. This will represent the eyeball. Attach the `OVREyeGaze` component script to it.

![|80%](img/posts/260625-meta-quest-pro-eye-tracker/ovreyegaze-attach.jpg)

**(2) Access the eye tracking signals in code:**

```csharp
// Get both left and right OVREyeGaze components
OVREyeGaze leftEyeGaze = leftEyeGazeTransform.GetComponent<OVREyeGaze>();
OVREyeGaze rightEyeGaze = rightEyeGazeTransform.GetComponent<OVREyeGaze>();

// Combine gaze rays from both eyes
var origin = (leftEyeGazeTransform.position + rightEyeGazeTransform.position) / 2f;
var direction = (leftEyeGazeTransform.forward + rightEyeGazeTransform.forward).normalized;
Ray gazeRay = new Ray(origin, direction);

// Raycast to detect gaze-object collision
if (Physics.Raycast(gazeRay, out var hit))
{
    GameObject gazedObject = hit.collider.gameObject;
}

// Check eye tracking validity
if (leftEyeGaze.enabled && leftEyeGaze.EyeTrackingEnabled && leftEyeGaze.Confidence >= leftEyeGaze.ConfidenceThreshold)
{
    // Eye tracking is active and reliable
}
```

# References

- [Eye Tracking for Movement SDK for Unity](https://developers.meta.com/horizon/documentation/unity/move-eye-tracking/)
- [Getting Started with Meta XR](https://developers.meta.com/horizon/documentation/unity/move-unity-getting-started/)
- [Meta Quest Hello World Tutorial](https://developers.meta.com/horizon/documentation/unity/unity-tutorial-hello-vr/)
- [Meta Quest Pro Official Page](https://www.meta.com/quest/quest-pro/)

# Changelog

- Jul 1, 2026: Post published
