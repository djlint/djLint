---
title: "Ignorando código"
description: "Como impedir que o djLint formate um bloco de código e como ignorar regras do linter diretamente no código."
---

O código entre os comentários `djlint:off` e `djlint:on` é ignorado pelo formatador e pelo linter. Os comentários podem ser de HTML:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Ou comentários do Django e do Jinja:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

Ou blocos `{% comment %}`:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Ou comentários de templates Go:

<!-- oxfmt-ignore -->
```html
{{/* djlint:off */}}
   <bad html to ignore>
{{/* djlint:on */}}
```

Ou comentários do Handlebars:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Ignorando regras

Regras específicas do linter também podem ser ignoradas adicionando o nome da regra à tag de abertura do bloco ignorado.

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
