---
title: Twig 템플릿 린터 및 포맷터
keywords: twig, djlint, twig 템플릿 린터, twig 템플릿 포맷터, twig 템플릿 포맷, pebble, pebble 템플릿 린터
description: djLint는 Twig 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 nunjucks 프로필을 설정하세요.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Twig란?](https://twig.symfony.com/)**

Pebble(Java) 템플릿은 Twig와 호환되므로 여기에도 같은 프로필을 사용하세요.

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
