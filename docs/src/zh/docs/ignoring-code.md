---
description: 如何防止 djLint 格式化代码块以及如何在行内忽略 djLint 规则。
title: 忽略码
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 代码格式化, 忽略规则, 忽略码
date: Last Modified
---

# 忽略码

使用包裹在 djLint 标签等忽略码来跳过代码检查/格式化：

{% raw %}

对于传统 HTML -

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

或使用注释 -

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

或使用长注释 -

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

亦或是 javascript 风格注释 -

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

以及 golang 风格注释 -

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## 忽略规则

通过这忽略模块中添加规则名，可以忽略特定代码检查规则。

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
