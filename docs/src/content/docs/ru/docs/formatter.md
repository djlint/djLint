---
title: "Использование форматера"
description: "Форматируйте свои HTML-шаблоны с помощью djLint. Быстрый и точный вывод сделает ваши шаблоны блестящими."
sidebar:
  label: "Форматер"
---

Форматировщик djLint возьмет неряшливые html-шаблоны и сделает форматирование последовательным и легким!

Прежде чем вносить изменения, проверьте результат с помощью `--check`.

Чтобы просмотреть, что может измениться в форматировании, выполните следующие действия:

```bash
djlint . --check
```

Для форматирования кода и обновления файлов выполните:

```bash
djlint . --reformat --single-attribute-per-line

# а заодно отформатировать скрипты и стили?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!](/ru/docs/configuration/)
:::

:::note[Note]
JSON и JavaScript, записанные в атрибут, остаются как есть, если не включён `--format-attribute-js-json`. HTML внутри атрибута не трогается никогда.
:::

:::note[Note]
djLint не является парсером html или синтаксическим валидатором.
:::

## Вот пример!

### До

Вот кусок HTML, который отчаянно нуждается во внимании -

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

### После

Теперь он выглядит немного лучше... мы можем его прочитать :)

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

### После с `single_attribute_per_line`

Предпочитаете атрибуты в стиле Prettier? Включите опцию `single_attribute_per_line`:

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
