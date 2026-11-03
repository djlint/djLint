---
description: Wie djLint HTML-Templates formatiert und wie Sie die Änderungen prüfen, bevor Sie sie übernehmen.
title: Formatter verwenden
keywords: Template-Linter, Template-Formatter, djLint, HTML, Templates, Formatter, Linter, Formatter verwenden
---

# Formatter verwenden

Der Formatter von djLint nimmt unordentliche HTML-Templates und formatiert sie einheitlich und leicht nachvollziehbar!

Prüfen Sie die Ausgabe mit `--check`, bevor Sie Änderungen übernehmen.

Um zu sehen, was sich beim Formatieren ändern würde, führen Sie Folgendes aus:

```bash
djlint . --check --single-attribute-per-line
```

Um den Code zu formatieren und die Dateien zu aktualisieren, führen Sie Folgendes aus:

```bash
djlint . --reformat --single-attribute-per-line

# und wie wäre es, auch Skripte und Styles zu formatieren?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Alle Optionen finden Sie in der Anleitung zur Konfiguration!</a></div>
</div>

{% admonition
   "note",
   "Hinweis",
   "JSON und JavaScript in einem Attribut bleiben unverändert, sofern `--format-attribute-js-json` nicht aktiviert ist. HTML innerhalb eines Attributs wird nie angetastet."
%}

{% admonition
   "note",
   "Hinweis",
   "djLint ist weder ein HTML-Parser noch ein Syntaxvalidator."
%}

## Ein Beispiel!

### Vorher

Hier ist ein Haufen HTML, der dringend etwas Zuwendung braucht:

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

### Nachher

Jetzt sieht es schon etwas besser aus … man kann es lesen :)

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

### Nachher mit `single_attribute_per_line`

Sie bevorzugen Attribute im Stil von Prettier? Aktivieren Sie die Option `single_attribute_per_line`:

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
