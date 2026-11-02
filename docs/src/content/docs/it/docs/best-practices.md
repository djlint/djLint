---
title: "Buone pratiche"
description: "Buone pratiche per formattare i template HTML con djLint."
sidebar:
  label: "Buone pratiche"
---

## Spazi attorno agli attributi condizionali

A volte si usano delle condizioni per aggiungere classi a un tag. djLint rimuove gli spazi all'interno delle istruzioni condizionali.

Questo schema è consigliato:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ spazio qui
```

Questo schema è sconsigliato:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ spazio qui
```

## `format_attribute_template_tags` e attributi condizionali senza spazi

Se l'opzione `format_attribute_template_tags` è attiva, gli attributi condizionali devono usare tag senza spazi, ad esempio `{% if a -%}` in nunjucks e jinja, per rimuovere gli spazi all'interno del tag.

djLint distribuisce gli attributi lunghi su più righe, e gli spazi conservati all'interno degli attributi potrebbero rompere il codice.

Questo schema è consigliato:

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

Ogni posizione segnata è un tag senza spazi.

Questo schema è sconsigliato:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Dopo la formattazione potrebbe risultare così:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
