---
title: "Uso del formateador"
description: "Cómo formatea djLint las plantillas HTML y cómo revisar los cambios antes de aplicarlos."
sidebar:
  label: "Formateador"
---

El formateador de djLint deja coherente la disposición de las plantillas HTML. Primero mira qué cambiaría:

```bash
djlint . --check --format-css --format-js
```

Después formatea los archivos en su sitio, aquí también con el contenido de `<style>` y `<script>`:

```bash
djlint . --reformat --format-css --format-js
```

:::note[Nota]
El JSON y el JavaScript escritos dentro de un atributo se dejan como están, salvo que `--format-attribute-js-json` esté activado. El HTML dentro de un atributo nunca se toca.
:::

:::note[Nota]
djLint no es un analizador sintáctico de HTML ni un validador de sintaxis.
:::

## Ejemplo

### Antes

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

### Después

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

### Después, con `single_attribute_per_line`

¿Prefieres los atributos al estilo de Prettier? Activa la opción `single_attribute_per_line`:

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
