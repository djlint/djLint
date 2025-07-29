---
description: 使用 djLint 格式化 HTML 模板的最佳实践。
title: 最佳实践
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 代码检查, 最佳实践
---

# 最佳实践

## 条件属性周围的空格

有时，条件语句会被用来向标签添加类（class）。djLint 会移除条件语句内部的空格。

推荐使用以下模式：

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ 注意这里的空格
```

{% endraw %}

不推荐使用一下模式：

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ 注意这里的空格
```

{% endraw %}

## `format_attribute_template_tags` 与无空格条件属性

若启用了 `format_attribute_template_tags`，条件属性应使用无空格标签，例如 numjuck 和 jinja 的 {% raw %}`{% if a -%}`{% endraw %}，应移除内部的空格。

djLint 会将长属性格式化为多行，而属性内部节省的空格可能会破坏您的代码。

推荐使用以下模式：

{% raw %}

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^ --
注意这里没有空格 tags
```

{% endraw %}

不推荐使用以下模式：

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

格式化之后代码如下：

{% raw %}

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```

{% endraw %}
