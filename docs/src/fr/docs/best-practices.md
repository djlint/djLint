---
description: Bonnes pratiques pour formater des templates HTML avec djLint.
title: Bonnes pratiques
keywords: linter de templates, formateur de templates, djLint, HTML, templates, formateur, linter, bonnes pratiques
---

# Bonnes pratiques

## Espaces autour des attributs conditionnels

On utilise parfois des conditions pour ajouter des classes à une balise. djLint supprime les espaces à l'intérieur des instructions conditionnelles.

Cette forme est recommandée :

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

Cette forme est déconseillée :

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` et attributs conditionnels sans espaces

Si l'option `format_attribute_template_tags` est activée, les attributs conditionnels doivent utiliser des balises sans espaces, par exemple {% raw %}`{% if a -%}`{% endraw %} en nunjucks et en jinja, afin de supprimer les espaces à l'intérieur de la balise.

djLint répartit les attributs longs sur plusieurs lignes, et les espaces ainsi conservés à l'intérieur des attributs pourraient casser votre code.

Cette forme est recommandée :

{% raw %}

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

{% endraw %}

Chaque position marquée est une balise sans espaces.

Cette forme est déconseillée :

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Après formatage, on pourrait obtenir :

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
