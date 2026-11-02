---
title: Angular 템플릿 린터
keywords: angular, djlint, angular 템플릿 린터, angular 템플릿 린트
description: djLint는 Angular 템플릿을 린트합니다. 규칙이 템플릿에 맞도록 angular 프로필을 설정하세요.
tool: angular
---

# {{ title }}

{{ description }}

**[Angular란?](https://angular.io/guide/template-syntax)**

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
