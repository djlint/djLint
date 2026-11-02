---
title: "Używanie formatera"
description: "Jak djLint formatuje szablony HTML i jak sprawdzić zmiany przed ich zastosowaniem."
sidebar:
  label: "Formater"
---

Formater djLint weźmie niechlujne szablony HTML i nada im spójne, czytelne formatowanie!

Zanim zastosujesz zmiany, przejrzyj wynik za pomocą `--check`.

Aby sprawdzić, co może się zmienić w formatowaniu, uruchom:

```bash
djlint . --check
```

Aby sformatować kod i zaktualizować pliki, uruchom:

```bash
djlint . --reformat --single-attribute-per-line

# a może sformatować też skrypty i style?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::

:::note[Uwaga]
JSON i JavaScript zapisane w atrybucie pozostają bez zmian, chyba że włączona jest opcja `--format-attribute-js-json`. HTML wewnątrz atrybutu nigdy nie jest zmieniany.
:::

:::note[Uwaga]
djLint nie jest parserem HTML ani walidatorem składni.
:::

## Oto przykład!

### Przed

Oto kawałek HTML-a, który rozpaczliwie potrzebuje uwagi:

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

Teraz wygląda trochę lepiej… da się to czytać :)

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

### Po włączeniu `single_attribute_per_line`

Wolisz atrybuty w stylu Prettiera? Włącz opcję `single_attribute_per_line`:

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
