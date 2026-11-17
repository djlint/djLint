---
title: "Ignorowanie kodu"
description: "Jak sprawić, by djLint nie formatował bloku kodu, i jak ignorować reguły lintera bezpośrednio w kodzie."
---

Kod między komentarzami `djlint:off` i `djlint:on` jest pomijany przez formater i linter. Mogą to być komentarze HTML:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Albo komentarze Django i Jinja:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

Albo bloki `{% comment %}`:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Albo komentarze szablonów Go:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

Albo komentarze Handlebars:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Ignorowanie reguł

Można też ignorować konkretne reguły lintera, dopisując nazwę reguły do tagu otwierającego ignorowany blok.

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
