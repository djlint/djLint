---
title: "Ignorer du code"
description: "Comment empêcher djLint de formater un bloc de code. Comment ignorer des règles de djLint directement dans le code."
sidebar:
  label: "Ignorer du code"
---

Pour ignorer du code, entourez-le de balises `djlint` :

En HTML classique :

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

ou sous forme de commentaire :

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

ou sous forme de commentaire long :

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

ou sous forme de commentaire de style golang :

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

ou sous forme de commentaire de style handlebars :

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Ignorer des règles

Vous pouvez aussi ignorer des règles précises du linter en ajoutant leur nom dans la balise d'ouverture du bloc ignoré.

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
