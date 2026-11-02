---
description: Dobre praktyki formatowania szablonów HTML za pomocą djLint.
title: Dobre praktyki
keywords: linter szablonów, formater szablonów, djLint, HTML, szablony, formater, linter, dobre praktyki
---

# Dobre praktyki

## Spacje wokół atrybutów warunkowych

Czasami warunki służą do dodawania klas do tagu. djLint usuwa białe znaki wewnątrz instrukcji warunkowych.

Zalecany jest ten wzorzec:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

Ten wzorzec nie jest zalecany:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` i atrybuty warunkowe z tagami usuwającymi białe znaki

Jeśli opcja `format_attribute_template_tags` jest włączona, atrybuty warunkowe powinny używać tagów usuwających białe znaki, na przykład {% raw %}`{% if a -%}`{% endraw %} w nunjucks i jinja, aby usunąć spacje wewnątrz tagu.

djLint rozbija długie atrybuty na kilka wierszy, a białe znaki zachowane wewnątrz atrybutów mogłyby zepsuć kod.

Zalecany jest ten wzorzec:

{% raw %}

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

{% endraw %}

Każde zaznaczone miejsce to tag usuwający białe znaki.

Ten wzorzec nie jest zalecany:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Po sformatowaniu mogłoby to wyglądać tak:

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
