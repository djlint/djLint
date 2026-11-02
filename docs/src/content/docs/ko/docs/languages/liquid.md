---
title: "Liquid 템플릿 린터 및 포맷터"
description: "djLint는 Liquid 템플릿 린터이자 Liquid 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요."
sidebar:
  label: "Liquid"
---

djLint는 Liquid 템플릿 린터이자 Liquid 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요.

**[Liquid란?](https://shopify.github.io/liquid/)**

프로필 하나로 모든 Liquid 방언을 다룹니다. Shopify 테마, Jekyll, LiquidJS(Eleventy), Fluid(Orchard Core)가 여기에 해당합니다.

#### 명령줄 사용

```bash
djlint /path/to/templates --profile=liquid
```

#### 또는 구성 파일 사용

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile="liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile="liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[모든 옵션은 구성 가이드에서 확인하세요!](/ko/docs/configuration/)
:::
