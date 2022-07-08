---
description: Конфигурация djLint для линтинга и форматирования HTML-шаблонов. Воспользуйтесь многочисленными возможностями форматирования.
title: Конфигурация
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, configuration
---

# {{ "configuration" | i18n }}

Конфигурация выполняется либо через файл `pyproject.toml` вашего проекта, либо через файл `.djlintrc`. Арги командной строки всегда будут переопределять любые настройки в `pyproject.toml`.

```ini
[tool.djlint]
<config options>
```

Формат для `.djlintrc` - `json`.

```json
{
  "вариант": "значение"
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
