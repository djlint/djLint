---
title: "忽略程式碼"
description: "如何避免 djLint 格式化某個程式碼區塊，以及如何在行內忽略 linter 規則。"
---

位於 `djlint:off` 和 `djlint:on` 註解之間的程式碼，格式化工具和 linter 都不會處理。這些註解可以是 HTML 註解：

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

或是 Django 和 Jinja 的註解：

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

或是 `{% comment %}` 區塊：

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

或是 Go 範本的註解：

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

或是 Handlebars 的註解：

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## 忽略規則

也可以在忽略區塊的開頭標籤中加上規則名稱，藉此忽略特定的 linter 規則。

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
