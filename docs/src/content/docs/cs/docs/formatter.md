---
title: "Použití formátovače"
description: "Jak djLint formátuje HTML šablony a jak si změny před použitím zkontrolovat."
sidebar:
  label: "Formátovač"
---

Formátovač djLint sjednocuje rozvržení HTML šablon. Nejdřív se podívejte, co by změnil:

```bash
djlint . --check --format-css --format-js
```

Potom soubory naformátujte na místě, tady i s obsahem `<style>` a `<script>`:

```bash
djlint . --reformat --format-css --format-js
```

:::note[Poznámka]
JSON a JavaScript zapsané v atributu zůstávají beze změny, pokud není zapnuté `--format-attribute-js-json`. HTML uvnitř atributu zůstává vždy beze změny.
:::

:::note[Poznámka]
djLint není parser HTML ani validátor syntaxe.
:::

## Ukázka

### Před

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

### Po

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

### Po s `single_attribute_per_line`

Dáváte přednost atributům ve stylu Prettier? Zapněte možnost `single_attribute_per_line`:

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
