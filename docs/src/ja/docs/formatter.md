---
description: djLint で HTML テンプレートをフォーマットしましょう。高速かつ正確で、出力はテンプレートを美しく整えます。
title: フォーマッターの使い方
keywords: テンプレート リンター, テンプレート フォーマッター, djLint, HTML, テンプレート, フォーマッター, リンター, フォーマッターの使い方
---

# フォーマッターの使い方

djLint のフォーマッターは、雑に書かれた HTML テンプレートを、一貫性があって読みやすいフォーマットに整えます！

変更を適用する前に、`--check` で出力を確認してください。

フォーマットで何が変わるかを確認するには、次のコマンドを実行します：

```bash
djlint . --check
```

コードをフォーマットしてファイルを更新するには、次のコマンドを実行します：

```bash
djlint . --reformat --single-attribute-per-line

# スクリプトとスタイルもフォーマットするには？
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">すべてのオプションは設定ガイドで確認してください！</a></div>
</div>

{% admonition
   "note",
   "メモ",
   "属性内に書かれた JSON と JavaScript は、`--format-attribute-js-json` を有効にしない限りそのまま残されます。属性内の HTML は常にそのまま残されます。"
%}

{% admonition
   "note",
   "メモ",
   "djLint は HTML パーサーでも構文バリデーターでもありません。"
%}

## 例を見てみましょう！

### 変更前

手入れがどうしても必要な HTML の塊です：

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

### 変更後

少し良くなりました……これなら読めますね :)

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

### `single_attribute_per_line` を使った変更後

Prettier 形式の属性のほうが好みですか？`single_attribute_per_line` オプションを有効にしてください：

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
