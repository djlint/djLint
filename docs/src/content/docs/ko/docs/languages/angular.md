---
title: "Angular 템플릿 린터"
description: "djLint는 Angular 템플릿을 린트합니다. 규칙이 템플릿에 맞도록 angular 프로필을 설정하세요."
sidebar:
  label: "Angular"
---

djLint는 Angular 템플릿을 린트합니다. 규칙이 템플릿에 맞도록 `angular` 프로필을 설정하세요.

**[Angular란?](https://angular.dev/guide/templates)**

## 명령줄 사용

```bash
djlint /path/to/templates --profile=angular
```

## 구성 파일에서

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```
