---
title: "Ignorer du code"
description: "Comment empêcher djLint de formater un bloc de code, et comment ignorer des règles du linter directement dans le code."
---

Le formateur et le linter ne touchent pas au code placé entre les commentaires `djlint:off` et `djlint:on`. Ce peuvent être des commentaires HTML :

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Ou des commentaires Django et Jinja :

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

Ou des blocs `{% comment %}` :

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Ou des commentaires de templates Go :

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

Ou des commentaires Handlebars :

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
