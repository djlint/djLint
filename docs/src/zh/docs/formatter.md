---
description: 用 djLint 格式化你的 HTML 模板。快速、准确，输出结果让你的模板焕然一新。
title: 格式化工具用法
keywords: 模板代码检查工具, 模板格式化工具, djLint, HTML, 模板, 格式化工具, 代码检查工具, 格式化工具用法
---

# 格式化工具用法

djLint 的格式化工具能把杂乱的 HTML 模板整理成一致、易读的格式！

在应用更改之前，先用 `--check` 检查输出。

要查看格式化可能带来的更改，请运行：

```bash
djlint . --check
```

要格式化代码并更新文件，请运行：

```bash
djlint . --reformat --single-attribute-per-line

# 想同时格式化脚本和样式？
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">查看配置指南，了解所有选项！</a></div>
</div>

{% admonition
   "note",
   "注意",
   "写在属性中的 JSON 和 JavaScript 会保持原样，除非开启了 `--format-attribute-js-json`。属性中的 HTML 始终不会被改动。"
%}

{% admonition
   "note",
   "注意",
   "djLint 不是 HTML 解析器，也不是语法验证器。"
%}

## 来看个示例！

### 格式化之前

下面是一段急需整理的 HTML：

{% raw %}

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
{% if pagination_required %}
{% for i in page_range %}
{% paginator_number cl i %}
{% endfor %}
{% endif %}
{{ cl.result_count }}
{% if cl.result_count == 1 %}
{{ cl.opts.verbose_name }}
{% else %}
{{ cl.opts.verbose_name_plural }}
{% endif %}
{% if show_all_url %}
<a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}</a>
{% endif %}
{% if cl.formset and cl.result_count %}
<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">
{% endif %}
</p>
```

{% endraw %}

### 格式化之后

现在看起来好一些了……至少能读懂了 :)

{% raw %}

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input type="submit"
               name="_save"
               class="default"
               value="{% translate 'Save' %}">
    {% endif %}
</p>
```

{% endraw %}

### 启用 `single_attribute_per_line` 之后

更喜欢 Prettier 风格的属性？启用 `single_attribute_per_line` 选项：

{% raw %}

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input
            type="submit"
            name="_save"
            class="default"
            value="{% translate 'Save' %}"
        >
    {% endif %}
</p>
```

{% endraw %}
