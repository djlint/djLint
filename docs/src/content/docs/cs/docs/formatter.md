---
title: "Použití formátovače"
description: "Formátujte HTML šablony pomocí djLint. Rychle, přesně a s výsledkem, díky kterému budou vaše šablony zářit."
sidebar:
  label: "Formátovač"
---

Formátovač djLint vezme neupravené HTML šablony a sjednotí jejich formátování, aby byly přehledné a snadno čitelné!

Než změny použijete, prohlédněte si výstup s `--check`.

Chcete-li zjistit, co se při formátování může změnit, spusťte:

```bash
djlint . --check
```

Chcete-li kód naformátovat a soubory aktualizovat, spusťte:

```bash
djlint . --reformat --single-attribute-per-line

# a co takhle naformátovat i skripty a styly?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::

:::note[Poznámka]
JSON a JavaScript zapsané v atributu zůstávají beze změny, pokud není zapnuté `--format-attribute-js-json`. HTML uvnitř atributu zůstává vždy beze změny.
:::

:::note[Poznámka]
djLint není parser HTML ani validátor syntaxe.
:::

## Ukázka

### Před

Tady je kus HTML, který zoufale potřebuje péči:

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

### Po

Teď to vypadá o něco lépe… dá se to přečíst :)

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

### Po s `single_attribute_per_line`

Dáváte přednost atributům ve stylu Prettier? Zapněte možnost `single_attribute_per_line`:

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
