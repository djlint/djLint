---
description: How to prevent djLint from formatting a block of code. How ignore djLint rules inline.
title: Ignoring Code
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, formatter usage, ignore code, ignore rules
date: Last Modified
---

# Ignoring Code

Code can be ignored by wrapping it in `djlint` tags:

{% raw %}

For plain old html -

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

or as a comment -

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

or as a long comment -

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

or as a javascript style comment -

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

or as a golang style comment -

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Ignoring Rules

Specific linter rules can also be ignored by adding the rule name into the ignored block opening tag.

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
