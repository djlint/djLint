---
title: "最佳实践"
description: "使用 djLint 格式化 HTML 模板的最佳实践。"
sidebar:
  label: "最佳实践"
---

## 条件属性周围的空格

有时会用条件语句给标签添加 class。djLint 会删除条件语句内部的空白。

推荐这种写法：

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

不推荐这种写法：

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` 与无空白条件属性

如果启用了 `format_attribute_template_tags` 选项，条件属性应使用无空白标签（例如 Nunjucks 和 Jinja 中的 `{% if a -%}`）来删除标签内部的空格。

djLint 会把较长的属性格式化为多行，属性中保留下来的空白可能会破坏你的代码。

推荐这种写法：

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

每个标记的位置都是一个无空白标签。

不推荐这种写法：

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

格式化之后可能会变成这样：

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
