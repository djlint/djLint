---
description: Comment empêcher djLint de formater un bloc de code, et comment ignorer des règles du linter directement dans le code.
title: Ignorer du code
keywords: linter de templates, formateur de templates, djLint, HTML, templates, formateur, linter, utilisation du formateur, ignorer du code, ignorer des règles
date: Last Modified
---

# Ignorer du code

Pour ignorer du code, entourez-le de balises `djlint` :

{% raw %}

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

{% endraw %}

## Ignorer des règles

Vous pouvez aussi ignorer des règles précises du linter en ajoutant leur nom dans la balise d'ouverture du bloc ignoré.

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
