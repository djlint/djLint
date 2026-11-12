---
title: "Linter a formátovač šablon Askama"
description: "djLint lintuje a formátuje šablony Askama. Nastavte profil askama, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Askama"
---

djLint lintuje a formátuje šablony Askama. Nastavte profil `askama`, aby jim pravidla i formátování odpovídaly.

**[Co je Askama?](https://askama.readthedocs.io/)**

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=askama
```

## Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
