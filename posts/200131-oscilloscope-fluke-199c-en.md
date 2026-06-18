---
title: Oscilloscope (Fluke 199C): How to Use
date: 2020-01-31
tag: Electronics
---

An oscilloscope displays voltage signals as a graph over time. While a multimeter gives you a single number for voltage, current, or resistance, an oscilloscope lets you see the waveform itself: its shape, period, and amplitude. Here's a quick guide to the Fluke 199C ScopeMeter that our lab has.

![Fluke 199C ScopeMeter|60%](img/posts/200131-oscilloscope-fluke-199c/overview.jpg)

The Fluke 199C works as both a scope and a multimeter. Press the yellow Scope button for scope mode, or the Meter button below it for multimeter mode.

# Scope Mode

![|60%](img/posts/200131-oscilloscope-fluke-199c/scope-screen.jpg)

- Vertical grid: 1 div = 20V / Horizontal grid: 1 div = 2ms (the example above shows ~60V AC)
- Trig (bottom center): triggering info. Shown dimmed when no trigger is detected.
- Probe 10:1: a 10:1 probe is in use. The probe divides the signal by 10 internally, but the scope compensates automatically, so the voltage shown on screen is the real signal voltage.
- AUTO mode: automatically sets vertical scale, horizontal scale, and triggering. Toggle with the teal Auto/Manual button.
- Additional notes:
  - Press the purple Hold/Run button to freeze the screen.
  - To reset all scope settings: power off, hold the User button (bottom right), then power on. Two beeps (beep beep) confirm the reset.

## Scope Mode Key Label Menu

![|70%](img/posts/200131-oscilloscope-fluke-199c/scope-menu.jpg)

Press the Scope button again to hide the labels. Or press the rightmost Clear menu button.

- **F1 (Readings on/off)**: Toggle the readings display on or off.
- **F2, F3 (Readings 1, 2)**: Choose what value each reading shows (V, Vpp, A, Hz, W, etc.). You can use one or both.
- **F4 (Waveform Options...)**: Configure waveform settings.
  - Average section: selecting Average 64, for example, averages 64 samples to reduce noise and smooth the waveform.
  - Other options include Glitch Detection and Mathematics (e.g., adding Input A and B waveforms).

# Meter Mode

![|60%](img/posts/200131-oscilloscope-fluke-199c/meter-screen.jpg)

The meter mode screen is relatively simple: a main measurement reading and a bar graph below. Manual means the range is set manually (0 to 50kΩ).

## Meter Mode Key Label Menu

![|70%](img/posts/200131-oscilloscope-fluke-199c/meter-menu.jpg)

Press the Meter button again to hide the labels.

- **F1 (Measure...)**: Select what to measure (kΩ, V, A, etc.).
- **F2 (Relative on/off)**: Shows values relative to the reading at the moment you pressed this button (+ or -).
- **F3, F4 (Auto, Manual)**: Default is Auto, which automatically selects the measurement range (shown in the bar graph below the reading). Switch to Manual to set the range yourself. Toggle with F3/F4 or the teal Auto/Manual button.
- The purple Hold/Run button captures the screen here too.

# Beyond Scope and Meter

There's also a Recorder mode. Features like Cursor, Zoom, and Replay exist as well. I'll document those if I ever get to use them.

# Changelog
- Jan 31, 2020: Post published
- Dec 1, 2021: Migrated to Velog
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
