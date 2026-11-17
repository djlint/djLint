---
title: "Nunjucks 템플릿 린터 및 포맷터"
description: "djLint는 Nunjucks 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 nunjucks 프로필을 설정하세요."
sidebar:
  label: "Nunjucks"
---

djLint는 Nunjucks 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 `nunjucks` 프로필을 설정하세요.

**[Nunjucks란?](https://mozilla.github.io/nunjucks/)**

## 명령줄 사용

```bash
djlint /path/to/templates --profile=nunjucks
```

## 구성 파일에서

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```
