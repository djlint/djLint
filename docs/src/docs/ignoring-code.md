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

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

or as a comment -

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

or as a long comment -

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

or as a javascript style comment -

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

or as a golang style comment -

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

{% endraw %}

## Ignoring Rules

Specific linter rules can also be ignored by adding the rule name into the ignored block opening tag.

{% raw %}

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

{% endraw %}
