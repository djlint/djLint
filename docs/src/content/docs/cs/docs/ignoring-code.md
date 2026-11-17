---
title: "Ignorování kódu"
description: "Jak zabránit djLint ve formátování bloku kódu a jak ignorovat pravidla linteru přímo v kódu."
---

Kód mezi komentáři `djlint:off` a `djlint:on` nechá formátovač i linter beze změny. Mohou to být komentáře HTML:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Nebo komentáře Django a Jinja:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

Nebo bloky `{% comment %}`:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Nebo komentáře šablon Go:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

Nebo komentáře Handlebars:

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
