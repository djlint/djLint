---
description: 使用 djLint 格式化 HTML 範本的最佳做法。
title: 最佳做法
keywords: 範本 linter, 範本格式化工具, djLint, HTML, 範本, 格式化工具, linter, 最佳做法
---

# 最佳做法

## 條件式屬性周圍的空格

有時會用條件判斷為標籤加上 class。djLint 會移除條件陳述式內的空白。

建議使用這種寫法：

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

不建議使用這種寫法：

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` 與去除空白的條件式屬性

如果啟用了 `format_attribute_template_tags` 選項，條件式屬性應使用去除空白的標籤，例如 nunjucks 和 jinja 中的 {% raw %}`{% if a -%}`{% endraw %}，以移除標籤內的空格。

djLint 會將過長的屬性格式化成多行，而保留在屬性內的空白可能會破壞你的程式碼。

建議使用這種寫法：

{% raw %}

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

{% endraw %}

每個標記的位置都是去除空白的標籤。

不建議使用這種寫法：

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

格式化之後可能會變成這樣：

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
