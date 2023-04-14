---
layout: post
title: "Interaction Effects in ANOVA"
---
<br>
ANOVA 분석에서는 각 factor의 main effect와 함께 factor 사이의 interaction effect도 함께 보고된다. **한 factor의 main effect가 다른 factor의 level에 dependent**하게 되면, 두 factor는 interaction effect가 있는 것이다.

### 예시

친구가 같이 영화를 보러가자고 했다. 대답은 "누가 같이 오는지, 어떤 영화를 보는지에 따라 참석 여부를 결정할게."
{% highlight markdown %}
Independent Variable: 영화의 종류, 같이 오는 친구의 종류
Dependent Variable: 참석 여부
{% endhighlight %}
* **같이 오는 친구** 중 내가 피하고 싶은 사람이 있다면 **영화의 종류**가 무엇이든 참석하지 않는다고 하자. 그렇지만 **같이 오는 친구** 중에 내가 피하고 싶은 사람이 없는 경우에서 **영화의 종류**가 액션 영화면 참석하고 로맨스 영화면 참석하지 않는다고 하자.
* **영화의 종류**라는 factor의 main effect는 **같이 오는 친구**라는 factor가 특정 level일 때에만 발생하는, 이에 dependent한 효과이다. 이런 경우 두 factor는 서로 interaction effect를 가질 수 있다.

### Elaboration

특정 factor의 main effect를 통해 내 주장을 뒷받침 하고 싶다. ANOVA 분석 결과  factor의 main effect가 확인되었다. 그런데 다른 factor와의 interaction effect 또한 확인되었다면? 이는 달갑지 않은 소식이 될 것이다. Interaction effect가 있다는 말은 factor의 main effect가 다른 factor의 level에 따라 있기도 하고 없기도 하다는 것이니 **"이 factor는 main effect가 있다"라고 온전히 주장할 수가 없게 된다**는 것이다. 나아가 Independent Variable이 사실은 "Independent"하지 않았다는 것을 보여주므로 잘못된 실험 디자인으로 지적받을 수도 있다. 사후 분석을 통해 두 Factor가 함께 조합된 조건들에 대한 pairwise comparison을 보여주며 결과를 설명하는 수 밖에 없다.

### Elaboration with Example

가상의 예시를 하나 들어보자. 손목의 두께와 진동 모터의 종류가 촉각 패턴 인지율에 미치는 영향을 확인하는 실험을 진행했다고 하자. 나는 **"진동 모터의 종류가 촉각 패턴 인지율에 통계적으로 유의미한 영향을 미친다. 모터 a가 모터 b보다 효과적이다."** 라는 주장을 내 논문에 싣고 싶은 상황이다.
{% highlight markdown %}
* Independent Variable: 손목의 두께 (10, 12, 14), 진동 모터의 종류 (모터a, 모터b)
* Dependent Variable: 촉각 패턴 인지율 (%)
{% endhighlight %}
실험을 끝내고 ANOVA 분석을 해보니 진동 모터의 종류라는 factor의 main effect가 확인되었다. 그런데 진동 모터의 종류 * 손목의 두께의 Interaction effect도 함께 발견이 된 것이다. 이런 경우 **"진동 모터의 종류가 촉각 패턴 인지율에 유의미한 영향을 미친다"** 라고 주장하면 **안된다.** 이런 상황에서는 각 factor의 main effect와 interaction effect를 모두 같이 보고한 다음 사후 분석 결과를 보여주며 **"손목 두께가 10인 경우에만 모터 a가 모터 b보다 촉각 패턴 인지에 효과적이며, 다른 손목 두께에서는 그렇지 않다"** 라고 주장하는 것이 바람직하다.

## 참고
https://opentext.wsu.edu/carriecuttler/chapter/9-2-main-effects-and-interactions/<br>
https://statisticsbyjim.com/regression/interaction-effects/<br>
## 변경 이력
* 2020년 9월 3일: 글 등록
* 2021년 8월 11일: 글 수정 (내용 보충)
