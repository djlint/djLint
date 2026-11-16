---
description: Le opzioni che configurano come djLint analizza e formatta i template HTML.
title: Configurazione
keywords: linter per template, formattatore per template, djLint, HTML, template, formattatore, linter, configurazione
date: Last Modified
---

# Configurazione

La configurazione si imposta nel file `pyproject.toml` del progetto, in un file `djlint.toml` o `.djlint.toml`, oppure in un file `.djlintrc`. Gli argomenti della riga di comando hanno sempre la precedenza su qualsiasi impostazione dei file di configurazione. Le impostazioni locali del progetto hanno la precedenza su un file di configurazione globale indicato con `--configuration`, a meno che non sia impostato `--prefer-configuration`.

djLint cerca questi file risalendo dal primo percorso che controlla (con `-`, dalla cartella di `--stdin-filename`, o dalla directory corrente se manca). Si ferma alla prima cartella che contiene un `djlint.toml`, un `.djlint.toml`, un `.djlintrc`, un `.djlint_rules.yaml` o un `pyproject.toml` con `[tool.djlint]`, e non va mai oltre la radice di un repository (una cartella con una cartella o un file `.git`, o una cartella `.hg`). Un `pyproject.toml` senza impostazioni di djLint non la ferma, quindi un pacchetto di un monorepo con il proprio `pyproject.toml` riceve le impostazioni del repository. djLint legge solo la cartella in cui si ferma: `[tool.djlint]` nel suo `pyproject.toml` se la tabella imposta qualcosa, altrimenti il suo `djlint.toml` o `.djlint.toml`, altrimenti il suo `.djlintrc`, e avvisa di quelli presenti lì che non legge.

Quando né la riga di comando né la configurazione impostano `indent` o `max_line_length`, djLint prende `indent_size` o `max_line_length` dai file `.editorconfig`, come fanno gli editor: ogni file li riceve in base al proprio percorso, vince il `.editorconfig` più vicino e quelli sopra completano il resto, fino a uno con `root = true` o alla radice del progetto.

Il formato di `pyproject.toml` è `toml`.

```toml
[tool.djlint]
<config options>
```

Il formato di `djlint.toml` e `.djlint.toml` è `toml`.

```toml
<config options>
```

Il formato di `.djlintrc` è `json`.

```json
{ "option": "value" }
```

## Opzioni

<div class="field">
  <label class="label">Filtra le opzioni</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="digita per filtrare le opzioni..." />

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

<div id="no-matches" class="is-hidden mb-5">Nessun risultato. Prova con un'altra ricerca.</div>

{% include 'src/_includes/tabs_script.njk' %}
