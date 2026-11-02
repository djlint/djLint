---
title: "Django 템플릿 린터 및 포맷터"
description: "djLint는 django 템플릿 린터이자 django 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요."
sidebar:
  label: "Django"
---

djLint는 django 템플릿 린터이자 django 템플릿 포맷터입니다! djLint로 템플릿을 린트하고 포맷할 때 미리 만들어진 프로필을 활용하세요.

**[Django란?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### 명령줄 사용

```bash
djlint /path/to/templates --profile=django
```

#### 또는 구성 파일 사용

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[모든 옵션은 구성 가이드에서 확인하세요!](/ko/docs/configuration/)
:::
