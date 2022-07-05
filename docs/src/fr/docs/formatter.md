---
description: Formatez vos modèles HTML avec djLint. Rapide et précis, le résultat fera briller vos modèles.
title: Utilisation du formateur
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, formatter usage
---

# Utilisation du formateur

Le formateur de djLint prendra des modèles html bâclés et rendra le formatage cohérent et facile à suivre !

Le formatage est un outil non définitif. Vérifiez la sortie avant d'appliquer les changements.

Pour revoir ce qui peut changer dans le formatage, lancez :

```bash
djlint . --check
```

Pour formater le code et exécuter les fichiers de mise à jour :

```bash
djlint . --reformat
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/fr/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>

{% admonition
   "note",
   "Note",
   "Le reformatage ne fonctionne pas avec les longs fichiers json/html intégrés dans les données d'attribut."
%}

{% admonition
   "note",
   "Note",
   "djLint n'est pas un analyseur html ou un validateur de syntaxe."
%}


## Voici un exemple !

### Avant

Voilà un pâté de HTML qui a désespérément besoin d’attention...

{% raw %}

```
{% load admin_list %}{% load i18n %}<p class="paginator">{% if pagination_required %}{% for i in page_range %}{% paginator_number cl i %}{% endfor %}{% endif %}{{ cl.result_count }}{% if cl.result_count == 1 %}{{ cl.opts.verbose_name }}   {% else %}{{ cl.opts.verbose_name_plural }}       {% endif %}{% if show_all_url %} <a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}          </a>  {% endif %}{% if cl.formset and cl.result_count %}<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">{% endif %}      </p>
```

{% endraw %}

### Après

C'est un peu mieux maintenant... on peut le lire :)

{% raw %}

```html
{% load admin_list %} {% load i18n %}
<p class="paginator">
  {% if pagination_required %} {% for i in page_range %} {% paginator_number cl
  i %} {% endfor %} {% endif %} {{ cl.result_count }} {% if cl.result_count == 1
  %} {{ cl.opts.verbose_name }} {% else %} {{ cl.opts.verbose_name_plural }} {%
  endif %} {% if show_all_url %}
  <a href="{{ show_all_url }}" class="showall"> {% translate 'Show all' %} </a>
  {% endif %} {% if cl.formset and cl.result_count %}
  <input
    type="submit"
    name="_save"
    class="default"
    value="{% translate 'Save' %}"
  />
  {% endif %}
</p>
```

{% endraw %}
