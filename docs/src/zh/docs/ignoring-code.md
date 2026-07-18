---
description: 如何防止 djLint 格式化代码块以及如何在行内忽略 djLint 规则。
title: 忽略代码
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 代码格式化, 忽略规则, 忽略代码
date: Last Modified
---

# 忽略代码

可以通过用 djLint 标签包裹代码来跳过代码检查或格式化：

{% raw %}

对于传统 HTML -

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

或使用注释 -

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

或使用长注释 -

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

亦或是 javascript 风格注释 -

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

以及 golang 风格注释 -

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

{% endraw %}

## 忽略规则

通过在忽略块的开始标签中添加规则名，可以忽略特定的代码检查规则。

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
