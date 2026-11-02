---
title: "Dobre praktyki"
description: "Dobre praktyki formatowania szablonów HTML za pomocą djLint."
sidebar:
  label: "Dobre praktyki"
---

## Spacje wokół atrybutów warunkowych

Czasami warunki służą do dodawania klas do tagu. djLint usuwa białe znaki wewnątrz instrukcji warunkowych.

Zalecany jest ten wzorzec:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

Ten wzorzec nie jest zalecany:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` i atrybuty warunkowe z tagami usuwającymi białe znaki

Jeśli opcja `format_attribute_template_tags` jest włączona, atrybuty warunkowe powinny używać tagów usuwających białe znaki, na przykład `{% if a -%}` w nunjucks i jinja, aby usunąć spacje wewnątrz tagu.

djLint rozbija długie atrybuty na kilka wierszy, a białe znaki zachowane wewnątrz atrybutów mogłyby zepsuć kod.

Zalecany jest ten wzorzec:

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

Każde zaznaczone miejsce to tag usuwający białe znaki.

Ten wzorzec nie jest zalecany:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Po sformatowaniu mogłoby to wyglądać tak:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
