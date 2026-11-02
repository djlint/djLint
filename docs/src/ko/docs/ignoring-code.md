---
description: djLint가 코드 블록을 포맷하지 않게 하는 방법과 린터 규칙을 인라인으로 무시하는 방법입니다.
title: 코드 무시하기
keywords: 템플릿 린터, 템플릿 포맷터, djLint, HTML, 템플릿, 포맷터, 린터, 포맷터 사용법, 코드 무시, 규칙 무시
date: Last Modified
---

# 코드 무시하기

코드를 `djlint` 태그로 감싸면 무시할 수 있습니다.

{% raw %}

일반 HTML에서는 다음과 같이 씁니다.

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

주석으로 쓸 수도 있습니다.

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

긴 주석으로 쓸 수도 있습니다.

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

golang 스타일 주석으로 쓸 수도 있습니다.

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

handlebars 스타일 주석으로 쓸 수도 있습니다.

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

{% endraw %}

## 규칙 무시하기

무시 블록의 여는 태그에 규칙 이름을 넣으면 특정 린터 규칙만 무시할 수도 있습니다.

{% raw %}

<!-- oxfmt-ignore -->
```html
{# djlint:off H025,H026 #}
<p>
{# djlint:on #}

<!-- djlint:off H025-->
<p>
<!-- djlint:on -->

{% comment %} djlint:off H025 {% endcomment %}
<p>
{% comment %} djlint:on {% endcomment %}

{{!-- djlint:off H025 --}}
<p>
{{!-- djlint:on --}}

{{ /* djlint:off H025 */ }}
<p>
{{ /* djlint:on */ }}
```

{% endraw %}
