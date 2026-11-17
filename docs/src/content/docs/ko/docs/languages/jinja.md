---
title: "Jinja 템플릿 린터 및 포맷터"
description: "djLint는 Jinja 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 jinja 프로필을 설정하세요."
sidebar:
  label: "Jinja"
---

djLint는 Jinja 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 `jinja` 프로필을 설정하세요.

**[Jinja란?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja는 Jinja2 문법을 따르고 HubSpot의 Jinjava 템플릿도 Jinja 스타일이므로, 둘 다 `jinja` 프로필을 사용하세요.

## 명령줄 사용

```bash
djlint /path/to/templates --profile=jinja
```

## 구성 파일에서

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```
