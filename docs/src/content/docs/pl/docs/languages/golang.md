---
title: "Linter i formater szablonów Go"
description: "djLint to linter i formater szablonów Go! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint."
sidebar:
  label: "Szablony Go"
---

djLint to linter i formater szablonów Go! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.

**[Czym są szablony Go?](https://pkg.go.dev/text/template)**

Szablony Go (`text/template`, `html/template`) napędzają też motywy Hugo i charty Helm, więc używaj dla nich tego samego profilu.

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile=golang
```

#### Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile="golang"
```

```toml title="djlint.toml / .djlint.toml"
profile="golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
