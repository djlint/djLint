---
title: Tera 템플릿 린터 및 포맷터
keywords: tera, rust, zola, djlint, tera 템플릿 린터, tera 템플릿 포맷터, tera 템플릿 포맷
description: djLint는 Tera 템플릿 린터이자 Tera 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요.
tool: tera
---

# {{ title }}

{{ description }}

**[Tera란?](https://keats.github.io/tera/)**

#### 명령줄 사용

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### 또는 구성 파일 사용

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">모든 옵션은 구성 가이드에서 확인하세요!</a></div>
</div>
