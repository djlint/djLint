---
title: "Linter a formátovač šablon Liquid"
description: "djLint je linter a formátovač šablon Liquid! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Liquid"
---

djLint je linter a formátovač šablon Liquid! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co je Liquid?](https://shopify.github.io/liquid/)**

Jeden profil pokrývá všechny dialekty Liquid: motivy Shopify, Jekyll, LiquidJS (Eleventy) a Fluid (Orchard Core).

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=liquid
```

#### Nebo v konfiguračním souboru

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
