---
title: "Utilisation du formateur"
description: "Formatez vos templates HTML avec djLint. Rapide et précis, il rendra vos templates impeccables."
sidebar:
  label: "Formateur"
---

Le formateur de djLint prend des templates HTML négligés et leur donne une mise en forme cohérente et facile à suivre !

Vérifiez le résultat avec `--check` avant d'appliquer les modifications.

Pour voir ce que le formatage pourrait modifier, exécutez :

```bash
djlint . --check
```

Pour formater le code et mettre à jour les fichiers, exécutez :

```bash
djlint . --reformat --single-attribute-per-line

# et si on formatait aussi les scripts et les styles ?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::

:::note[Remarque]
Le JSON et le JavaScript écrits dans un attribut sont laissés tels quels, sauf si `--format-attribute-js-json` est activé. Le HTML à l'intérieur d'un attribut n'est jamais modifié.
:::

:::note[Remarque]
djLint n'est ni un parseur HTML ni un validateur de syntaxe.
:::

## Un exemple !

### Avant

Voici un bloc de HTML qui a désespérément besoin d'attention :

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

C'est un peu mieux maintenant… on arrive à le lire :)

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
