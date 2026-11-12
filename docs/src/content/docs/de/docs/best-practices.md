---
title: "Best Practices"
description: "Best Practices für das Formatieren von HTML-Templates mit djLint."
sidebar:
  label: "Best Practices"
---

## Leerzeichen um bedingte Attribute

Manchmal werden Bedingungen verwendet, um einem Tag Klassen hinzuzufügen. djLint entfernt Leerraum innerhalb von Bedingungen.

Dieses Muster wird empfohlen:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

Dieses Muster wird nicht empfohlen:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` und bedingte Attribute mit Whitespace-Kontrolle

Ist die Option `format_attribute_template_tags` aktiviert, sollten bedingte Attribute Tags mit Whitespace-Kontrolle verwenden, zum Beispiel `{% if a -%}` in Nunjucks und Jinja, damit der Leerraum innerhalb des Tags entfernt wird.

djLint verteilt lange Attribute auf mehrere Zeilen, und Leerraum, der innerhalb von Attributen erhalten bleibt, könnte Ihren Code kaputtmachen.

Dieses Muster wird empfohlen:

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

Jede markierte Stelle ist ein Tag mit Whitespace-Kontrolle.

Dieses Muster wird nicht empfohlen:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Nach dem Formatieren könnte es so aussehen:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
