---
description: Jak djLint formátuje HTML šablony a jak si změny před použitím zkontrolovat.
title: Použití formátovače
keywords: linter šablon, formátovač šablon, djLint, HTML, šablony, formátovač, linter, použití formátovače
---

# Použití formátovače

Formátovač djLint vezme neupravené HTML šablony a sjednotí jejich formátování, aby byly přehledné a snadno čitelné!

Než změny použijete, prohlédněte si výstup s `--check`.

Chcete-li zjistit, co se při formátování může změnit, spusťte:

```bash
djlint . --check --single-attribute-per-line
```

Chcete-li kód naformátovat a soubory aktualizovat, spusťte:

```bash
djlint . --reformat --single-attribute-per-line

# a co takhle naformátovat i skripty a styly?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Všechny možnosti najdete v průvodci konfigurací!</a></div>
</div>

{% admonition
   "note",
   "Poznámka",
   "JSON a JavaScript zapsané v atributu zůstávají beze změny, pokud není zapnuté `--format-attribute-js-json`. HTML uvnitř atributu zůstává vždy beze změny."
%}

{% admonition
   "note",
   "Poznámka",
   "djLint není parser HTML ani validátor syntaxe."
%}

## Ukázka

### Před

Tady je kus HTML, který zoufale potřebuje péči:

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

### Po

Teď to vypadá o něco lépe… dá se to přečíst :)

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

### Po s `single_attribute_per_line`

Dáváte přednost atributům ve stylu Prettier? Zapněte možnost `single_attribute_per_line`:

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
