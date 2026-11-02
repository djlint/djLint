---
description: Best Practices für das Formatieren von HTML-Templates mit djLint.
title: Best Practices
keywords: Template-Linter, Template-Formatter, djLint, HTML, Templates, Formatter, Linter, Best Practices
---

# Best Practices

## Leerzeichen um bedingte Attribute

Manchmal werden Bedingungen verwendet, um einem Tag Klassen hinzuzufügen. djLint entfernt Leerraum innerhalb von Bedingungen.

Dieses Muster wird empfohlen:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

Dieses Muster wird nicht empfohlen:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` und bedingte Attribute mit Whitespace-Kontrolle

Ist die Option `format_attribute_template_tags` aktiviert, sollten bedingte Attribute Tags mit Whitespace-Kontrolle verwenden, zum Beispiel {% raw %}`{% if a -%}`{% endraw %} in Nunjucks und Jinja, damit der Leerraum innerhalb des Tags entfernt wird.

djLint verteilt lange Attribute auf mehrere Zeilen, und Leerraum, der innerhalb von Attributen erhalten bleibt, könnte Ihren Code kaputtmachen.

Dieses Muster wird empfohlen:

{% raw %}

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

{% endraw %}

Jede markierte Stelle ist ein Tag mit Whitespace-Kontrolle.

Dieses Muster wird nicht empfohlen:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Nach dem Formatieren könnte es so aussehen:

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
