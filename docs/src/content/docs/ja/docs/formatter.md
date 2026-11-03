---
title: "フォーマッターの使い方"
description: "djLint による HTML テンプレートのフォーマットと、変更を適用する前に確認する方法。"
sidebar:
  label: "フォーマッター"
---

djLint のフォーマッターは、雑に書かれた HTML テンプレートを、一貫性があって読みやすいフォーマットに整えます！

変更を適用する前に、`--check` で出力を確認してください。

フォーマットで何が変わるかを確認するには、次のコマンドを実行します：

```bash
djlint . --check --single-attribute-per-line
```

コードをフォーマットしてファイルを更新するには、次のコマンドを実行します：

```bash
djlint . --reformat --single-attribute-per-line

# スクリプトとスタイルもフォーマットするには？
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::

:::note[メモ]
属性内に書かれた JSON と JavaScript は、`--format-attribute-js-json` を有効にしない限りそのまま残されます。属性内の HTML は常にそのまま残されます。
:::

:::note[メモ]
djLint は HTML パーサーでも構文バリデーターでもありません。
:::

## 例を見てみましょう！

### 変更前

手入れがどうしても必要な HTML の塊です：

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

少し良くなりました……これなら読めますね :)

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
