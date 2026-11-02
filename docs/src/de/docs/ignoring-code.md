---
description: Wie Sie verhindern, dass djLint einen Codeblock formatiert, und wie Sie Linter-Regeln inline ignorieren.
title: Code ignorieren
keywords: Template-Linter, Template-Formatter, djLint, HTML, Templates, Formatter, Linter, Formatter verwenden, Code ignorieren, Regeln ignorieren
date: Last Modified
---

# Code ignorieren

Code lässt sich ignorieren, indem Sie ihn in `djlint`-Tags einschließen:

{% raw %}

Für ganz normales HTML:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

oder als Kommentar:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

oder als langer Kommentar:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

oder als Kommentar im Stil von Go:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

oder als Kommentar im Stil von Handlebars:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

{% endraw %}

## Regeln ignorieren

Sie können auch einzelne Linter-Regeln ignorieren, indem Sie den Namen der Regel in das öffnende Tag des ignorierten Blocks schreiben.

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
