---
title: Transistor (1): Basics
date: 2019-11-12
tag: Electronics
---

Working on the [Heterogeneous Stroke](https://github.com/taejun20/HeterogeneousStroke) project, I had to supply stable voltage to four ERM vibration motors while controlling them independently. For that, I added a [2N2369 transistor](https://www.elektronik-kompendium.de/public/schaerer/FILES/2n2369.pdf) to the circuit. Let me document the role and operating principles of transistors.

![2N2369 Transistor (NPN)|40%](img/posts/191112-transistor-basics/transistor-2n2369.png)

There are two main types of transistors: BJT (Bipolar Junction Transistor) and FET (Field Effect Transistor). The role is essentially the same. Amplification and Switching. The key difference is that a BJT is controlled by a current input, while a FET is controlled by voltage. The rest of this post goes with the BJT transistor.

# Role of a Transistor

A transistor serves two main purposes: 1) amplification and 2) switching. How do these work? (Note: amplification here does not mean creating new energy. It means using energy from an external supply (VCC), using a small change in Base current as a much larger change in Collector current. VCC is the ceiling; the transistor acts as a valve that scales the signal within that range.)

For an NPN transistor: the Collector is the inlet, the Emitter is the outlet, and the Base is the faucet handle. Opening the faucet more increases the current flowing from Base to Emitter.

![PNP/NPN transistor circuit symbols and faucet analogy](img/posts/191112-transistor-basics/pnp-npn-valve.png)

Depending on the Base current (I_B), the transistor operates in one of three regions described by the Collector-Emitter Voltage (V_CE) vs. Collector Current (I_C) curve:

![Practical Electronics For Inventors (2nd Edition), Figure 4.47, p.442](img/posts/191112-transistor-basics/iv-curve.png)

1. **Cut-off Region**: When Base current (I_B) = 0: the faucet is fully closed. The transistor acts like an open switch between Collector and Emitter. No matter how large V_CE is, essentially no current flows through the Collector. (A negligible leakage current does exist in practice.)

2. **Active Region**: The faucet is partially open and controls how much current flows. This is where the transistor operates as an amplifier. At a fixed V_CE of 5V, as I_B increases from 0 mA to 0.4 mA, I_C increases proportionally. This relationship is expressed as **I_C = β × I_B**, where β is the current gain (also called h_FE): the ratio by which Base current is reproduced at the Collector. For example, with β = 100 and I_B = 1 mA, the Collector carries 100 mA. That 100 mA comes from the external supply (VCC), not from the transistor itself: the transistor simply opens the valve proportionally. β is unique to each transistor, typically between 10 and 500, and can vary slightly with temperature.

3. **Saturation Region**: The Collector current has reached its maximum for a given V_CE. Increasing I_B further no longer increases I_C.

Using the transistor within the Active Region enables it as an amplifier. Rapidly switching between Cut-off (off) and Saturation (fully on) enables it as a switch. The ERM motor control mentioned at the start uses this switching approach: an Arduino digital output turns the Base on and off to independently control each motor.

# Physical Operating Principle

Pure silicon (Si) is an insulator. Adding boron (B) creates P-type semiconductor (electron-deficient, dominated by holes); adding phosphorus (P) creates N-type semiconductor (electron-rich). When P-type and N-type are joined, current flows from P to N but not from N to P: this is **rectification**, also the basis for P-N junction diodes. Stacking P-N-P gives a PNP transistor; N-P-N gives an NPN transistor.

![Example circuit to illustrate NPN transistor operation|70%](img/posts/191112-transistor-basics/npn-circuit.png)

In the diagram, the right-side reverse bias (N→P) blocks current. The left-side forward bias (N connected to (−), P to (+)) pushes holes in the P-type toward the junction and electrons in the N-type toward the junction: current flows. Most electrons from the Emitter (N) pass straight through the thin Base layer (P) into the Collector: that's I_C. A small fraction recombine with holes in the Base: that's I_B. Slightly increasing I_B proportionally increases I_C. This ratio is the Current Gain (β = I_C / I_B), and it's how a small change at the Base produces a large change at the Collector.

Continued: [Transistor (2): Transistor with Arduino](/posts?post=220309-transistor-arduino)

# References

- Paul Scherz. 2006. *Practical Electronics for Inventors* (2nd ed.). McGraw-Hill.
- [Transistor Summary – Naver Blog](https://m.blog.naver.com/okseods1/220949581522)
- [Transistor – Tistory](https://gigawatt.tistory.com/124)

# Changelog
- Nov 12, 2019: Post published
- Dec 1, 2021: Migrated to Velog
- Feb 28, 2022: Content expanded
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
