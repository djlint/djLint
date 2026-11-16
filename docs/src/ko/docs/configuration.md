---
description: djLint가 HTML 템플릿을 린트하고 포맷하는 방식을 정하는 옵션입니다.
title: 구성
keywords: 템플릿 린터, 템플릿 포맷터, djLint, HTML, 템플릿, 포맷터, 린터, 구성
date: Last Modified
---

# 구성

구성은 프로젝트의 `pyproject.toml` 파일, `djlint.toml` 또는 `.djlint.toml` 파일, `.djlintrc` 파일 중 하나로 합니다. 명령줄 인수는 언제나 구성 파일의 모든 설정보다 우선합니다. `--prefer-configuration`을 지정하지 않는 한, 로컬 프로젝트 설정은 `--configuration`으로 지정한 전역 구성 파일보다 우선합니다.

djLint는 처음 검사하는 경로(`-`이면 `--stdin-filename`의 폴더, 이 옵션이 없으면 현재 디렉터리)에서 위쪽으로 이 파일들을 찾습니다. `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml` 또는 `[tool.djlint]`가 있는 `pyproject.toml` 중 하나가 있는 첫 폴더에서 멈추며, 저장소의 루트(`.git` 폴더나 파일, 또는 `.hg` 폴더가 있는 폴더)보다 위로는 가지 않습니다. djLint 설정이 없는 `pyproject.toml`에서는 멈추지 않으므로, 자체 `pyproject.toml`이 있는 모노레포의 패키지도 저장소의 설정을 받습니다. djLint는 멈춘 폴더만 읽습니다. `pyproject.toml`의 `[tool.djlint]`에 설정이 있으면 그것을 읽고, 없으면 `djlint.toml`이나 `.djlint.toml`을, 그것도 없으면 `.djlintrc`를 읽으며, 그 폴더에 있지만 읽지 않는 파일은 경고로 알려 줍니다.

명령줄과 구성 어디에서도 `indent`나 `max_line_length`를 설정하지 않으면, djLint는 편집기처럼 `.editorconfig` 파일에서 `indent_size`나 `max_line_length`를 가져옵니다. 각 파일은 자신의 경로에 따라 값을 받고, 가장 가까운 `.editorconfig`가 우선하며 위쪽 파일들이 빠진 값을 채웁니다. 검색은 `root = true`가 있는 파일이나 프로젝트 루트에서 끝납니다.

`pyproject.toml`의 형식은 `toml`입니다.

```toml
[tool.djlint]
<config options>
```

`djlint.toml`과 `.djlint.toml`의 형식은 `toml`입니다.

```toml
<config options>
```

`.djlintrc`의 형식은 `json`입니다.

```json
{ "option": "value" }
```

## 옵션

<div class="field">
  <label class="label">옵션 필터</label>
  <div class="control">
    <input id="filter" class="input" type="text" placeholder="옵션을 필터링하려면 입력하세요..." />

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

<div id="no-matches" class="is-hidden mb-5">찾은 항목이 없습니다. 다른 검색어를 입력해 보세요.</div>

{% include 'src/_includes/tabs_script.njk' %}
