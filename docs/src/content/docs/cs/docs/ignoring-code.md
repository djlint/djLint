---
title: "Ignorování kódu"
description: "Jak zabránit djLint ve formátování bloku kódu. Jak ignorovat pravidla djLint přímo v kódu."
sidebar:
  label: "Ignorování kódu"
---

Kód lze ignorovat tak, že ho obalíte značkami `djlint`:

Pro obyčejné HTML:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

nebo jako komentář:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

nebo jako dlouhý komentář:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

nebo jako komentář ve stylu golang:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

nebo jako komentář ve stylu handlebars:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Ignorování pravidel

Konkrétní pravidla linteru lze ignorovat také tak, že název pravidla přidáte do otevírací značky ignorovaného bloku.

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
