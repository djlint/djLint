---
description: Come impedire a djLint di formattare un blocco di codice e come ignorare le regole del linter inline.
title: Ignorare il codice
keywords: linter per template, formattatore per template, djLint, HTML, template, formattatore, linter, uso del formattatore, ignorare il codice, ignorare le regole
date: Last Modified
---

# Ignorare il codice

Il codice può essere ignorato racchiudendolo tra tag `djlint`:

{% raw %}

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

{% endraw %}

## Ignorare le regole

Si possono ignorare anche specifiche regole del linter aggiungendo il nome della regola al tag di apertura del blocco ignorato.

{% raw %}

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

{% endraw %}
