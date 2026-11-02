---
description: djLint'in HTML şablonlarını nasıl denetleyip biçimlendireceğini belirleyen seçenekler.
title: Yapılandırma
keywords: şablon linter'ı, şablon biçimlendiricisi, djLint, HTML, şablonlar, biçimlendirici, linter, yapılandırma
date: Last Modified
---

# Yapılandırma

Yapılandırma, projenizin `pyproject.toml` dosyası, bir `djlint.toml` ya da `.djlint.toml` dosyası veya bir `.djlintrc` dosyası üzerinden yapılır. Komut satırı argümanları, yapılandırma dosyalarındaki ayarları her zaman geçersiz kılar. `--prefer-configuration` ayarlanmadıkça yerel proje ayarları, `--configuration` ile verilen genel bir yapılandırma dosyasını geçersiz kılar.

`pyproject.toml` dosyası `toml` biçimindedir.

```toml
[tool.djlint]
<config options>
```

`djlint.toml` ve `.djlint.toml` dosyaları `toml` biçimindedir.

```toml
<config options>
```

`.djlintrc` dosyası `json` biçimindedir.

```json
{ "option": "value" }
```

## Seçenekler

<div class="field">
  <label class="label">Seçenekleri filtrele</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="seçenekleri filtrelemek için yazın..." />

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

<div id="no-matches" class="is-hidden mb-5">Hiçbir şey bulunamadı. Başka bir arama deneyin.</div>

{% include 'src/_includes/tabs_script.njk' %}
