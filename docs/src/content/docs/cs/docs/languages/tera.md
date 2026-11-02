---
title: "Linter a formátovač šablon Tera"
description: "djLint je linter a formátovač šablon Tera! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Tera"
---

djLint je linter a formátovač šablon Tera! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co je Tera?](https://keats.github.io/tera/)**

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=tera
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
