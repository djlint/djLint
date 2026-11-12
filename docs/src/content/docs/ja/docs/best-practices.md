---
title: "ベストプラクティス"
description: "djLint で HTML テンプレートをフォーマットするときのベストプラクティス。"
sidebar:
  label: "ベストプラクティス"
---

## 条件付き属性の周りのスペース

タグにクラスを追加するために条件を使うことがあります。djLint は条件文の内側の空白を取り除きます。

次のパターンを推奨します：

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ ここにスペース
```

次のパターンは推奨しません：

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ ここにスペース
```

## `format_attribute_template_tags` と空白制御付きの条件付き属性

`format_attribute_template_tags` オプションを有効にしている場合、条件付き属性では、タグ内のスペースを取り除くために空白制御タグ（nunjucks や jinja の `{% if a -%}` など）を使ってください。

djLint は長い属性を複数行にフォーマットするため、属性内に残った空白によってコードが壊れるおそれがあります。

次のパターンを推奨します：

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

印を付けた位置はそれぞれ空白制御タグです。

次のパターンは推奨しません：

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

フォーマット後は次のようになる可能性があります：

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
