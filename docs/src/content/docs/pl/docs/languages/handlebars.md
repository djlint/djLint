---
title: "Linter i formater szablonów Handlebars"
description: "djLint lintuje i formatuje szablony Handlebars. Ustaw profil handlebars, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Handlebars"
---

djLint lintuje i formatuje szablony Handlebars. Ustaw profil `handlebars`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Handlebars?](https://handlebarsjs.com/)**

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=handlebars
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
