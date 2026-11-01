---
title: "代码格式化"
description: "使用 djLint 格式化你的 HTML 模板。又快又准的使你的模板焕发光彩。"
sidebar:
  label: "代码格式化"
---

djLint 的格式化工具可以处理混乱的HTML模板，使之变得格式统一且易于模仿！

在确认修改之前使用 `--check` 查看输出。

预览格式化修改内容：

```bash
djlint . --check
```

直接格式化：

```bash
djlint . --reformat --single-attribute-per-line

# 顺带格式化一下脚本和样式？
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
详情请参考 [配置](/zh/docs/configuration/) 章节
:::

:::note[注意]
写在属性里的 JSON 和 JavaScript 保持原样，除非开启 `--format-attribute-js-json`。属性中的 HTML 始终不作改动。
:::

:::note[注意]
djLint 并非 HTML 解析器或语法验证器。
:::

## 示例

### 处理前

下面是一段急需处理的 HTML 代码块 -

<!-- prettier-ignore -->
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

### 处理后

看起来好多了…… 至少我们能读得下去了：

<!-- prettier-ignore -->
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

### 使用 `single_attribute_per_line` 的处理结果

如果你更喜欢 Prettier 风格的属性排版，可以启用 `single_attribute_per_line` 选项：

<!-- prettier-ignore -->
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
