---
description: Jak sprawić, by djLint nie formatował bloku kodu. Jak ignorować reguły djLint bezpośrednio w kodzie.
title: Ignorowanie kodu
keywords: linter szablonów, formater szablonów, djLint, HTML, szablony, formater, linter, używanie formatera, ignorowanie kodu, ignorowanie reguł
date: Last Modified
---

# Ignorowanie kodu

Kod można zignorować, otaczając go tagami `djlint`:

{% raw %}

W zwykłym HTML-u:

<!-- oxfmt-ignore -->

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

lub w komentarzu:

<!-- oxfmt-ignore -->

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

lub w długim komentarzu:

<!-- oxfmt-ignore -->

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

lub w komentarzu w stylu golang:

<!-- oxfmt-ignore -->

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

lub w komentarzu w stylu handlebars:

<!-- oxfmt-ignore -->

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Ignorowanie reguł

Można też ignorować konkretne reguły lintera, dopisując nazwę reguły do tagu otwierającego ignorowany blok.

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
