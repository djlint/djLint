---
title: "Utilisation du formateur"
description: "Formatez vos modèles HTML avec djLint. Rapide et précis, le résultat fera briller vos modèles."
sidebar:
  label: "Formateur"
---

Le formateur de djLint prendra des modèles html bâclés et rendra le formatage cohérent et facile à suivre !

Vérifiez la sortie avec `--check` avant d'appliquer les changements.

Pour revoir ce qui peut changer dans le formatage, lancez :

```bash
djlint . --check
```

Pour formater le code et exécuter les fichiers de mise à jour :

```bash
djlint . --reformat --single-attribute-per-line

# et si on formatait aussi les scripts et les styles ?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::

:::note[Note]
Le JSON et le JavaScript écrits dans un attribut sont laissés tels quels, sauf si `--format-attribute-js-json` est activé. Le HTML dans un attribut n'est jamais touché.
:::

:::note[Note]
djLint n'est pas un analyseur html ou un validateur de syntaxe.
:::

## Voici un exemple !

### Avant

Voilà un pâté de HTML qui a désespérément besoin d’attention...

<!-- prettier-ignore -->
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

C'est un peu mieux maintenant... on peut le lire :)

<!-- prettier-ignore -->
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

### Après avec `single_attribute_per_line`

Vous préférez les attributs à la manière de Prettier ? Activez l'option `single_attribute_per_line` :

<!-- prettier-ignore -->
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
