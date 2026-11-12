---
title: "Buenas prácticas"
description: "Buenas prácticas para usar djLint al formatear plantillas HTML."
sidebar:
  label: "Buenas prácticas"
---

## Espacios alrededor de los atributos condicionales

A veces se usan condiciones para añadir clases a una etiqueta. djLint elimina los espacios en blanco dentro de las sentencias condicionales.

Se recomienda este patrón:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ espacio aquí
```

No se recomienda este patrón:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ espacio aquí
```

## `format_attribute_template_tags` y atributos condicionales con control de espacios

Si la opción `format_attribute_template_tags` está activada, los atributos condicionales deben usar etiquetas con control de espacios, por ejemplo `{% if a -%}` en nunjucks y jinja, para eliminar los espacios dentro de la etiqueta.

djLint reparte los atributos largos en varias líneas, y los espacios en blanco que se conservan dentro de los atributos podrían romper tu código.

Se recomienda este patrón:

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

Cada posición marcada es una etiqueta con control de espacios.

No se recomienda este patrón:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Después de formatearlo, podría quedar así:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
