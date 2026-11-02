---
description: Рекомендации по форматированию HTML-шаблонов с помощью djLint.
title: Рекомендации
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, рекомендации
---

# Рекомендации

## Пробелы вокруг условных атрибутов

Иногда условия используются, чтобы добавить тегу классы. djLint удаляет пробельные символы внутри условных конструкций.

Рекомендуется такой вариант:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

Не рекомендуется такой вариант:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` и условные атрибуты без пробелов

Если включён параметр `format_attribute_template_tags`, в условных атрибутах следует использовать теги с удалением пробелов, например {% raw %}`{% if a -%}`{% endraw %} в nunjucks и jinja, чтобы убрать пробелы внутри тега.

djLint переносит длинные атрибуты на несколько строк, и пробельные символы, оставшиеся внутри атрибутов, могут сломать ваш код.

Рекомендуется такой вариант:

{% raw %}

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

{% endraw %}

Каждая отмеченная позиция — тег с удалением пробелов.

Не рекомендуется такой вариант:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

После форматирования это может выглядеть так:

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
