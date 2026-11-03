---
description: Jak djLint formatuje szablony HTML i jak sprawdzić zmiany przed ich zastosowaniem.
title: Używanie formatera
keywords: linter szablonów, formater szablonów, djLint, HTML, szablony, formater, linter, używanie formatera
---

# Używanie formatera

Formater djLint weźmie niechlujne szablony HTML i nada im spójne, czytelne formatowanie!

Zanim zastosujesz zmiany, przejrzyj wynik za pomocą `--check`.

Aby sprawdzić, co może się zmienić w formatowaniu, uruchom:

```bash
djlint . --check --single-attribute-per-line
```

Aby sformatować kod i zaktualizować pliki, uruchom:

```bash
djlint . --reformat --single-attribute-per-line

# a może sformatować też skrypty i style?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Wszystkie opcje znajdziesz w przewodniku po konfiguracji!</a></div>
</div>

{% admonition
   "note",
   "Uwaga",
   "JSON i JavaScript zapisane w atrybucie pozostają bez zmian, chyba że włączona jest opcja `--format-attribute-js-json`. HTML wewnątrz atrybutu nigdy nie jest zmieniany."
%}

{% admonition
   "note",
   "Uwaga",
   "djLint nie jest parserem HTML ani walidatorem składni."
%}

## Oto przykład!

### Przed

Oto kawałek HTML-a, który rozpaczliwie potrzebuje uwagi:

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

Teraz wygląda trochę lepiej… da się to czytać :)

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

### Po włączeniu `single_attribute_per_line`

Wolisz atrybuty w stylu Prettiera? Włącz opcję `single_attribute_per_line`:

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
