---
title: "Formatter verwenden"
description: "Formatieren Sie Ihre HTML-Templates mit djLint. Schnell und präzise – das Ergebnis lässt Ihre Templates glänzen."
sidebar:
  label: "Formatter"
---

Der Formatter von djLint nimmt unordentliche HTML-Templates und formatiert sie einheitlich und leicht nachvollziehbar!

Prüfen Sie die Ausgabe mit `--check`, bevor Sie Änderungen übernehmen.

Um zu sehen, was sich beim Formatieren ändern würde, führen Sie Folgendes aus:

```bash
djlint . --check
```

Um den Code zu formatieren und die Dateien zu aktualisieren, führen Sie Folgendes aus:

```bash
djlint . --reformat --single-attribute-per-line

# und wie wäre es, auch Skripte und Styles zu formatieren?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::

:::note[Hinweis]
JSON und JavaScript in einem Attribut bleiben unverändert, sofern `--format-attribute-js-json` nicht aktiviert ist. HTML innerhalb eines Attributs wird nie angetastet.
:::

:::note[Hinweis]
djLint ist weder ein HTML-Parser noch ein Syntaxvalidator.
:::

## Ein Beispiel!

### Vorher

Hier ist ein Haufen HTML, der dringend etwas Zuwendung braucht:

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

### Nachher

Jetzt sieht es schon etwas besser aus … man kann es lesen :)

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

### Nachher mit `single_attribute_per_line`

Sie bevorzugen Attribute im Stil von Prettier? Aktivieren Sie die Option `single_attribute_per_line`:

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
