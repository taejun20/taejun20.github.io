---
title: Interaction Effects in ANOVA
date: 2020-09-03
tag: Statistics
---

In ANOVA, both the main effect of each factor and the interaction effects between factors are reported. When the main effect of one factor depends on the level of another factor, the two factors are said to have an interaction effect.

# Example

A friend asks if I want to go see a movie. My answer: "It depends on who's coming and what movie it is."

```note
Independent Variables: type of movie, who is coming  
Dependent Variable: whether I attend
```

- If someone I don't want to watch a movie with is coming, I won't go regardless of the movie. But if no one I want to avoid is coming, I'll go for an action movie and skip a romance.
- The main effect of movie type only occurs when the people factor is at a certain level. In this case, the two factors have an interaction effect.

# Elaboration

Say I want to use the main effect of a factor to support my claim. ANOVA confirms a significant main effect. But what if an interaction effect with another factor is also found? That's an unwelcome result. An interaction effect means the main effect of that factor exists for some levels of the other factor but not others, so you can no longer simply claim "this factor has a main effect." It might also suggest that the independent variables you defined weren't truly independent, which could raise questions about the experimental design. The only option is to show pairwise comparisons across combinations of both factors in post-hoc analysis and explain the results accordingly.

## Elaboration with Example

A hypothetical example. Suppose I ran an experiment to examine how wrist thickness and vibration motor type affect tactile pattern recognition accuracy. I want to claim: "The type of vibration motor has a statistically significant effect on tactile recognition accuracy. Motor A is more effective than Motor B."

```note
Independent Variables: wrist thickness (10, 12, 14), vibration motor type (Motor A, Motor B)  
Dependent Variable: tactile pattern recognition accuracy (%)
```

After running ANOVA, the main effect of motor type is confirmed. But an interaction effect of (motor type x wrist thickness) is also found. In this case, I cannot simply claim "motor type significantly affects tactile recognition." I need to report both the main effects and the interaction effect, then present post-hoc results: "Motor A is more effective than Motor B only when wrist thickness is 10. For other wrist thicknesses, the difference is not significant."

# References

- [Main Effects and Interactions – WSU OpenText](https://opentext.wsu.edu/carriecuttler/chapter/9-2-main-effects-and-interactions/)
- [Interaction Effects – Statistics By Jim](https://statisticsbyjim.com/regression/interaction-effects/)

# Changelog
- Sep 3, 2020: Post published
- Aug 11, 2021: Content expanded
- Dec 1, 2021: Migrated to Velog
- Feb 28, 2026: Migrated to Notion
- May 28, 2026: Migrated to personal website
