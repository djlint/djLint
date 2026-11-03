---
description: djLint 如何格式化 HTML 範本，以及如何在套用前檢查變更。
title: 格式化工具用法
keywords: 範本 linter, 範本格式化工具, djLint, HTML, 範本, 格式化工具, linter, 格式化工具用法
---

# 格式化工具用法

djLint 的格式化工具能把凌亂的 HTML 範本整理成一致、易讀的格式！

套用變更前，請先用 `--check` 檢視輸出結果。

若要檢視格式化可能會變更哪些地方，請執行：

```bash
djlint . --check --single-attribute-per-line
```

若要格式化程式碼並更新檔案，請執行：

```bash
djlint . --reformat --single-attribute-per-line

# 也想格式化 script 和 style 嗎？
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">查看設定指南，了解所有選項！</a></div>
</div>

{% admonition
   "note",
   "注意",
   "除非開啟了 `--format-attribute-js-json`，否則寫在屬性中的 JSON 和 JavaScript 會保持原樣。屬性中的 HTML 一律不會被更動。"
%}

{% admonition
   "note",
   "注意",
   "djLint 不是 HTML 剖析器，也不是語法驗證器。"
%}

## 來看個範例！

### 格式化前

這是一團急需整理的 HTML：

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

### 格式化後

現在看起來好一點了……至少讀得懂了 :)

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

### 使用 `single_attribute_per_line` 格式化後

偏好 Prettier 風格的屬性排列嗎？請啟用 `single_attribute_per_line` 選項：

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
