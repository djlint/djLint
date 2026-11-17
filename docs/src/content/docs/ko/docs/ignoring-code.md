---
title: "코드 무시하기"
description: "djLint가 코드 블록을 포맷하지 않게 하는 방법과 린터 규칙을 인라인으로 무시하는 방법입니다."
---

`djlint:off`와 `djlint:on` 주석 사이의 코드는 포맷터와 린터가 건드리지 않습니다. HTML 주석을 쓸 수 있습니다.

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Django와 Jinja 주석도 쓸 수 있습니다.

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

`{% comment %}` 블록도 쓸 수 있습니다.

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Go 템플릿 주석도 쓸 수 있습니다.

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

Handlebars 주석도 쓸 수 있습니다.

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## 규칙 무시하기

무시 블록의 여는 태그에 규칙 이름을 넣으면 특정 린터 규칙만 무시할 수도 있습니다.

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
