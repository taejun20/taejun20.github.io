---
title: Balanced Latin Square: Partial Counterbalancing? Complete Counterbalancing?
date: 2020-05-06
tag: User Study
---

Within-subject 실험 디자인에서는 between-subject 디자인과 달리 각 Subject가 모든 조건을 경험하게 되기 때문에 order effect가 발생한다. 세션이 진행될 수록 연습을 통해 전반적인 퍼포먼스가 점점 개선되는 경우 (Practice Effect), 피로가 누적되어 퍼포먼스에 영향을 주는 경우 (Fatigue Effect) 등. 이러한 Order Effect를 제거할 수는 없지만, 특정 조건만 집중적으로 영향을 받지 않도록 각 피험자가 경험하는 조건의 순서를 분산시켜줄 수 있다. 이를 카운터밸런싱이라 한다. 카운터밸런싱을 통해 Order Effect는 모든 조건에 고르게 분산되어 조건 간 비교에서 상쇄된다.

# Complete Counterbalancing

Complete Counterbalancing은 n!개의 순서를 모두 포함시키는 것으로, n!명의 배수가 되는 피험자가 필요하다. 실험 조건(Factor)이 3개라면 Complete Counterbalancing을 위해 최소 3! = 6명이 필요하다. 그래서 6명, 12명, ... 6의 배수의 사람을 구인해야 한다.

```note
| Participant | 1st | 2nd | 3rd |
|---|---|---|---|
| p1 | A | B | C |
| p2 | A | C | B |
| p3 | B | A | C |
| p4 | B | C | A |
| p5 | C | A | B |
| p6 | C | B | A |

Complete Counterbalancing with 3 Conditions
```

# Latin Square

Latin Square를 이용한 Counterbalancing은 특정 순서에 특정 Condition이 단 한 번만 경험되도록 한다 (ex. 아래 4×4 Latin Square: 1st Session에서 조건 A는 딱 한 번). Latin Square의 한계는 (A→B)와 같은 일련의 순서가 고정되는 것이다. (B→A)와 같은 순서는 발생하지 않는다. 이처럼 앞 조건이 뒤 조건에 미치는 영향, 즉 Carryover Effect가 방향에 따라 비대칭적으로 발생할 경우 이를 통제하지 못한다는 한계가 있다.

```note
| Participant | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| p1 | A | B | C | D |
| p2 | B | C | D | A |
| p3 | C | D | A | B |
| p4 | D | A | B | C |

4×4 Latin Square
```

# Balanced Latin Square

Balanced Latin Square는 이러한 문제를 해결해준다. 특정 조건의 순서는 동일한 횟수만큼 발생한다 (ex. 아래 4×4 Balanced Latin Square에서 A→B 순서, B→A 순서 모두 각각 한번씩 있다) [Balanced Latin Square 생성기](https://damienmasson.com/tools/latin_square/). 단, 조건 수 n이 홀수인 경우 하나의 n×n 표로는 완전한 균형을 만들 수 없어 2n개의 행(즉, 2n명의 피험자) 이 필요하다.

```note
| Participant | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| p1 | A | B | C | D |
| p2 | B | D | A | C |
| p3 | D | C | B | A |
| p4 | C | A | D | B |

4×4 Balanced Latin Square
```

# Partial Counterbalancing

Balanced Latin Square를 이용해 카운터 밸런싱을 했다고 하면 대체로 그 Validity가 인정된다. 그렇지만 Size 4 이상의 Balanced Latin Square는 여전히 Complete Counterbalancing이 아니고 Partial Counterbalancing이라는 점을 인지하고 있어야 한다. 실험 조건이 6개인 경우 현실적으로 720명의 피험자를 구인할 수 없기에 Balanced Latin Square를 이용한 Partial Counterbalancing을 통해 12명의 피험자만 구인할 수 있는 것이다.

정리하면, 조건이 4개 이상이면 현실적으로 Complete Counterbalancing은 불가능하므로 Balanced Latin Square를 이용한 Partial Counterbalancing이 표준적인 선택이다. HCI 및 사용자 연구 분야에서는 Balanced Latin Square만으로도 충분한 Validity가 인정되는 것이 일반적이다.

# 참고

- [Latin Square Generator – statpages.info](https://statpages.info/latinsq.html)
- [Complete Counterbalancing – APA Dictionary](https://dictionary.apa.org/complete-counterbalancing)
- [Within-Subjects Experiments – UNCW](http://people.uncw.edu/tothj/psy355/psy355-12-expts-within-subjects.pdf)
- [Experimental Design – WSU OpenText](https://opentext.wsu.edu/carriecuttler/chapter/experimental-design/)
- Williams, E. J. (1949): Experimental designs balanced for the estimation of residual effects of treatments. *Australian Journal of Scientific Research*, Ser. A 2, 149–168.

# 변경 이력
- 2020년 5월 6일: 글 등록
- 2021년 8월 11일: 글 수정 (내용 보충)
- 2021년 12월 1일: Velog로 이전
- 2026년 2월 26일: Notion으로 이전
- 2026년 5월 28일: 개인 웹사이트로 이전
