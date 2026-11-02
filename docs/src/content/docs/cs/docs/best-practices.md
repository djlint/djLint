---
title: "Osvědčené postupy"
description: "Osvědčené postupy pro formátování HTML šablon pomocí djLint."
sidebar:
  label: "Osvědčené postupy"
---

## Mezery kolem podmíněných atributů

Podmínky se někdy používají k přidání tříd do značky. djLint odstraňuje prázdné znaky uvnitř podmíněných příkazů.

Tento zápis doporučujeme:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

Tento zápis nedoporučujeme:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` a podmíněné atributy bez mezer

Pokud je zapnutá možnost `format_attribute_template_tags`, měly by podmíněné atributy používat značky bez mezer, například `{% if a -%}` v nunjucks a jinja, které odstraní mezery uvnitř značky.

djLint rozdělí dlouhé atributy na více řádků a prázdné znaky ponechané uvnitř atributů by mohly rozbít váš kód.

Tento zápis doporučujeme:

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

Každá označená pozice je značka bez mezer.

Tento zápis nedoporučujeme:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Po formátování by mohl vypadat takto:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
