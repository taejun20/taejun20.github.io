---
layout: post
title: "Balanced Latin Square: Partial Counterbalancing? Complete Counterbalancing?"
---
<br>
Within-subject 디자인에서는 Between-subject 디자인과 달리 각 Subject가 모든 조건을 경험하게 되기 때문에 Order Effect가 발생한다. 세션이 진행될 수록 연습을 통해 전반적인 퍼포먼스가 점점 개선되는 경우 (Practice Effect), 피로가 누적되어 퍼포먼스에 영향을 주는 경우 (Fatigue Effect) 등. 이러한 Order Effect로 인해 특정 실험 Condition의 데이터가 받는 영향들을 서로 Balance하기 위해 각 피험자가 경험하는 실험 조건의 순서를 섞어준다. 이를 카운터 밸런싱이라 한다. 

### Complete Counterbalancing

**Complete Counterbalancing**은 n!개의 순서를 모두 포함시키는 것으로, n!명의 피험자가 필요하다. 실험 조건(Factor)이 3개라면 Complete Counterbalancing을 위해 최소 3! = 6명이 필요하다. 그래서 6명, 12명, ... 6의 배수의 사람을 구인해야 한다.

{% highlight markdown %}
    1st 2nd 3rd
p1:  A   B   C 
p2:  A   C   B
p3:  B   A   C
p4:  B   C   A
p5:  C   A   B
p6:  C   B   A
{% endhighlight %}
<p style='text-align:center'>Complete Counterbalancing with 3 Factor</p>

### Balanced Latin Square

**Latin Square**를 이용한 Counterbalancing는 특정 순서에 특정 Condition이 단 한번만 경험되도록 한다. (ex. 아래 4 * 4 Latin Square: 1st Session에서 조건 A는 딱 한 번) Latin Square의 문제는 (A->B)와 같은 순서가 고정되는 것이다. (B->A)와 같은 순서는 발생하지 않는다. 비대칭적인 순서 효과의 영향을 피할 수 없다.
{% highlight markdown %}
    1st 2nd 3rd 4th
p1:  A   B   C   D
p2:  B   C   D   A
p3:  C   D   A   B
p4:  D   A   B   C
{% endhighlight %}
<p style='text-align:center'> 4*4 Latin Square</p>

**Balanced Latin Square**는 이러한 문제를 해결해준다. 특정 조건의 순서는 동일한 횟수만큼 발생한다. (ex. 아래 4 * 4 Balanced Latin Square에서 A->B 순서, B->A 순서 모두 각각 한번씩 있다)
{% highlight markdown %}
    1st 2nd 3rd 4th
p1:  A   B   C   D
p2:  B   D   A   C
p3:  D   C   B   A
p4:  C   A   D   B
{% endhighlight %}
<p style='text-align:center'> 4*4 Balanced Latin Square</p>

### Partial Counterbalancing

Balanced Latin Square를 이용해 카운터 밸런싱을 했다고 하면 대체로 그 Validity가 인정된다. 그렇지만 Size 4 이상의 Balanced Latin Square는 여전히 **Complete Counterbalancing**이 아니고 **Partial Counterbalancing**이라는 점을 인지하고 있어야 한다. 실험 조건이 6개인 경우 현실적으로 720명의 피험자를 구인할 수 없기에 Balanced Latin Square를 이용한 **Partial Counterbalancing**을 통해 12명의 피험자만 구인할 수 있는 것이다.

## 참고
https://statpages.info/latinsq.html <br>
https://dictionary.apa.org/complete-counterbalancing<br>
http://people.uncw.edu/tothj/psy355/psy355-12-expts-within-subjects.pdf<br>
https://opentext.wsu.edu/carriecuttler/chapter/experimental-design/<br>
Williams, E. J. (1949): Experimental designs balanced for the estimation of residual effects of treatments. Australian Journal of Scientific Research, Ser. A 2, 149-168.<br>
## 변경 이력
* 2020년 5월 6일: 글 등록
* 2021년 8월 11일: 글 수정 (내용 보충)
