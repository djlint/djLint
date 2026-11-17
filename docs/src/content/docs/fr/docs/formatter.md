---
title: "Utilisation du formateur"
description: "Comment djLint formate les templates HTML, et comment vérifier les modifications avant de les appliquer."
sidebar:
  label: "Formateur"
---

Le formateur de djLint rend la mise en page des templates HTML cohérente. Regardez d'abord ce qu'il changerait :

```bash
djlint . --check --format-css --format-js
```

Formatez ensuite les fichiers sur place, ici avec le contenu de `<style>` et `<script>` aussi :

```bash
djlint . --reformat --format-css --format-js
```

:::note[Remarque]
Le JSON et le JavaScript écrits dans un attribut sont laissés tels quels, sauf si `--format-attribute-js-json` est activé. Le HTML à l'intérieur d'un attribut n'est jamais modifié.
:::

:::note[Remarque]
djLint n'est ni un parseur HTML ni un validateur de syntaxe.
:::

## Exemple

### Avant

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

### Après

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

### Après, avec `single_attribute_per_line`

Vous préférez les attributs à la Prettier ? Activez l'option `single_attribute_per_line` :

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
