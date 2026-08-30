---
description: Как запретить djLint форматировать блок кода. Как игнорировать правила djLint в строке.
title: Игнорирование кода
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, Использование форматера
date: Last Modified
---

# Игнорирование кода

Код можно игнорировать, обернув его в теги `djlint`:

{% raw %}

Для простого старого html -

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <плохой html, который следует игнорировать>
<!-- djlint:on -->
```

или как комментарий -

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <плохой html, который следует игнорировать>
{# djlint:on #}
```

или в виде длинного комментария -

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <плохой html, который следует игнорировать>
{% comment %} djlint:on {% endcomment %}
```

или как комментарий в стиле golang -

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <плохой html, который следует игнорировать>
{{ /* djlint:on */ }}
```

или как комментарий в стиле handlebars -

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <плохой html, который следует игнорировать>
{{!-- djlint:on --}}
```

{% endraw %}

## Игнорирование правил

Определенные правила linter можно игнорировать, добавив имя правила в открывающий тег игнорируемого блока.

{% raw %}

<!-- prettier-ignore -->
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
