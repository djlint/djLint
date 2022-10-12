---
description: djLint configuration for HTML Template Linting and Formatting. Take advantage of the many formatter options.
title: Configuration
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, configuration
date: Last Modified
---

# Configuration

Configuration is done either through your projects `pyproject.toml` file, or a `.djlintrc` file. Command line args will always override any settings in `pyproject.toml`. Local project settings will always override global configuration files.

The format for `pyproject.toml` is `toml`.

```ini
[tool.djlint]
<config options>
```

The format for `.djlintrc` is `json`.

```json
{
  "option": "value"
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
