---
description: Jak zabránit djLint ve formátování bloku kódu. Jak ignorovat pravidla djLint přímo v kódu.
title: Ignorování kódu
keywords: linter šablon, formátovač šablon, djLint, HTML, šablony, formátovač, linter, použití formátovače, ignorování kódu, ignorování pravidel
date: Last Modified
---

# Ignorování kódu

Kód lze ignorovat tak, že ho obalíte značkami `djlint`:

{% raw %}

Pro obyčejné HTML:

<!-- oxfmt-ignore -->

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

nebo jako komentář:

<!-- oxfmt-ignore -->

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

nebo jako dlouhý komentář:

<!-- oxfmt-ignore -->

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

nebo jako komentář ve stylu golang:

<!-- oxfmt-ignore -->

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

nebo jako komentář ve stylu handlebars:

<!-- oxfmt-ignore -->

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Ignorování pravidel

Konkrétní pravidla linteru lze ignorovat také tak, že název pravidla přidáte do otevírací značky ignorovaného bloku.

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
