---
description: Как запретить djLint форматировать блок кода. Как игнорировать правила djLint в строке.
title: Игнорирование кодекса
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, Использование форматера
date: Last Modified
---

## Игнорирование кодекса

Код можно игнорировать, обернув его в теги `djlint`:

{% raw %}

Для простого старого html -

```html
<!-- djlint:off -->
<плохой html, который следует игнорировать> <!-- djlint:on --></bad>
```

или как комментарий -

```html
{# djlint:off #} <плохой html, который следует игнорировать> {# djlint:on #}</bad>
```

или в виде длинного комментария

```html
{% comment %} djlint:off {% endcomment %}
<плохой html, который следует игнорировать> {% comment %} djlint:on {% endcomment %}</bad>
```

или как комментарий в стиле javascript -

```html
{{ /* djlint:off */ }} <плохой html, который следует игнорировать> {{ /* djlint:on */ }}</bad>
```

или как комментарий в стиле golang -

```html
{{!-- djlint:off --}} <плохой html, который следует игнорировать> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Игнорирование правил

Определенные правила linter можно игнорировать, добавив имя правила в открывающий тег игнорируемого блока.

{% raw %}
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
