---
title: "Linter i formater szablonów Askama"
description: "djLint lintuje i formatuje szablony Askama. Ustaw profil askama, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Askama"
---

djLint lintuje i formatuje szablony Askama. Ustaw profil `askama`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Askama?](https://askama.readthedocs.io/)**

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=askama
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
