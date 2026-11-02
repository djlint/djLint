---
title: "Linter i formater szablonów Handlebars"
description: "djLint to linter i formater szablonów handlebars! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint."
sidebar:
  label: "Handlebars"
---

djLint to linter i formater szablonów handlebars! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.

**[Czym jest Handlebars?](https://handlebarsjs.com/)**

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile=handlebars
```

#### Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
