---
description: As opções que configuram como o djLint faz o lint e formata templates HTML.
title: Configuração
keywords: linter de templates, formatador de templates, djLint, HTML, templates, formatador, linter, configuração
date: Last Modified
---

# Configuração

A configuração é feita pelo arquivo `pyproject.toml` do seu projeto, por um arquivo `djlint.toml` ou `.djlint.toml`, ou por um arquivo `.djlintrc`. Os argumentos da linha de comando sempre têm prioridade sobre as configurações dos arquivos de configuração. As configurações locais do projeto têm prioridade sobre um arquivo de configuração global informado com `--configuration`, a menos que `--prefer-configuration` esteja definido.

O djLint procura esses arquivos subindo a partir do primeiro caminho que verifica (com `-`, a partir da pasta de `--stdin-filename`, ou do diretório atual sem essa opção). Ele para na primeira pasta que tem um `djlint.toml`, um `.djlint.toml`, um `.djlintrc`, um `.djlint_rules.yaml` ou um `pyproject.toml` com `[tool.djlint]`, e nunca passa da raiz de um repositório (uma pasta com uma pasta ou um arquivo `.git`, ou uma pasta `.hg`). Um `pyproject.toml` sem configurações do djLint não interrompe a busca, então um pacote de um monorepo com o próprio `pyproject.toml` recebe as configurações do repositório. O djLint lê só a pasta onde para: `[tool.djlint]` no `pyproject.toml` dela, se essa tabela definir algo; se não, o `djlint.toml` ou `.djlint.toml`; se não, o `.djlintrc`, e avisa sobre os que estão lá e não são lidos.

Quando nem a linha de comando nem a configuração definem `indent` ou `max_line_length`, o djLint pega `indent_size` ou `max_line_length` dos arquivos `.editorconfig`, como os editores fazem: cada arquivo recebe esses valores pelo próprio caminho, o `.editorconfig` mais próximo vence e os de cima completam o resto, até um com `root = true` ou a raiz do projeto.

O formato do `pyproject.toml` é `toml`.

```toml
[tool.djlint]
<config options>
```

O formato do `djlint.toml` e do `.djlint.toml` é `toml`.

```toml
<config options>
```

O formato do `.djlintrc` é `json`.

```json
{ "option": "value" }
```

## Opções

<div class="field">
  <label class="label">Filtrar opções</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="digite para filtrar as opções..." />

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

<div id="no-matches" class="is-hidden mb-5">Nada encontrado. Tente outra busca.</div>

{% include 'src/_includes/tabs_script.njk' %}
