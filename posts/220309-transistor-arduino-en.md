---
title: Transistor (2): Transistor with Arduino
date: 2022-03-09
tag: Electronics
---

In the [previous post](/posts?post=191112-transistor-basics), I went over the role and operating principles of transistors. This post covers when and why you need a transistor when building circuits with a microcontroller like Arduino.

# Why Use a Transistor with a Microcontroller

The current limit on Arduino digital and analog I/O pins is 40 mA. Exceeding this can damage the pin. A small LED (e.g., [MCL053MD](https://www.farnell.com/datasheets/2861526.pdf) with a recommended operating current of 20 mA) can be driven directly from an Arduino pin. But higher-power motors (e.g., [12G88 Athlonix DC Motor](https://www.digikey.be/htmldatasheets/production/1763365/0/0/1/12g88-spec-sheet.html): 9V, max continuous current 370 mA; [Precision Microdrive vibration motor](https://catalogue.precisionmicrodrives.com/product/datasheet/310-113-10mm-vibration-motor-3mm-type-datasheet.pdf): 3V, rated current 60 mA) would draw far more than 40 mA if connected directly, damaging the pin.

That's where a motor driver or, more simply, a transistor comes in. The small current from the Arduino pin acts as a control signal, while an external power supply delivers sufficient and stable voltage/current to the motor. The circuit below shows an example of connecting an Arduino pin to the Base of a transistor.

![Digital pin connected to a transistor. The motor is powered from the 5V pin (VCC and GND pin current limit: 200 mA)|60%](img/posts/220309-transistor-arduino/circuit.png)

Note the resistor (R1) between the Arduino pin and the Base. This limits the current flowing into the Base. The Arduino outputs 5V, and connecting directly to the Base without a resistor would let too much current flow, potentially damaging the transistor or the pin. The value of R1 is chosen to push the transistor into the Saturation Region (fully on). For example, with 5V and a 1kΩ resistor, about 5 mA flows into the Base; with β = 100, that controls up to 500 mA at the Collector.

# References

- [Arduino Pin Current Limitations](https://playground.arduino.cc/Main/ArduinoPinCurrentLimitations/)
- [Transistors – Adafruit Arduino Lesson 13](https://learn.adafruit.com/adafruit-arduino-lesson-13-dc-motors/transistors)
- [Transistor as a Switch – YouTube](https://www.youtube.com/watch?v=T1eMKml3iE0&t=235s)
- [Transistor Summary – Naver Blog](https://m.blog.naver.com/okseods1/220949581522)

# Changelog
- Mar 9, 2022: Post published
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
