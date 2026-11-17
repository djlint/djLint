---
title: "Linter a formátovač šablon Liquid"
description: "djLint lintuje a formátuje šablony Liquid. Nastavte profil liquid, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Liquid"
---

djLint lintuje a formátuje šablony Liquid. Nastavte profil `liquid`, aby jim pravidla i formátování odpovídaly.

**[Co je Liquid?](https://shopify.github.io/liquid/)**

Jeden profil pokrývá všechny dialekty Liquid: motivy Shopify, Jekyll, LiquidJS (Eleventy) a Fluid (Orchard Core).

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=liquid
```

## Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

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
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
