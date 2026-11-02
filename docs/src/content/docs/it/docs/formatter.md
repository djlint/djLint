---
title: "Uso del formattatore"
description: "Formatta i tuoi template HTML con djLint. Veloce e preciso, con un risultato che farà brillare i tuoi template."
sidebar:
  label: "Formattatore"
---

Il formattatore di djLint prende template HTML disordinati e ne rende la formattazione coerente e facile da seguire!

Controlla l'output con `--check` prima di applicare le modifiche.

Per vedere cosa potrebbe cambiare nella formattazione, esegui:

```bash
djlint . --check
```

Per formattare il codice e aggiornare i file, esegui:

```bash
djlint . --reformat --single-attribute-per-line

# e se formattassimo anche script e stili?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::

:::note[Nota]
JSON e JavaScript scritti in un attributo restano come sono, a meno che non sia attivo `--format-attribute-js-json`. L'HTML all'interno di un attributo non viene mai toccato.
:::

:::note[Nota]
djLint non è un parser HTML né un validatore di sintassi.
:::

## Ecco un esempio!

### Prima

Ecco un blocco di HTML che ha disperatamente bisogno di attenzione:

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

### Dopo

Ora va un po' meglio... si riesce a leggere :)

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

### Dopo, con `single_attribute_per_line`

Preferisci gli attributi in stile Prettier? Attiva l'opzione `single_attribute_per_line`:

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
