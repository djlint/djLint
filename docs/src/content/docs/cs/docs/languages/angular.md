---
title: "Linter šablon Angular"
description: "djLint je linter šablon Angular! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Angular"
---

djLint je linter šablon Angular! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co je Angular?](https://angular.io/guide/template-syntax)**

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=angular
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

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
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
