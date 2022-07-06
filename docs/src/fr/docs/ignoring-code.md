---
description: Comment empêcher djLint de formater un bloc de code. Comment ignorer les règles de djLint en ligne.
title: Ignorer le code
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, formatter usage, ignorer le code, ignorer les règles
date: Last Modified
---

## Ignorer le code

Le code peut être ignoré en l'entourant de balises `djlint` :

{% raw %}

Pour le simple html -

```html
<!-- djlint:off -->
<mauvais html à ignorer> <!-- djlint:on --></bad>
```

ou comme un long commentaire -

```html
{# djlint:off #} <mauvais html à ignorer> {# djlint:on #}</bad>
```

ou comme un long commentaire -

```html
{% comment %} djlint:off {% endcomment %}
<mauvais html à ignorer> {% comment %} djlint:on {% endcomment %}</bad>
```

ou comme un commentaire de style javascript -

```html
{{ /* djlint:off */ }} <mauvais html à ignorer> {{ /* djlint:on */ }}</bad>
```

ou comme un commentaire de style golang -

```html
{{!-- djlint:off --}} <mauvais html à ignorer> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Ignorer les règles

Des règles spécifiques de linter peuvent également être ignorées en ajoutant le nom de la règle dans la balise d'ouverture du bloc ignoré.

{% raw %}

```html
{# djlint:off H025,H026 #}
<p>
  {# djlint:on #}

  <!-- djlint:off H025-->
</p>

<p>
  <!-- djlint:on -->

  {% comment %} djlint:off H025 {% endcomment %}
</p>

<p>{% comment %} djlint:on {% endcomment %} {{!-- djlint:off H025 --}}</p>

<p>{{!-- djlint:on --}} {{ /* djlint:off H025 */ }}</p>

<p>{{ /* djlint:on */ }}</p>
```

{% endraw %}
