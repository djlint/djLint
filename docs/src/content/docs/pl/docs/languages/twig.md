---
title: "Linter i formater szablonów Twig"
description: "djLint to linter i formater szablonów twig! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint."
sidebar:
  label: "Twig"
---

djLint to linter i formater szablonów twig! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.

**[Czym jest Twig?](https://twig.symfony.com/)**

Szablony Pebble (Java) są zgodne z Twig, więc używaj dla nich tego samego profilu.

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Lub w pliku konfiguracyjnym

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
