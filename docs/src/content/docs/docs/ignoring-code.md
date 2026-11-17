---
title: "Ignoring code"
description: "How to keep djLint from formatting a block of code, and how to ignore linter rules inline."
---

Code between `djlint:off` and `djlint:on` comments is left alone by the formatter and the linter. The comments can be HTML ones:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Or Django and Jinja comments:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

Or `{% comment %}` blocks:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Or Go template comments:

<!-- oxfmt-ignore -->
```html
{{/* djlint:off */}}
   <bad html to ignore>
{{/* djlint:on */}}
```

Or Handlebars comments:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Ignoring rules

Specific linter rules can also be ignored by adding the rule name into the ignored block opening tag.

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

{{/* djlint:off H025 */}}
<p>
{{/* djlint:on */}}
```
