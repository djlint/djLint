---
description: Meilleures pratiques pour l'utilisation de djLint pour formater les modèles HTML.
title: Meilleures Pratiques
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, meilleures pratiques
---

# {{ "best_practices" | i18n }}

## Espaces autour des attributs conditionnels

Parfois, les conditions sont utilisées pour ajouter des classes à une balise. djLint supprime les espaces à l'intérieur des déclarations conditionnelles.

Ce modèle est recommandé :

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">contenu</div>
                  ^ espace ici
```

{% endraw %}

Ce modèle n'est pas recommandé :

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">contenu</div>
                                     ^ espace ici
```

{% endraw %}

## `format_attribute_template_tags` et des attributs conditionnels non spatiaux

Si l'option `format_attribute_template_tags` est activée, les attributs conditionnels devraient utiliser des balises sans espace, par exemple {% raw %}`{% if a -%}`{% endraw %} dans nunjuck et jinja, pour supprimer les espaces à l'intérieur des.

djLint formatera les attributs longs sur plusieurs lignes, et l'espacement conservé à l'intérieur des attributs pourrait casser votre code.

Ce modèle est recommandé :

{% raw %}

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^ -- tags sans
espace
```

{% endraw %}

Ce modèle n'est pas recommandé :

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Après le formatage, cela pourrait ressembler à ceci :

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
