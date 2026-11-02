---
title: "Linter i formater szablonów Liquid"
description: "djLint lintuje i formatuje szablony Liquid. Ustaw profil liquid, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Liquid"
---

djLint lintuje i formatuje szablony Liquid. Ustaw profil `liquid`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Liquid?](https://shopify.github.io/liquid/)**

Jeden profil obejmuje wszystkie dialekty Liquid: motywy Shopify, Jekyll, LiquidJS (Eleventy) i Fluid (Orchard Core).

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=liquid
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
