---
title: "Рекомендации"
description: "Рекомендации по форматированию HTML-шаблонов с помощью djLint."
sidebar:
  label: "Рекомендации"
---

## Пробелы вокруг условных атрибутов

Иногда условия используются, чтобы добавить тегу классы. djLint удаляет пробельные символы внутри условных конструкций.

Рекомендуется такой вариант:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

Не рекомендуется такой вариант:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` и условные атрибуты без пробелов

Если включён параметр `format_attribute_template_tags`, в условных атрибутах следует использовать теги с удалением пробелов, например `{% if a -%}` в nunjucks и jinja, чтобы убрать пробелы внутри тега.

djLint переносит длинные атрибуты на несколько строк, и пробельные символы, оставшиеся внутри атрибутов, могут сломать ваш код.

Рекомендуется такой вариант:

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

Каждая отмеченная позиция — тег с удалением пробелов.

Не рекомендуется такой вариант:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

После форматирования это может выглядеть так:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
