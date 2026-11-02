---
description: Форматируйте HTML-шаблоны с помощью djLint. Быстро и точно — ваши шаблоны будут выглядеть безупречно.
title: Использование форматера
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование форматера
---

# Использование форматера

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

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Обо всех параметрах читайте в руководстве по конфигурации!</a></div>
</div>

{% admonition
   "note",
   "Примечание",
   "JSON и JavaScript внутри атрибута остаются как есть, если не включён `--format-attribute-js-json`. HTML внутри атрибута не изменяется никогда."
%}

{% admonition
   "note",
   "Примечание",
   "djLint не является HTML-парсером или валидатором синтаксиса."
%}

## Пример

### До

Вот фрагмент HTML, которому срочно требуется внимание:

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

### После

Стало немного лучше... теперь это хотя бы можно читать :)

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

### После с `single_attribute_per_line`

Предпочитаете атрибуты в стиле Prettier? Включите параметр `single_attribute_per_line`:

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
