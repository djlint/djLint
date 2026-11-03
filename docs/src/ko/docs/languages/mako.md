---
title: Mako 템플릿 린터 및 포맷터
keywords: mako, python, pyramid, open edx, djlint, mako 템플릿 린터, mako 템플릿 포맷터, mako 템플릿 포맷
description: djLint는 Mako 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 mako 프로필을 설정하세요.
tool: mako
---

# {{ title }}

{{ description }}

**[Mako란?](https://www.makotemplates.org/)**

mako 프로필에서는 `% if x:` 같은 제어 줄과 `##` 주석이 항상 한 줄을 따로 차지하고, 속성이 제어 줄에 따라 달라지는 태그는 속성을 쓴 그대로 유지합니다. Python 블록과 `<%doc>`, `<%text>`의 내용은 건드리지 않으며, `--format-js`나 `--format-css`를 써도 Mako 구문이 든 script나 style은 그대로 둡니다. `% if`와 `% endif` 사이의 줄, 그리고 각각 한 줄을 따로 차지하는 `<%block>`이나 `<%def>` 태그와 그 닫는 태그 사이의 줄은 다른 블록처럼 들여씁니다. `${}` 표현식의 코드는 쓴 그대로 둡니다.

## 명령줄 사용

```bash
djlint /path/to/templates --profile={{ tool }}
```

## 또는 구성 파일 사용

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">모든 옵션은 구성 가이드에서 확인하세요!</a></div>
</div>
