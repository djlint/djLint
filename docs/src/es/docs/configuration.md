---
description: Las opciones que configuran cómo djLint analiza y formatea las plantillas HTML.
title: Configuración
keywords: linter de plantillas, formateador de plantillas, djLint, HTML, plantillas, formateador, linter, configuración
date: Last Modified
---

# Configuración

La configuración se hace a través del archivo `pyproject.toml` de tu proyecto, de un archivo `djlint.toml` o `.djlint.toml`, o de un archivo `.djlintrc`. Los argumentos de la línea de comandos siempre prevalecen sobre cualquier ajuste de los archivos de configuración. Los ajustes locales del proyecto prevalecen sobre un archivo de configuración global indicado con `--configuration`, salvo que se use `--prefer-configuration`.

djLint busca estos archivos hacia arriba a partir de la primera ruta que revisa (con `-`, desde la carpeta de `--stdin-filename`, o desde el directorio actual si no se indica). Se detiene en la primera carpeta que contiene un `djlint.toml`, un `.djlint.toml`, un `.djlintrc`, un `.djlint_rules.yaml` o un `pyproject.toml` con `[tool.djlint]`, y nunca pasa de la raíz de un repositorio (una carpeta con una carpeta o un archivo `.git`, o una carpeta `.hg`). Un `pyproject.toml` sin ajustes de djLint no la detiene, así que un paquete de un monorepo con su propio `pyproject.toml` recibe los ajustes del repositorio. djLint solo lee la carpeta donde se detiene: `[tool.djlint]` en su `pyproject.toml` si esa tabla define algo; si no, su `djlint.toml` o `.djlint.toml`; si no, su `.djlintrc`, y avisa de los que hay ahí y no lee.

Cuando ni la línea de comandos ni la configuración fijan `indent` o `max_line_length`, djLint toma `indent_size` o `max_line_length` de los archivos `.editorconfig`, como hacen los editores: cada archivo los recibe según su propia ruta, gana el `.editorconfig` más cercano y los de más arriba completan lo que falta, hasta uno con `root = true` o la raíz del proyecto.

El formato de `pyproject.toml` es `toml`.

```toml
[tool.djlint]
<config options>
```

El formato de `djlint.toml` y `.djlint.toml` es `toml`.

```toml
<config options>
```

El formato de `.djlintrc` es `json`.

```json
{ "option": "value" }
```

## Opciones

<div class="field">
  <label class="label">Filtrar opciones</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="escribe para filtrar las opciones..." />

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
// The text of every value, so a quote typed in the search matches a quote in an option.
var searchText = (value) => typeof value === 'string' ? value : Object.values(value ?? {}).map(searchText).join(' ');
document.querySelector('#filter').addEventListener('input', (event) => {
    document.querySelector('#no-matches').classList.add('is-hidden');
      if (event.target.value === ''){
        showAll()
      } else {
        var regex = new RegExp(event.target.value.replaceAll(/[.*+?^${}()|[\]\\]/g, '\\$&').replaceAll(' ', '.*[ _-].*'), 'gmi'),
        matches=[]
        search_data.forEach((obj) => {
        if (searchText(obj).match(regex)) {
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

<div id="no-matches" class="is-hidden mb-5">No se encontró nada. Prueba con otra búsqueda.</div>

{% include 'src/_includes/tabs_script.njk' %}
