---
title: "Bonnes pratiques"
description: "Bonnes pratiques pour formater des templates HTML avec djLint."
sidebar:
  label: "Bonnes pratiques"
---

## Espaces autour des attributs conditionnels

On utilise parfois des conditions pour ajouter des classes à une balise. djLint supprime les espaces à l'intérieur des instructions conditionnelles.

Cette forme est recommandée :

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

Cette forme est déconseillée :

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` et attributs conditionnels sans espaces

Si l'option `format_attribute_template_tags` est activée, les attributs conditionnels doivent utiliser des balises sans espaces, par exemple `{% if a -%}` en nunjucks et en jinja, afin de supprimer les espaces à l'intérieur de la balise.

djLint répartit les attributs longs sur plusieurs lignes, et les espaces ainsi conservés à l'intérieur des attributs pourraient casser votre code.

Cette forme est recommandée :

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

Chaque position marquée est une balise sans espaces.

Cette forme est déconseillée :

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Après formatage, on pourrait obtenir :

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
