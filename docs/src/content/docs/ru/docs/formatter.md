---
title: "Использование форматера"
description: "Форматируйте HTML-шаблоны с помощью djLint. Быстро и точно — ваши шаблоны будут выглядеть безупречно."
sidebar:
  label: "Форматер"
---

Форматер djLint берёт неаккуратные HTML-шаблоны и делает их оформление единообразным и удобным для чтения!

Прежде чем применять изменения, просмотрите результат с `--check`.

Чтобы посмотреть, что изменится при форматировании, выполните:

```bash
djlint . --check
```

Чтобы отформатировать код и обновить файлы, выполните:

```bash
djlint . --reformat --single-attribute-per-line

# а заодно отформатировать скрипты и стили?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::

:::note[Примечание]
JSON и JavaScript внутри атрибута остаются как есть, если не включён `--format-attribute-js-json`. HTML внутри атрибута не изменяется никогда.
:::

:::note[Примечание]
djLint не является HTML-парсером или валидатором синтаксиса.
:::

## Пример

### До

Вот фрагмент HTML, которому срочно требуется внимание:

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

### После

Стало немного лучше... теперь это хотя бы можно читать :)

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

### После с `single_attribute_per_line`

Предпочитаете атрибуты в стиле Prettier? Включите параметр `single_attribute_per_line`:

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
