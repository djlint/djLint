---
description: djLint で HTML テンプレートをフォーマットするときのベストプラクティス。
title: ベストプラクティス
keywords: テンプレート リンター, テンプレート フォーマッター, djLint, HTML, テンプレート, フォーマッター, リンター, ベストプラクティス
---

# ベストプラクティス

## 条件付き属性の周りのスペース

タグにクラスを追加するために条件を使うことがあります。djLint は条件文の内側の空白を取り除きます。

次のパターンを推奨します：

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ ここにスペース
```

{% endraw %}

次のパターンは推奨しません：

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ ここにスペース
```

{% endraw %}

## `format_attribute_template_tags` と空白制御付きの条件付き属性

`format_attribute_template_tags` オプションを有効にしている場合、条件付き属性では、タグ内のスペースを取り除くために空白制御タグ（nunjucks や jinja の {% raw %}`{% if a -%}`{% endraw %} など）を使ってください。

djLint は長い属性を複数行にフォーマットするため、属性内に残った空白によってコードが壊れるおそれがあります。

次のパターンを推奨します：

{% raw %}

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

{% endraw %}

印を付けた位置はそれぞれ空白制御タグです。

次のパターンは推奨しません：

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

フォーマット後は次のようになる可能性があります：

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
