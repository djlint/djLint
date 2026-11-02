---
title: "Ignorare il codice"
description: "Come impedire a djLint di formattare un blocco di codice. Come ignorare le regole di djLint inline."
sidebar:
  label: "Ignorare il codice"
---

Il codice può essere ignorato racchiudendolo tra tag `djlint`:

Per il semplice HTML:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

oppure come commento:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

oppure come commento lungo:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

oppure come commento in stile golang:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

oppure come commento in stile handlebars:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Ignorare le regole

Si possono ignorare anche specifiche regole del linter aggiungendo il nome della regola al tag di apertura del blocco ignorato.

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
