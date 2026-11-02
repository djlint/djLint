---
description: Boas práticas para usar o djLint na formatação de templates HTML.
title: Boas práticas
keywords: linter de templates, formatador de templates, djLint, HTML, templates, formatador, linter, boas práticas
---

# Boas práticas

## Espaços em torno de atributos condicionais

Às vezes, condições são usadas para adicionar classes a uma tag. O djLint remove os espaços em branco dentro de instruções condicionais.

Este padrão é recomendado:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

Este padrão não é recomendado:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` e atributos condicionais sem espaços

Se a opção `format_attribute_template_tags` estiver ativada, os atributos condicionais devem usar tags sem espaços, por exemplo {% raw %}`{% if a -%}`{% endraw %} no nunjucks e no jinja, para remover os espaços dentro da tag.

O djLint vai formatar atributos longos em várias linhas, e os espaços em branco preservados dentro dos atributos podem quebrar o seu código.

Este padrão é recomendado:

{% raw %}

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

{% endraw %}

Cada posição marcada é uma tag sem espaços.

Este padrão não é recomendado:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Depois da formatação, ficaria assim:

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
