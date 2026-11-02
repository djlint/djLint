---
title: "Ignorowanie kodu"
description: "Jak sprawić, by djLint nie formatował bloku kodu. Jak ignorować reguły djLint bezpośrednio w kodzie."
sidebar:
  label: "Ignorowanie kodu"
---

Kod można zignorować, otaczając go tagami `djlint`:

W zwykłym HTML-u:

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

lub w komentarzu:

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

lub w długim komentarzu:

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

lub w komentarzu w stylu golang:

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

lub w komentarzu w stylu handlebars:

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Ignorowanie reguł

Można też ignorować konkretne reguły lintera, dopisując nazwę reguły do tagu otwierającego ignorowany blok.

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
