---
description: Configuration de djLint pour le linting et le formatage des modèles HTML. Profitez des nombreuses options de formatage.
title: Configuration
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, configuration
---

# {{ "configuration" | i18n }}

La configuration se fait soit à travers le fichier `pyproject.toml` de votre projet, soit à travers un fichier `.djlintrc`. Les arguments de la ligne de commande remplaceront toujours les paramètres du fichier `pyproject.toml`.

Le format du fichier `pyproject.toml` est `toml`.

```ini
[tool.djlint]
<options de configuration>
```

Le format du fichier `djlintrc` est `json`.

```json
{
  "option": "valeur"
}
```

{% for option in configuration %}

### {{ option.name }}

<p>{{ option.description[locale or "en"] | markdown | safe }}</p>

<div class="tabs">
<ul>

{% for flag in option.usage %}

<li class="{% if loop.index == 1 %}is-active{% endif %}"><a tab="{{- option.name | slugify -}}-{{- flag.name | slugify -}}-tab">{{ flag.name }}</a></li>

{% endfor %}

</ul>
</div>

<div class="tab-container">
{% for flag in option.usage %}
<div class="tab {% if loop.index == 1 %}is-active{% endif %}"id="{{- option.name | slugify -}}-{{- flag.name | slugify -}}-tab">

```{% if flag.name == "pyproject.toml" %}toml{% else %}json{% endif %}
{{ flag.value | safe }}
```

</div>
{% endfor %}

</div>

{% endfor %}
