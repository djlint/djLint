---
title: "Twig 템플릿 린터 및 포맷터"
description: "djLint는 twig 템플릿 린터이자 twig 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요."
sidebar:
  label: "Twig"
---

djLint는 twig 템플릿 린터이자 twig 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요.

**[Twig이란?](https://twig.symfony.com/)**

Pebble(Java) 템플릿은 Twig와 호환되므로 여기에도 같은 프로필을 사용하세요.

#### 명령줄 사용

```bash
djlint /path/to/templates --profile=nunjucks
```

#### 또는 구성 파일 사용

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[모든 옵션은 구성 가이드에서 확인하세요!](/ko/docs/configuration/)
:::
