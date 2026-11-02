---
title: "Boas práticas"
description: "Boas práticas para usar o djLint na formatação de templates HTML."
sidebar:
  label: "Boas práticas"
---

## Espaços em torno de atributos condicionais

Às vezes, condições são usadas para adicionar classes a uma tag. O djLint remove os espaços em branco dentro de instruções condicionais.

Este padrão é recomendado:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

Este padrão não é recomendado:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` e atributos condicionais sem espaços

Se a opção `format_attribute_template_tags` estiver ativada, os atributos condicionais devem usar tags sem espaços, por exemplo `{% if a -%}` no nunjucks e no jinja, para remover os espaços dentro da tag.

O djLint vai formatar atributos longos em várias linhas, e os espaços em branco preservados dentro dos atributos podem quebrar o seu código.

Este padrão é recomendado:

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

Cada posição marcada é uma tag sem espaços.

Este padrão não é recomendado:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Depois da formatação, ficaria assim:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
