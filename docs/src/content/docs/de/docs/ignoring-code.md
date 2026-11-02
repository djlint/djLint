---
title: "Code ignorieren"
description: "So verhindern Sie, dass djLint einen Codeblock formatiert. So ignorieren Sie djLint-Regeln inline."
sidebar:
  label: "Code ignorieren"
---

Code lässt sich ignorieren, indem Sie ihn in `djlint`-Tags einschließen:

Für ganz normales HTML:

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

oder als Kommentar:

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

oder als langer Kommentar:

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

oder als Kommentar im Stil von Go:

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

oder als Kommentar im Stil von Handlebars:

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Regeln ignorieren

Sie können auch einzelne Linter-Regeln ignorieren, indem Sie den Namen der Regel in das öffnende Tag des ignorierten Blocks schreiben.

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
