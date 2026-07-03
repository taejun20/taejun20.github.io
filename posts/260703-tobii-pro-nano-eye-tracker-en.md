---
title: Eye Tracker: Tobii Pro Nano/Spark/Fusion (How To Use)
date: 2026-07-03
tag: Eye Tracking
---

[Tobii Pro](https://www.tobii.com/products/eye-trackers/screen-based) series are research-grade eye trackers.

```note
**Strength:** Tobii Pro devices (Nano, Spark, Fusion, Spectrum) come with embedded license, pre-activated on the hardware at the factory time. Just connect it to your PC, no additional registration or license activation. I love this.
```

![Tobii Pro Nano (now discontinued, replaced by Tobii Pro Spark)|100%](img/posts/260703-tobii-pro-nano-eye-tracker/tobii-nano-etm.jpg)

![|80%](img/posts/260703-tobii-pro-nano-eye-tracker/tobii-nano-setup.jpg)

# 1. Install, Mount, and Configure

First, read the official Tobii documentation: [Install Manager Software](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US) & [Mount the Device](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US) & [Configure.](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US)

**(1) Install Tobii Pro Eye Tracker Manager:** connect the eye tracker to the PC via USB (I am using Windows), download the [Tobii Pro Eye Tracker Manager](https://connect.tobii.com/s/etm-downloads?language=en_US), and install.

![|80%](img/posts/260703-tobii-pro-nano-eye-tracker/tobii-etm-calibration.jpg)

**(2) Mount the tracker:** follow the [official instructions for Mounting](https://connect.tobii.com/s/article/Mount-Tobii-Pro-Fusion-on-the-screen-Step-2?language=en_US) and attach it beneath your display.

**(3) Configure the tracker:** do [setup](https://connect.tobii.com/s/article/Install-Tobii-Pro-Fusion-on-your-computer-Step-1?language=en_US) in the Tobii Pro Eye Tracker Manager program.

# 2. Program with Python

I made a [simple Python demo](https://github.com/taejun20/EyeTrackerDemo-Blog/tree/main/TobiiProNano) that you can clone and run directly. Settings used:

- Windows 
- Python 3.10 (in conda environment)
- Tobii Pro SDK (in conda environment: pip install tobii_research)
- Tobii Pro Nano device

![|100%](img/posts/260703-tobii-pro-nano-eye-tracker/tobii-nano-demo.gif)

## Tips

First, check the official Tobii documentation: [Tobii Pro SDK](https://developer.tobiipro.com/index.html), [Python Getting Started](https://developer.tobiipro.com/python/python-getting-started.html), [Official Python Code Samples](https://developer.tobiipro.com/c/c-sdk-reference-guide.html)

Let me briefly describe the [app.py](https://github.com/taejun20/EyeTrackerDemo-Blog/blob/main/TobiiProNano/app.py) in my simple demo.

**(1) Connect to tracker:**
Find the Tobii tracker and subscribe to real-time gaze updates.

```python
def discover_trackers():
    trackers = list(tobii_research.find_all_eyetrackers())
    return trackers[0]

# In ExperimentWindow.__init__:
self.tracker = discover_trackers()
self.tracker.subscribe_to(tobii_research.EYETRACKER_GAZE_DATA, self.gaze_callback, as_dictionary=True)
self.subscribed = True
```

**(2) Process gaze data:**
Extract gaze points from left and right eyes, handling validity checks.

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

**(3) Detect gaze hit:**
Use distance calculation to detect when gaze hits each circle.

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

# References

- [Tobii Pro](https://www.tobii.com/products/eye-trackers/screen-based)
- [Tobii Pro SDK](https://developer.tobiipro.com/index.html)

# Changelog

- Jul 3, 2026: Post published
