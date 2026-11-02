---
description: Como impedir que o djLint formate um bloco de código. Como ignorar regras do djLint diretamente no código.
title: Ignorando código
keywords: linter de templates, formatador de templates, djLint, HTML, templates, formatador, linter, uso do formatador, ignorar código, ignorar regras
date: Last Modified
---

# Ignorando código

É possível ignorar código envolvendo-o em tags `djlint`:

{% raw %}

Em HTML puro -

<!-- oxfmt-ignore -->

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

ou como comentário -

<!-- oxfmt-ignore -->

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

ou como comentário longo -

<!-- oxfmt-ignore -->

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

ou como comentário no estilo golang -

<!-- oxfmt-ignore -->

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

ou como comentário no estilo handlebars -

<!-- oxfmt-ignore -->

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Ignorando regras

Regras específicas do linter também podem ser ignoradas adicionando o nome da regra à tag de abertura do bloco ignorado.

{% raw %}

<!-- oxfmt-ignore -->

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
