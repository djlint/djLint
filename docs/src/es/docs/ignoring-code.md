---
description: Cómo evitar que djLint formatee un bloque de código. Cómo ignorar reglas de djLint en línea.
title: Ignorar código
keywords: linter de plantillas, formateador de plantillas, djLint, HTML, plantillas, formateador, linter, uso del formateador, ignorar código, ignorar reglas
date: Last Modified
---

# Ignorar código

Para que se ignore un fragmento de código, enciérralo entre etiquetas `djlint`:

{% raw %}

Para HTML de toda la vida:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

o como comentario:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

o como comentario largo:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

o como comentario al estilo de golang:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

o como comentario al estilo de handlebars:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

{% endraw %}

## Ignorar reglas

También se pueden ignorar reglas concretas del linter añadiendo el nombre de la regla a la etiqueta de apertura del bloque ignorado.

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
