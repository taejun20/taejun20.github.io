---
title: Eye Tracker: FOVE VR (How To Use)
date: 2026-06-30
tag: Eye Tracking
---

[FOVE](https://fove-inc.com/product/fove0/) is a VR headset with built-in eye tracking. It is regarded as the world's first commercially available eye tracking VR headset, which was released in **2016**. Even today, with Meta and Apple manufacturing leading products like the Quest Pro and Vision Pro, I feel FOVE has its uniqueness: it is far more lightweight.

The hardware is simple and [system source codes](https://github.com/FoveHMD) are open. Apple Vision Pro or Meta Quest Pro is considerably heavier as it bundles other capabilities like hand tracking and 3D space scanning. FOVE only cares about VR graphic rendering and eye tracking, and provide real-time eye camera feeds, gaze vectors, blink status, and inter-pupillary distance in a straightforward way. Note that other research-grade devices that open such signals easily cost above $10,000. FOVE is $1,500.

![FOVE 0 headset|80%](img/posts/260625-fove-vr-eye-tracker/fove1.jpg)


# 1. Install FOVE VR Platform (Desktop App)

**(1) Request the Download:** fill out the [official contact form](https://fove-inc.com/fove-vr-platform-contact/) and they'll email you the `.msi` installer for FOVE VR Platform (desktop app) along with a license key `.txt` file. They respond quite quickly.

**(2) Install and Activate License:** run the `.msi` installer. Once installation completes, a license activation window appears. Copy the license key from the `.txt` file and paste it in.

# 2. Explore FOVE VR Platform

Once installed, you can find the "FOVE VR" app in the Windows Start Menu. It stays in the bottom-right corner, and you can run several functionalities like Debug Tool (see below).

### (1) Debug Tool

![FOVE VR desktop app: Debug Tool (You'll get an English UI if you specify the region in the contact form)|100%](img/posts/260625-fove-vr-eye-tracker/fove2.jpg)



This already gives you several useful information. Live eye video, real-time head rotation and translation state, eye tracking signals, and a button to start **Calibration**. You will use this window to check if the tracking is correctly working and to initiate calibration for each participant in user study.

### (2) Mirror Client View

![FOVE VR desktop app: Mirror Client|100%](img/posts/260625-fove-vr-eye-tracker/fove3.jpg)

The mirror view shows the (binocular) rendered scene, what the user sees in real time.

# 3. Program with Unity

I made a [simple Unity demo](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/FOVE) that you can clone and run directly. Settings used:

- Windows
- Unity 2021.3.45f2
- FOVE 0 device

![Unity demo: gaze ray visualization, gaze-object collision, and printing raw signals.|100%](img/posts/260625-fove-vr-eye-tracker/fove5.gif)

## Tips

First and foremost, refer to the FOVE official guides: [Unity Plugin Guide](https://github.com/FoveHMD/UnityPlugin/blob/master/PluginGuide.md) and [Quick Start Guide](https://github.com/FoveHMD/UnityPlugin/blob/master/QuickStart.md).

Let me briefly describe the [FoveGazeDemoController.cs](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/FOVE/Assets/Scripts/FoveGazeDemoController.cs) in my demo Unity project.

**(1) First, include the FOVE modules:**

```csharp
using Fove;
using Fove.Unity;
```

**(2) Next, the main entry point is registering the capabilities you need:**

```csharp
FoveManager.RegisterCapabilities(ClientCapabilities.EyeTracking |
    ClientCapabilities.GazedObjectDetection |
    ClientCapabilities.UserIPD |
    ClientCapabilities.EyeBlink);
```

**(3) Then in the main loop (e.g., `Update`, `LateUpdate`), you can access the signals:**

```csharp
Result<Ray> ray = foveInterface.GetCombinedGazeRay();
Result<GameObject> gazed = FoveManager.GetGazedObject();
Result<bool> leftBlink  = FoveManager.IsEyeBlinking(Eye.Left);
Result<bool> rightBlink = FoveManager.IsEyeBlinking(Eye.Right);
```

All return a `Result<T>`. Check `.IsValid` before using `.value`.

**(4) Full list of accessible signals:**

```csharp
// Gaze rays (world space — via FoveInterface)
Result<Ray> combinedRay = foveInterface.GetCombinedGazeRay();
Result<Ray> leftRay     = foveInterface.GetGazeRay(Eye.Left);
Result<Ray> rightRay    = foveInterface.GetGazeRay(Eye.Right);
Result<float> gazeDepth = foveInterface.GetCombinedGazeDepth(); // distance where left & right gaze rays converge

// Gazed object
Result<GameObject> gazed = FoveManager.GetGazedObject();

// Blink
Result<bool> leftBlink      = FoveManager.IsEyeBlinking(Eye.Left);
Result<bool> rightBlink     = FoveManager.IsEyeBlinking(Eye.Right);

// Eye state & attention
Result<EyeState> leftState  = FoveManager.GetEyeState(Eye.Left);  // Opened / Closed / NotDetected — finer than IsEyeBlinking
Result<EyeState> rightState = FoveManager.GetEyeState(Eye.Right);
Result<bool> shiftingAttn   = FoveManager.IsUserShiftingAttention(); // true during saccades; filter out for stable fixation data

// Eye geometry
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

// Eye camera image
Result<Texture2D> eyesImage = FoveManager.GetEyesImage();

// Head pose
Result<Quaternion> hmdRotation = FoveManager.GetHmdRotation();
Result<Vector3>    hmdPosition = FoveManager.GetHmdPosition(isUserStanding: true);

// Timestamps
Result<FrameTimestamp> eyeDataTimestamp = FoveManager.GetEyeTrackingDataTimestamp();
```

# References

- [FOVE official site](https://fove-inc.com/)
- [Getting Started With FOVE – official guide](https://support.fove-inc.com/Getting-Started-With-FOVE-6e81882b908446d4b4f100ceb70eeab0)

# Changelog
- Jun 30, 2026: Post published
