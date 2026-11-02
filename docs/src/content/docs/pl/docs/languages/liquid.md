---
title: "Linter i formater szablonów Liquid"
description: "djLint to linter i formater szablonów Liquid! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint."
sidebar:
  label: "Liquid"
---

djLint to linter i formater szablonów Liquid! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.

**[Czym jest Liquid?](https://shopify.github.io/liquid/)**

Jeden profil obejmuje wszystkie dialekty Liquid: motywy Shopify, Jekyll, LiquidJS (Eleventy) i Fluid (Orchard Core).

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile=liquid
```

#### Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile="liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile="liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
