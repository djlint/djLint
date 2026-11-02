---
description: Buone pratiche per formattare i template HTML con djLint.
title: Buone pratiche
keywords: linter per template, formattatore per template, djLint, HTML, template, formattatore, linter, buone pratiche
---

# Buone pratiche

## Spazi attorno agli attributi condizionali

A volte si usano delle condizioni per aggiungere classi a un tag. djLint rimuove gli spazi all'interno delle istruzioni condizionali.

Questo schema è consigliato:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ spazio qui
```

{% endraw %}

Questo schema è sconsigliato:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ spazio qui
```

{% endraw %}

## `format_attribute_template_tags` e attributi condizionali senza spazi

Se l'opzione `format_attribute_template_tags` è attiva, gli attributi condizionali devono usare tag senza spazi, ad esempio {% raw %}`{% if a -%}`{% endraw %} in nunjucks e jinja, per rimuovere gli spazi all'interno del tag.

djLint distribuisce gli attributi lunghi su più righe, e gli spazi conservati all'interno degli attributi potrebbero rompere il codice.

Questo schema è consigliato:

{% raw %}

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

{% endraw %}

Ogni posizione segnata è un tag senza spazi.

Questo schema è sconsigliato:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Dopo la formattazione potrebbe risultare così:

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
