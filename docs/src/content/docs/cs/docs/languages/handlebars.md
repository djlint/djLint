---
title: "Linter a formátovač šablon Handlebars"
description: "djLint je linter a formátovač šablon Handlebars! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Handlebars"
---

djLint je linter a formátovač šablon Handlebars! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co je Handlebars?](https://handlebarsjs.com/)**

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=handlebars
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
