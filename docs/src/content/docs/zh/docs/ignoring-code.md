---
title: "忽略代码"
description: "如何阻止 djLint 格式化某个代码块，以及如何以内联方式忽略代码检查规则。"
---

位于 `djlint:off` 和 `djlint:on` 注释之间的代码，格式化工具和代码检查工具都不会处理。这两个注释可以是 HTML 注释：

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

也可以是 Django 和 Jinja 的注释：

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

也可以是 `{% comment %}` 块：

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

也可以是 Go 模板的注释：

<!-- oxfmt-ignore -->
```html
{{/* djlint:off */}}
   <bad html to ignore>
{{/* djlint:on */}}
```

也可以是 Handlebars 的注释：

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## 忽略规则

也可以在忽略块的起始标签中写上规则名称，从而只忽略特定的代码检查规则。

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
