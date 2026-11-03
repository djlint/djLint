---
title: "Linter szablonów Angular"
description: "djLint lintuje szablony Angular. Ustaw profil angular, aby reguły były do nich dopasowane."
sidebar:
  label: "Angular"
---

djLint lintuje szablony Angular. Ustaw profil `angular`, aby reguły były do nich dopasowane.

**[Czym jest Angular?](https://angular.io/guide/template-syntax)**

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=angular
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
