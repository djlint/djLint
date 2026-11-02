---
description: Как запретить djLint форматировать блок кода. Как отключать правила djLint прямо в коде.
title: Игнорирование кода
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование форматера, игнорирование кода, игнорирование правил
date: Last Modified
---

# Игнорирование кода

Чтобы djLint пропускал код, оберните его в теги `djlint`:

{% raw %}

Для обычного HTML:

<!-- oxfmt-ignore -->

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

или в виде комментария:

<!-- oxfmt-ignore -->

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

или в виде длинного комментария:

<!-- oxfmt-ignore -->

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

или в виде комментария в стиле golang:

<!-- oxfmt-ignore -->

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

или в виде комментария в стиле handlebars:

<!-- oxfmt-ignore -->

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Игнорирование правил

Можно игнорировать и отдельные правила линтера: для этого укажите имя правила в открывающем теге игнорируемого блока.

{% raw %}

<!-- oxfmt-ignore -->

```html
{# djlint:off H025,H026 #}
<p>
  {# djlint:on #}

  <!-- djlint:off H025-->
</p>

<p>
  <!-- djlint:on -->

  {% comment %} djlint:off H025 {% endcomment %}
</p>

<p>{% comment %} djlint:on {% endcomment %} {{!-- djlint:off H025 --}}</p>

<p>{{!-- djlint:on --}} {{ /* djlint:off H025 */ }}</p>

<p>{{ /* djlint:on */ }}</p>
```

{% endraw %}
