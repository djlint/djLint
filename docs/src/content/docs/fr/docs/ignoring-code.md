---
title: "Ignorer le code"
description: "Comment empêcher djLint de formater un bloc de code. Comment ignorer les règles de djLint en ligne."
sidebar:
  label: "Ignorer le code"
---

Le code peut être ignoré en l'entourant de balises `djlint` :

Pour le simple html -

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <mauvais html à ignorer>
<!-- djlint:on -->
```

ou comme un commentaire -

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <mauvais html à ignorer>
{# djlint:on #}
```

ou comme un long commentaire -

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <mauvais html à ignorer>
{% comment %} djlint:on {% endcomment %}
```

ou comme un commentaire de style golang -

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <mauvais html à ignorer>
{{ /* djlint:on */ }}
```

ou comme un commentaire de style handlebars -

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <mauvais html à ignorer>
{{!-- djlint:on --}}
```

## Ignorer les règles

Des règles spécifiques de linter peuvent également être ignorées en ajoutant le nom de la règle dans la balise d'ouverture du bloc ignoré.

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
