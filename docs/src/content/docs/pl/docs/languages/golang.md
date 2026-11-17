---
title: "Linter i formater szablonów Go"
description: "djLint lintuje i formatuje szablony Go. Ustaw profil golang, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Szablony Go"
---

djLint lintuje i formatuje szablony Go. Ustaw profil `golang`, aby reguły i formatowanie były do nich dopasowane.

**[Czym są szablony Go?](https://pkg.go.dev/text/template)**

Szablony Go (`text/template`, `html/template`) napędzają też motywy Hugo i charty Helm, więc używaj dla nich tego samego profilu.

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=golang
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

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
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
