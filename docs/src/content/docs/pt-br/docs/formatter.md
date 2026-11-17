---
title: "Uso do formatador"
description: "Como o djLint formata templates HTML e como conferir as alterações antes de aplicá-las."
sidebar:
  label: "Formatador"
---

O formatador do djLint pega templates HTML desleixados e deixa a formatação consistente e fácil de acompanhar!

Revise a saída com `--check` antes de aplicar as alterações.

Para revisar o que pode mudar na formatação, execute:

```bash
djlint . --check --single-attribute-per-line
```

Para formatar o código e atualizar os arquivos, execute:

```bash
djlint . --reformat --single-attribute-per-line

# e que tal formatar scripts e estilos?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Confira o guia de configuração para ver todas as opções!](/pt-br/docs/configuration/)
:::

:::note[Observação]
JSON e JavaScript escritos em um atributo são mantidos como estão, a menos que `--format-attribute-js-json` esteja ativado. HTML dentro de um atributo nunca é alterado.
:::

:::note[Observação]
O djLint não é um parser de HTML nem um validador de sintaxe.
:::

## Veja um exemplo!

### Antes

Aqui está um bloco de HTML que precisa urgentemente de atenção -

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
{% if pagination_required %}
{% for i in page_range %}
{% paginator_number cl i %}
{% endfor %}
{% endif %}
{{ cl.result_count }}
{% if cl.result_count == 1 %}
{{ cl.opts.verbose_name }}
{% else %}
{{ cl.opts.verbose_name_plural }}
{% endif %}
{% if show_all_url %}
<a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}</a>
{% endif %}
{% if cl.formset and cl.result_count %}
<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">
{% endif %}
</p>
```

### Depois

Agora está um pouco melhor... dá para ler :)

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input type="submit"
               name="_save"
               class="default"
               value="{% translate 'Save' %}">
    {% endif %}
</p>
```

### Depois, com `single_attribute_per_line`

Prefere atributos no estilo do Prettier? Ative a opção `single_attribute_per_line`:

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input
            type="submit"
            name="_save"
            class="default"
            value="{% translate 'Save' %}"
        >
    {% endif %}
</p>
```
