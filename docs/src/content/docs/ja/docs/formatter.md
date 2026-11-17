---
title: "フォーマッターの使い方"
description: "djLint による HTML テンプレートのフォーマットと、変更を適用する前に確認する方法。"
sidebar:
  label: "フォーマッター"
---

djLint のフォーマッターは、HTML テンプレートのレイアウトを一貫したものに整えます。まず、何が変わるかを確認します：

```bash
djlint . --check --format-css --format-js
```

次に、ファイルをその場でフォーマットします。この例では `<style>` と `<script>` の中身もフォーマットします：

```bash
djlint . --reformat --format-css --format-js
```

:::note[メモ]
属性内に書かれた JSON と JavaScript は、`--format-attribute-js-json` を有効にしない限りそのまま残されます。属性内の HTML は常にそのまま残されます。
:::

:::note[メモ]
djLint は HTML パーサーでも構文バリデーターでもありません。
:::

## 例

### 変更前

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

### 変更後

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

### `single_attribute_per_line` を使った変更後

Prettier 形式の属性のほうが好みですか？`single_attribute_per_line` オプションを有効にしてください：

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
