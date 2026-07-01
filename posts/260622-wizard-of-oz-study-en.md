---
title: Wizard of Oz Study: The Spirit of HCI Research
date: 2026-06-22
tag: Reading
---

A Wizard of Oz (WoZ) study is an experiment where researchers observe users while deceiving them into believing an incomplete system is fully functional. Users think they're interacting with an autonomous computing system, but in reality, a hidden human operator (the "wizard") is controlling the system behind the scenes. Much like in the classic story.

WoZ studies beautifully reflects the culture of HCI research, showing the attitude that we can study future interactions even without fully realized technology today. In this article, we look at the brief historical background of WoZ, the unique benefits this approach brings, and the broader concept of Proof-of-Concept simulation that HCI researchers value.

# History of Wizard of Oz Study

The first instances appeared in early 1980s HCI research that hid human operators to simulate non-existent technology ([Gould et al.'s "Simulated Listening Typewriter"](http://doi.org/10.1145/2163.358100) and [John F. Kelley's 1983 CHI paper](http://doi.org/10.1145/800045.801609)). They wanted to understand how users would actually interact with a natural language interface. But building a complete natural language processing system would take decades. Instead, human operators (behind the curtain) simulated the system by listening to user questions and responding as if the computer understood naturally. This allowed them to observe authentic user experience and interaction decades before the technology could be realized.

![|90%](img/posts/260622-wizard-of-oz-study/wizard-of-oz-example.jpg)

This was very interesting approach. "Time-travel" the user experience before the technology even exists. Since then, the Wizard of Oz method has become one of the standard tools in HCI research.

# Why Simulate Before Building?

There's a key question that distinguishes HCI from pure engineering: before asking "Can we build this?", we first ask "How will people interact with this once it's built?" In most engineering disciplines, the typical sequence is: build the system → optimize performance → conduct internal evaluation → deploy to real users. By then, months are invested. What if there were fundamental problems in the initial interaction model and design?

WoZ inverts this order. It carefully observes first how users would behave, what they expect, and where they encounter obstacles when confronted with such a system. **This attitude of asking "Does this interaction make sense?" before "Is this technology feasible?" reflects the academic spirit that has defined HCI research from its beginning.** It's precisely why HCI research often involves prototypes, simulations, and approximations. And perhaps this is a point that might make those from traditional engineering backgrounds uncomfortable. The goal is not to ship a finished product today. It's to understand and envision the future. I believe this is the direction that research, in general (not just our field), should pursue.

# The Broader Spirit of HCI: Proof-of-Concept Simulation

I view WoZ study as a case of a more general concept: Proof-of-Concept (PoC) simulation. WoZ studies refer only to methods where human operators simulate autonomous system (like conversational agents or voice interfaces), but modern HCI research actively employs simulation across a much broader spectrum. Researchers go beyond WoZ, using various  approximations methods to simulate future systems, and through this, we can answer questions like:

* **What level of performance and task load will future systems deliver?**
* **Do users actually want this capability?**
* **How do users respond when the system malfunctions or fails?**
* **Do users interact as designers intended, or do they find unexpected uses?**

## Example 1: [STAR Project](https://arxiv.org/pdf/2511.21143) (Kim et al. UIST 2023)

![|60%](img/posts/260622-wizard-of-oz-study/star-example.jpg)

The research question is: "Can we transfer the familiar skill of two-thumb typing on smartphones to a freehand AR environment?" And we proposed STAR, an idea where AR glasses display project a virtual QWERTY keyboard above the user's hands, with the skin surface serving as the typing surface instead of a touchscreen (using thumb taps for input). However, fully realizing this with technology at the time (2022) was a challenging problem.

While we used the hand tracking and display capability provided by Hololens 2 (to ground our work in realistic technology), reliably detecting the subtle contact between thumb and skin was infeasible. **Thus we simulated perfect touch detection using a capacitive tape strip (technology unavailable at the time, but we anticipated it would become feasible with more sophisticated vision-based hand tracking or integration with wearables like smart rings and watches. Indeed, in 2025, Meta Neural Band appeared and demonstrated very stable thumb tap detection).** Eventually, rather than waiting for high-performance vision and sensing technology to arrive on the market, we built a PoC prototype to explore questions like: (1) Can people transfer their decades-trained smartphone typing skill to an AR freehand environment? (2) How close can STAR technique's typing performance get to actual smartphone typing? While this is not a Wizard of Oz study, it is a PoC simulation performed with precisely the same purpose.

## Example 2: [HiFiGaze Project](https://arxiv.org/pdf/2603.19588) (Kim et al. CHI 2026)

![|70%](img/posts/260622-wizard-of-oz-study/hifigaze-example.jpg)

This work presented a deep learning-based eye tracking model for smartphones. However, we discovered that when users gaze at the lower portion of the screen (from the front camera perspective), eyelids and eyelashes often occlude the eye features our model relies on.

**As a supplementary study, we posed a pinpointed question: "If the camera were positioned at the bottom instead of the top, could this problem be resolved and performance improved?"** But no such smartphone exists, and disassembling an iPhone to add another camera of equal capability at the bottom would be practically hard. Instead of overcomplicating things, we simply rotated the phone 180 degrees to position the camera at the bottom, and inverted the display so that users saw no difference when viewing the screen. Eventually we could immediately explore our research question without waiting for a completely new device to be manufactured (the study results are detailed in the paper). Like the STAR case, this is not a Wizard of Oz study, but it was conducted with the same purpose: simulating conditions we anticipate will be feasible in the future using current approximations, measuring outcomes, and expanding our understanding.

# References

* Kelley, J. F. An empirical methodology for writing user-friendly natural language computer applications. CHI 1983. https://doi.org/10.1145/800045.801609
* Gould, J. D., Conti, J., & Hovanyecz, T. Composing Letters with a Simulated Listening Typewriter. Communications of the ACM 1983. https://doi.org/10.1145/2163.358100
* Kim, T., Karlson, A., Gupta, A., Grossman, T., Wu, J., Abtahi, P., Collins, C., Glueck, M., & Surale, H. B. STAR: Smartphone-analogous Typing in Augmented Reality. UIST 2023. https://arxiv.org/pdf/2511.21143
* Kim, T., Mollyn, V., Arakawa, R., & Harrison, C. HiFiGaze: Improving Eye Tracking Accuracy Using Screen Content Knowledge. CHI 2026. https://arxiv.org/pdf/2603.19588
* Hyungtae Lim. Wizard of Oz Study. https://limhyungtae.github.io/2026/05/17/hci-note-wizard-of-oz-study/

# Changelog

- Jun 22, 2026: Post published
