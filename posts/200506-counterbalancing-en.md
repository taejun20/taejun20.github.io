---
title: Balanced Latin Square: Partial Counterbalancing? Complete Counterbalancing?
date: 2020-05-06
tag: User Study
---

In a within-subject design, unlike between-subject, each participant experiences all conditions, which introduces order effects. Performance can generally improve over sessions due to practice (Practice Effect), or degrade due to fatigue (Fatigue Effect). These order effects cannot be eliminated, but counterbalancing distributes them evenly across conditions so no single condition is disproportionately affected. Through counterbalancing, order effects are spread evenly and cancel out when comparing conditions.

# Complete Counterbalancing

Complete counterbalancing includes all n! possible orderings, requiring a sample size that is a multiple of n!. With 3 conditions, you need at least 3! = 6 participants, so you'd recruit 6, 12, 18, ... people.

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

Latin Square counterbalancing ensures each condition appears exactly once in each order (e.g., in the 4x4 Latin Square below, condition A appears exactly once in the 1st session). The limitation is that certain sequences are fixed: (A→B) always appears, but (B→A) never does. This means carryover effects, where one condition influences the next, can be asymmetric and uncontrolled.

```note
| Participant | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| p1 | A | B | C | D |
| p2 | B | C | D | A |
| p3 | C | D | A | B |
| p4 | D | A | B | C |

4x4 Latin Square
```

# Balanced Latin Square

Balanced Latin Square solves this problem. Each sequential pair of conditions appears the same number of times in both directions (e.g., in the 4x4 Balanced Latin Square below, A→B and B→A each appear exactly once). [Balanced Latin Square generator](https://damienmasson.com/tools/latin_square/). Note: when n is odd, a single n×n table cannot achieve full balance, so 2n rows (i.e., 2n participants) are needed.

```note
| Participant | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| p1 | A | B | C | D |
| p2 | B | D | A | C |
| p3 | D | C | B | A |
| p4 | C | A | D | B |

4x4 Balanced Latin Square
```

# Partial Counterbalancing

Using a Balanced Latin Square is generally accepted as valid counterbalancing. However, it's good to be aware that for n >= 4, a Balanced Latin Square is still Partial Counterbalancing, not Complete. With 6 conditions, recruiting 720 participants for complete counterbalancing is not realistic. A Balanced Latin Square brings that down to 12 participants.

In short: for 4 or more conditions, complete counterbalancing is practically impossible, and Balanced Latin Square with partial counterbalancing is the standard approach. In HCI and user research, a Balanced Latin Square is generally considered sufficient for validity.

# References

- [Latin Square Generator – statpages.info](https://statpages.info/latinsq.html)
- [Complete Counterbalancing – APA Dictionary](https://dictionary.apa.org/complete-counterbalancing)
- [Within-Subjects Experiments – UNCW](http://people.uncw.edu/tothj/psy355/psy355-12-expts-within-subjects.pdf)
- [Experimental Design – WSU OpenText](https://opentext.wsu.edu/carriecuttler/chapter/experimental-design/)
- Williams, E. J. (1949): Experimental designs balanced for the estimation of residual effects of treatments. *Australian Journal of Scientific Research*, Ser. A 2, 149–168.

# Changelog
- May 6, 2020: Post published
- Aug 11, 2021: Content expanded
- Dec 1, 2021: Migrated to Velog
- Feb 26, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
