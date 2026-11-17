---
title: "Linter a formátovač šablon Nunjucks"
description: "djLint lintuje a formátuje šablony Nunjucks. Nastavte profil nunjucks, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Nunjucks"
---

djLint lintuje a formátuje šablony Nunjucks. Nastavte profil `nunjucks`, aby jim pravidla i formátování odpovídaly.

**[Co je Nunjucks?](https://mozilla.github.io/nunjucks/)**

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=nunjucks
```

## V konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```
