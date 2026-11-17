---
title: "Linter i formater szablonów Nunjucks"
description: "djLint lintuje i formatuje szablony Nunjucks. Ustaw profil nunjucks, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Nunjucks"
---

djLint lintuje i formatuje szablony Nunjucks. Ustaw profil `nunjucks`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Nunjucks?](https://mozilla.github.io/nunjucks/)**

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=nunjucks
```

## W pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

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
