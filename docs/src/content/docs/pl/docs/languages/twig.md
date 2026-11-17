---
title: "Linter i formater szablonów Twig"
description: "djLint lintuje i formatuje szablony Twig. Ustaw profil nunjucks, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Twig"
---

djLint lintuje i formatuje szablony Twig. Ustaw profil `nunjucks`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Twig?](https://twig.symfony.com/)**

Szablony Pebble (Java) są zgodne z Twig, więc używaj dla nich tego samego profilu.

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=nunjucks
```

## Lub w pliku konfiguracyjnym

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

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
