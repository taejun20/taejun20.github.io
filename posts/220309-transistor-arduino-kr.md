---
title: Transistor (2): Transistor with Arduino
date: 2022-03-09
tag: Electronics
---

[지난 포스트](/posts?post=191112-transistor-basics)에서 Transistor의 역할, 원리 등에 대해 알아보았다. 이어지는 본 글에서는 아두이노와 같은 Microcontroller 회로를 구성할 때 트랜지스터가 필요한 상황이 언제인지에 대해 정리한다.

# Microcontroller에서 트랜지스터를 사용하는 이유

Arduino I/O Digital Pin 혹은 Analogue Pin의 Current Limit는 40 mA 이다. 40 mA 보다 더 큰 전류가 흐르게 되면 Pin에 손상이 갈 수 있다. 작은 LED (e.g., [MCL053MD](https://www.farnell.com/datasheets/2861526.pdf) — Recommended Operating Current 20 mA)의 경우에는 Arduino Pin Output을 이용해 직접 드라이브할 수 있다. 하지만 더 큰 전력을 소모하는 모터의 경우 (e.g., [12G88 Athlonix DC Motor](https://www.digikey.be/htmldatasheets/production/1763365/0/0/1/12g88-spec-sheet.html): 9V 구동 & Max Continuous Current 370 mA, [Precision Microdrive 진동 모터](https://catalogue.precisionmicrodrives.com/product/datasheet/310-113-10mm-vibration-motor-3mm-type-datasheet.pdf): 3V 구동 & Rated Operating Current: 60 mA) 아두이노 Pin을 모터에 직접 연결하면 큰 전류가 흘러서 Pin에 손상이 갈 수 있다.

따라서 모터 드라이버 혹은 간단하게는 트랜지스터를 이용하는 것이다. Arduino Pin Output을 통해 전달할 수 있는 작은 전류를 Control Signal로 사용하고, 실제 모터에는 외부 전원을 이용해 충분하고 안정적인 전압/전류를 공급해주는 것이다. 아래 회로도는 Arduino Pin을 트랜지스터의 Base 단과 연결하여 사용하는 예시를 보여준다.

![Digital pin을 트랜지스터와 연결. 실제 모터의 전압은 5V pin에서 공급 (VCC pin, GND pin의 Current Limit은 200 mA)|60%](img/posts/220309-transistor-arduino/circuit.jpg)

회로도에서 Arduino Pin과 Base 사이에 저항(R1)이 연결되어 있다. 이는 Base에 흐르는 전류를 제한하기 위함이다. Arduino Pin은 5V를 출력하는데, 저항 없이 Base에 직접 연결하면 과전류가 흘러 트랜지스터나 Arduino Pin이 손상될 수 있다. R1의 값은 트랜지스터를 Saturation Region(완전히 켜진 상태)으로 만들기에 충분한 전류가 흐르도록 계산한다. 예를 들어 5V에서 1kΩ 저항을 사용하면 약 5mA가 흐르고, β = 100인 트랜지스터라면 I_C = 500mA까지 제어할 수 있다.



# 참고

- [Arduino Pin Current Limitations](https://playground.arduino.cc/Main/ArduinoPinCurrentLimitations/)
- [Transistors – Adafruit Arduino Lesson 13](https://learn.adafruit.com/adafruit-arduino-lesson-13-dc-motors/transistors)
- [Transistor as a Switch – YouTube](https://www.youtube.com/watch?v=T1eMKml3iE0&t=235s)
- [트랜지스터 정리 – Naver Blog](https://m.blog.naver.com/okseods1/220949581522)


# 변경 이력
- 2022년 3월 9일: 글 등록
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
