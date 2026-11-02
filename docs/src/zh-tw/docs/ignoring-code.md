---
description: 如何避免 djLint 格式化某個程式碼區塊，以及如何在行內忽略 djLint 規則。
title: 忽略程式碼
keywords: 範本 linter, 範本格式化工具, djLint, HTML, 範本, 格式化工具, linter, 格式化工具用法, 忽略程式碼, 忽略規則
date: Last Modified
---

# 忽略程式碼

只要用 `djlint` 標籤包住程式碼，就能忽略它：

{% raw %}

一般的 HTML：

<!-- oxfmt-ignore -->

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

或寫成註解：

<!-- oxfmt-ignore -->

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

或寫成長註解：

<!-- oxfmt-ignore -->

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

或寫成 golang 風格的註解：

<!-- oxfmt-ignore -->

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

或寫成 handlebars 風格的註解：

<!-- oxfmt-ignore -->

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## 忽略規則

也可以在忽略區塊的開頭標籤中加上規則名稱，藉此忽略特定的 linter 規則。

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
