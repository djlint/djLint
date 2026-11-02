---
title: "Игнорирование кода"
description: "Как запретить djLint форматировать блок кода. Как отключать правила djLint прямо в коде."
sidebar:
  label: "Игнорирование кода"
---

Чтобы djLint пропускал код, оберните его в теги `djlint`:

Для обычного HTML:

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

или в виде комментария:

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

или в виде длинного комментария:

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

или в виде комментария в стиле golang:

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

или в виде комментария в стиле handlebars:

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Игнорирование правил

Можно игнорировать и отдельные правила линтера: для этого укажите имя правила в открывающем теге игнорируемого блока.

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
