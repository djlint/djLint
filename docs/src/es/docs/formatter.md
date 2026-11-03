---
description: Cómo formatea djLint las plantillas HTML y cómo revisar los cambios antes de aplicarlos.
title: Uso del formateador
keywords: linter de plantillas, formateador de plantillas, djLint, HTML, plantillas, formateador, linter, uso del formateador
---

# Uso del formateador

¡El formateador de djLint toma plantillas HTML descuidadas y deja su formato coherente y fácil de seguir!

Revisa el resultado con `--check` antes de aplicar los cambios.

Para ver qué podría cambiar en el formato, ejecuta:

```bash
djlint . --check --single-attribute-per-line
```

Para formatear el código y actualizar los archivos, ejecuta:

```bash
djlint . --reformat --single-attribute-per-line

# ¿y si también formateamos los scripts y los estilos?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">¡Consulta la guía de configuración para ver todas las opciones!</a></div>
</div>

{% admonition
   "note",
   "Nota",
   "El JSON y el JavaScript escritos dentro de un atributo se dejan como están, salvo que `--format-attribute-js-json` esté activado. El HTML dentro de un atributo nunca se toca."
%}

{% admonition
   "note",
   "Nota",
   "djLint no es un analizador sintáctico de HTML ni un validador de sintaxis."
%}

## ¡Veamos un ejemplo!

### Antes

Este es un bloque de HTML que necesita atención urgente:

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

### Después

Ahora se ve un poco mejor... ya se puede leer :)

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

### Después, con `single_attribute_per_line`

¿Prefieres los atributos al estilo de Prettier? Activa la opción `single_attribute_per_line`:

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
