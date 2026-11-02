---
description: 設定 djLint 如何 lint 與格式化 HTML 範本的選項。
title: 設定
keywords: 範本 linter, 範本格式化工具, djLint, HTML, 範本, 格式化工具, linter, 設定
date: Last Modified
---

# 設定

設定可以透過專案的 `pyproject.toml` 檔案、`djlint.toml` 或 `.djlint.toml` 檔案，或是 `.djlintrc` 檔案進行。命令列引數一律會覆寫設定檔中的任何設定。除非設定了 `--prefer-configuration`，否則專案層級的設定會覆寫以 `--configuration` 指定的全域設定檔。

`pyproject.toml` 的格式為 `toml`。

```toml
[tool.djlint]
<config options>
```

`djlint.toml` 和 `.djlint.toml` 的格式為 `toml`。

```toml
<config options>
```

`.djlintrc` 的格式為 `json`。

```json
{ "option": "value" }
```

## 選項

<div class="field">
  <label class="label">篩選選項</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="輸入文字以篩選選項…" />

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

<div id="no-matches" class="is-hidden mb-5">找不到任何結果，請試試其他搜尋。</div>

{% include 'src/_includes/tabs_script.njk' %}
