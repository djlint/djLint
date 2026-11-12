---
title: "Go 템플릿 린터 및 포맷터"
description: "djLint는 Go 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 golang 프로필을 설정하세요."
sidebar:
  label: "Go 템플릿"
---

djLint는 Go 템플릿을 린트하고 포맷합니다. 규칙과 포맷이 템플릿에 맞도록 `golang` 프로필을 설정하세요.

**[Go 템플릿이란?](https://pkg.go.dev/text/template)**

Hugo 테마와 Helm 차트도 Go 템플릿(`text/template`, `html/template`)으로 만들어지므로, 여기에도 같은 프로필을 사용하세요.

## 명령줄 사용

```bash
djlint /path/to/templates --profile=golang
```

## 또는 구성 파일 사용

프로젝트의 `pyproject.toml`, `djlint.toml` / `.djlint.toml`, `.djlintrc` 파일 중 하나에서 djLint를 구성합니다.

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[모든 옵션은 구성 가이드에서 확인하세요!](/ko/docs/configuration/)
:::
