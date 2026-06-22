---
title: Wizard of Oz Study: The Spirit of HCI Research
date: 2026-06-22
tag: Reading
---

Wizard of Oz (WoZ) study is a research method that makes users believe they're interacting with an autonomous system, but actually a hidden human operator (the "wizard") is partially or fully controlling it. This approach gracefully reflects the spirit of HCI research, which prioritizes understanding human experience before investing in the full system.

In this post, we'll look at the historical background of WoZ, why this approach has unique benefits, and the broader spirit it shares.

# History of Wizard of Oz Study

The term comes from the classic metaphor: the Wizard of Oz appeared as a powerful magical figure, but behind the curtain was just a person pulling levers.

First instances of hidden-human simulation appeared in HCI in the early 1980s, including [Gould et al.'s "Simulated Listening Typewriter"](http://doi.org/10.1145/2163.358100) and [John F. Kelley's 1983 CHI paper](http://doi.org/10.1145/800045.801609), which introduced the "OZ paradigm." They wanted to study how users would interact with a natural language interface, but building a complete natural language processing system would take years. Instead, they had a human operator listen to user queries and respond as if the system understood them naturally. This let them observe authentic user behavior without waiting for the technology to mature.

![|90%](img/posts/260622-wizard-of-oz-study/wizard-of-oz-example.jpg)

The insight was simple but powerful: the interaction pattern, not the implementation, is what you need to understand first. "Time-travel" the user experience first before the technology exists. Since then, WoZ studies have become a standard tool in HCI research.

# Why Simulate Before Building?

Here's the key research question that separates HCI from pure engineering: **Before asking "Can we build this?", ask "How will people interact with this?"** In most engineering, the typical path is: build system → optimize performance → run evaluation → hope users want it. By then, months are invested. If the interaction model is fundamentally wrong, it's too late.

WoZ inverts this order. It observes user behavior first by carefully simulating a future system before committing to full implementation. This lets researchers understand how users will behave when such a system actually exists, what they expect, and where they encounter obstacles. In other words, the WoZ study asks "Does this interaction make sense?" before asking "Is this technology possible?" This ordering has defined HCI research from the start. It's why HCI researchers often work with prototypes, simulations, and approximations that would make traditional engineers uncomfortable. The goal isn't to ship a finished product today. It's to understand and envision the future. The true direction where "research" should go.

# The Broader Spirit of HCI: Proof-of-Concept Simulation

I view WoZ study as part of the broader spirit of HCI research: **Proof-of-Concept (PoC) simulation**. Traditionally WoZ study refers to methods involving a human operator who simulates an autonomous system (such as conversational agents, speech interfaces). But modern HCI research uses simulation in general far more broadly. Beyond WoZ, researchers now simulate future systems using whatever approximations are available. The goal is to answer critical questions earlier, such as:

* **What performance levels and real-world task loads will the system deliver?**
* **Do users actually want this capability?**
* **How do users respond when the system fails?**
* **Do users interact with it as intended, or do they find unexpected uses?**

By observing real behavior in a simulated environment, researchers can answer these questions before investing in full implementation. This is where PoC simulation shines. And I think this is the strong spirit that HCI researchers share, one that descended from the field pioneers. Let me illustrate this with some examples from papers of my team:

## Example 1: [STAR Project](https://arxiv.org/pdf/2511.21143) (Kim et al. UIST 2023)

![|60%](img/posts/260622-wizard-of-oz-study/star-example.jpg)

We wanted to explore: can we transfer smartphone two-thumb typing skills to bare-hand AR? The vision was overlaying a virtual QWERTY keyboard on users' bare hands via AR glasses, responding to thumb taps on skin. But this required expensive, imperfect technologies of integrated hand-tracking, robust tap detection, AR displays.

We used HoloLens's default AR rendering and hand tracking, but **simulated future on-skin tap detection using a capacitive tape strip (unavailable in contemporary AR glasses)**, letting users two-thumb type on this setup. The interaction was real; the sensing was simulated. We could then ask: **Will users transfer their smartphone typing skills to AR? How much typing speed do they reach compared to actual smartphones?** We learned this before investing in production-grade sensing. Not technically WoZ (no human operator). But same spirit: approximate future conditions and observe behavior and experience.

## Example 2: [HiFiGaze Project](https://arxiv.org/pdf/2603.19588) (Kim et al. CHI 2026)

![|70%](img/posts/260622-wizard-of-oz-study/hifigaze-example.jpg)

We presented a novel deep learning model for eye tracking on smartphones (using the built-in front camera). In our evaluation, we discovered that upper eyelids and lashes occlude eye features our approach relies on, especially when users fixate near the bottom of the screen.

We hypothesized a bottom-positioned camera could sidestep this occlusion. But no such smartphone exists, and building a custom prototype is expensive. Instead, we flipped the iPhone 180 degrees to position the camera at the bottom, inverted the display, and ran the same algorithm. **We could then test: Does moving the camera to the bottom reduce occlusion errors? Without manufacturing a new device.** The results informed future smartphone design. Again not traditional WoZ, but same spirit: simulate future hardware conditions using available approximations, measure outcomes, then distill understanding for future systems.

# References

* Kelley, J. F. An empirical methodology for writing user-friendly natural language computer applications. CHI 1983. https://doi.org/10.1145/800045.801609
* Gould, J. D., Conti, J., & Hovanyecz, T. Composing Letters with a Simulated Listening Typewriter. Communications of the ACM 1983. https://doi.org/10.1145/2163.358100
* Kim, T., Karlson, A., Gupta, A., Grossman, T., Wu, J., Abtahi, P., Collins, C., Glueck, M., & Surale, H. B. STAR: Smartphone-analogous Typing in Augmented Reality. UIST 2023. https://arxiv.org/pdf/2511.21143
* Kim, T., Mollyn, V., Arakawa, R., & Harrison, C. HiFiGaze: Improving Eye Tracking Accuracy Using Screen Content Knowledge. CHI 2026. https://arxiv.org/pdf/2603.19588
* Hyungtae Lim. Wizard of Oz Study. https://limhyungtae.github.io/2026/05/17/hci-note-wizard-of-oz-study/

# Changelog

- Jun 22, 2026: Post published
