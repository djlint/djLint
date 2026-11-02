---
description: Buenas prácticas para usar djLint al formatear plantillas HTML.
title: Buenas prácticas
keywords: linter de plantillas, formateador de plantillas, djLint, HTML, plantillas, formateador, linter, buenas prácticas
---

# Buenas prácticas

## Espacios alrededor de los atributos condicionales

A veces se usan condiciones para añadir clases a una etiqueta. djLint elimina los espacios en blanco dentro de las sentencias condicionales.

Se recomienda este patrón:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

No se recomienda este patrón:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` y atributos condicionales con control de espacios

Si la opción `format_attribute_template_tags` está activada, los atributos condicionales deben usar etiquetas con control de espacios, por ejemplo {% raw %}`{% if a -%}`{% endraw %} en nunjucks y jinja, para eliminar los espacios dentro de la etiqueta.

djLint reparte los atributos largos en varias líneas, y los espacios en blanco que se conservan dentro de los atributos podrían romper tu código.

Se recomienda este patrón:

{% raw %}

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

{% endraw %}

Cada posición marcada es una etiqueta con control de espacios.

No se recomienda este patrón:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Después de formatearlo, podría quedar así:

{% raw %}

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```

{% endraw %}
