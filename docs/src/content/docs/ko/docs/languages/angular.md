---
title: "Angular 템플릿 린터"
description: "djLint는 Angular 템플릿 린터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요."
sidebar:
  label: "Angular"
---

djLint는 Angular 템플릿 린터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요.

**[Angular란?](https://angular.io/guide/template-syntax)**

#### 명령줄 사용

```bash
djlint /path/to/templates --profile=angular
```

#### 또는 구성 파일 사용

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile="angular"
```

```toml title="djlint.toml / .djlint.toml"
profile="angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[모든 옵션은 구성 가이드에서 확인하세요!](/ko/docs/configuration/)
:::
