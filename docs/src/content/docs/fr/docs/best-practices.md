---
title: "Meilleures Pratiques"
description: "Meilleures pratiques pour l'utilisation de djLint pour formater les modèles HTML."
sidebar:
  label: "Bonnes pratiques"
---

## Espaces autour des attributs conditionnels

Parfois, les conditions sont utilisées pour ajouter des classes à une balise. djLint supprime les espaces à l'intérieur des déclarations conditionnelles.

Ce modèle est recommandé :

```html
<div class="class1 {% if condition -%}class2{%- endif %}">contenu</div>
                  ^ espace ici
```

Ce modèle n'est pas recommandé :

```html
<div class="class1{% if condition -%} class2{%- endif %}">contenu</div>
                                     ^ espace ici
```

## `format_attribute_template_tags` et des attributs conditionnels non spatiaux

Si l'option `format_attribute_template_tags` est activée, les attributs conditionnels devraient utiliser des balises sans espace, par exemple `{% if a -%}` dans nunjucks et jinja, pour supprimer les espaces à l'intérieur de la balise.

djLint formatera les attributs longs sur plusieurs lignes, et l'espacement conservé à l'intérieur des attributs pourrait casser votre code.

Ce modèle est recommandé :

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

Chaque position marquée est une balise sans espace.

Ce modèle n'est pas recommandé :

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Après le formatage, cela pourrait ressembler à ceci :

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
