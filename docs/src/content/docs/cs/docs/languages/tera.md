---
title: "Linter a formátovač šablon Tera"
description: "djLint lintuje a formátuje šablony Tera. Nastavte profil tera, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Tera"
---

djLint lintuje a formátuje šablony Tera. Nastavte profil `tera`, aby jim pravidla i formátování odpovídaly.

**[Co je Tera?](https://keats.github.io/tera/)**

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=tera
```

## Nebo v konfiguračním souboru

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
