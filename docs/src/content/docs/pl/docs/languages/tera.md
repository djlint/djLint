---
title: "Linter i formater szablonów Tera"
description: "djLint to linter i formater szablonów Tera! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint."
sidebar:
  label: "Tera"
---

djLint to linter i formater szablonów Tera! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.

**[Czym jest Tera?](https://keats.github.io/tera/)**

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile=tera
```

#### Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
