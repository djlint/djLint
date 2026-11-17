---
title: "Code ignorieren"
description: "Wie Sie verhindern, dass djLint einen Codeblock formatiert, und wie Sie Linter-Regeln inline ignorieren."
---

Code zwischen den Kommentaren `djlint:off` und `djlint:on` lassen Formatter und Linter in Ruhe. Das können HTML-Kommentare sein:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Oder Kommentare von Django und Jinja:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

Oder `{% comment %}`-Blöcke:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Oder Kommentare in Go-Templates:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

Oder Kommentare in Handlebars:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Regeln ignorieren

Sie können auch einzelne Linter-Regeln ignorieren, indem Sie den Namen der Regel in das öffnende Tag des ignorierten Blocks schreiben.

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
