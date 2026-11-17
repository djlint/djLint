---
title: "Linter a formátovač šablon Mustache"
description: "djLint lintuje a formátuje šablony Mustache. Nastavte profil handlebars, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Mustache"
---

djLint lintuje a formátuje šablony Mustache. Nastavte profil `handlebars`, aby jim pravidla i formátování odpovídaly.

**[Co je Mustache?](https://mustache.github.io/mustache.5.html)**

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=handlebars
```

## Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
