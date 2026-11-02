---
title: Liquid 템플릿 린터 및 포맷터
keywords: liquid, shopify, jekyll, eleventy, djlint, liquid 템플릿 린터, liquid 템플릿 포맷터, liquid 템플릿 포맷, shopify, jekyll, eleventy, liquidjs, fluid, shopify 테마 린터, jekyll 린터
description: djLint는 Liquid 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 liquid 프로필을 설정하세요.
tool: liquid
---

# {{ title }}

{{ description }}

**[Liquid란?](https://shopify.github.io/liquid/)**

프로필 하나로 Shopify 테마, Jekyll, LiquidJS(Eleventy), Fluid(Orchard Core)까지 모든 Liquid 방언을 다룹니다.

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
