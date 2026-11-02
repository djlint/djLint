---
description: Конфигурация djLint для проверки и форматирования HTML-шаблонов. Пользуйтесь множеством параметров форматера.
title: Конфигурация
keywords: линтер шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, конфигурация
date: Last Modified
---

# Конфигурация

Настройка выполняется через файл `pyproject.toml` вашего проекта, файл `djlint.toml` или `.djlint.toml` либо файл `.djlintrc`. Аргументы командной строки всегда переопределяют настройки из файлов конфигурации. Локальные настройки проекта переопределяют глобальный файл конфигурации, заданный через `--configuration`, если не указан `--prefer-configuration`.

Файл `pyproject.toml` записывается в формате `toml`.

```toml
[tool.djlint]
<config options>
```

Файлы `djlint.toml` и `.djlint.toml` записываются в формате `toml`.

```toml
<config options>
```

Файл `.djlintrc` записывается в формате `json`.

```json
{ "option": "value" }
```

## Параметры

<div class="field">
  <label class="label">Фильтр параметров</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="введите текст для фильтрации параметров..." />

  </div>
</div>
<script>
const hideAll=() => {
    (document.querySelectorAll('.option') || []).forEach((x) => {
                x.classList.add('is-hidden')
        })
}
const showAll=() => {
    (document.querySelectorAll('.option') || []).forEach((x) => {
                x.classList.remove('is-hidden')
        })
}
var search_data = {{ configuration | dump | safe }};
document.querySelector('#filter').addEventListener('input', (event) => {
    document.querySelector('#no-matches').classList.add('is-hidden');
      if (event.target.value === ''){
        showAll()
      } else {
        var regex = new RegExp(event.target.value.replaceAll(' ', '.*[ _-].*'), 'gmi'),
        matches=[]
        search_data.forEach((obj) => {
        if (JSON.stringify(obj).match(regex)) {
            matches.push(obj.name)
        }
        if(matches.length > 0){
             document.querySelector('#no-matches').classList.add('is-hidden');
        (document.querySelectorAll('.option') || []).forEach((x) => {
            if (matches.includes(x.getAttribute('data-name'))){
                x.classList.remove('is-hidden')
            }
            else {
                x.classList.add('is-hidden')
            }
        })} else {
            hideAll();
            document.querySelector('#no-matches').classList.remove('is-hidden');
        }
        })
        }
    })
    </script>
<hr />

{% for option in configuration | sort(false, false, "name") %}

<div class="option p-3 my-3 is-rounded" data-name="{{option.name}}">
<div class="is-flex is-justify-content-space-between">
    <h3 class="title is-3" id="{{ option.name | slugify }}">
        <a class="link bn" href="#{{ option.name | slugify }}" aria-hidden="true" tabindex="-1">#</a> {{ option.name }}</h3>
    <div class="tags option-tags"><span class="tag is-family-sans-serif has-text-weight-medium">{{ "since" | i18n }} {{ option.since }}</span>{% for tag in option.tags %}<span class="tag is-family-sans-serif is-link has-text-weight-medium">{{ tag }}</span>{% endfor %}</div></div>

{{ option.description[locale or "en"] | markdown | safe }}

<div class="tabs">
<ul>

{% for flag in option.usage %}

<li{% if loop.index == 1 %} class="is-active"{% endif %}><a tab="{{- flag.name | slugify -}}-tab">{{ flag.name }}</a></li>
{% if flag.name == "pyproject.toml" %}
<li><a tab="djlint-toml-tab">djlint.toml / .djlint.toml</a></li>
{% endif %}

{% endfor %}

</ul>
</div>

<div class="tab-container">
{% for flag in option.usage %}
<div class="tab {% if loop.index == 1 %}is-active{% endif %}"id="{{- flag.name | slugify -}}-tab">

```{% if flag.name == "pyproject.toml" %}toml{% else %}json{% endif %}
{{ flag.value | safe }}
```

</div>
{% if flag.name == "pyproject.toml" %}
<div class="tab"id="djlint-toml-tab">

```toml
{{ flag.value | djlintTomlConfig | safe }}
```

</div>
{% endif %}
{% endfor %}

</div></div>

{% endfor %}

<div id="no-matches" class="is-hidden mb-5">Ничего не найдено. Попробуйте другой запрос.</div>

{% include 'src/_includes/tabs_script.njk' %}
