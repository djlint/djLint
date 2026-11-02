---
description: Osvědčené postupy pro formátování HTML šablon pomocí djLint.
title: Osvědčené postupy
keywords: linter šablon, formátovač šablon, djLint, HTML, šablony, formátovač, linter, osvědčené postupy
---

# Osvědčené postupy

## Mezery kolem podmíněných atributů

Podmínky se někdy používají k přidání tříd do značky. djLint odstraňuje prázdné znaky uvnitř podmíněných příkazů.

Tento zápis doporučujeme:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

Tento zápis nedoporučujeme:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` a podmíněné atributy bez mezer

Pokud je zapnutá možnost `format_attribute_template_tags`, měly by podmíněné atributy používat značky bez mezer, například {% raw %}`{% if a -%}`{% endraw %} v nunjucks a jinja, které odstraní mezery uvnitř značky.

djLint rozdělí dlouhé atributy na více řádků a prázdné znaky ponechané uvnitř atributů by mohly rozbít váš kód.

Tento zápis doporučujeme:

{% raw %}

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

{% endraw %}

Každá označená pozice je značka bez mezer.

Tento zápis nedoporučujeme:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Po formátování by mohl vypadat takto:

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
