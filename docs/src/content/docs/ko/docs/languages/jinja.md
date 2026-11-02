---
title: "Jinja 템플릿 린터 및 포맷터"
description: "djLint는 jinja 템플릿 린터이자 jinja 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요."
sidebar:
  label: "Jinja"
---

djLint는 jinja 템플릿 린터이자 jinja 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요.

**[Jinja란?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 템플릿은 Jinja2와 완전히 호환되므로 같은 `jinja` 프로필을 사용하세요.

HubSpot의 Jinjava 템플릿도 jinja 스타일이므로 여기에도 이 프로필을 사용하세요.

#### 명령줄 사용

```bash
djlint /path/to/templates --profile=jinja
```

#### 또는 구성 파일 사용

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

:::tip
[모든 옵션은 구성 가이드에서 확인하세요!](/ko/docs/configuration/)
:::
