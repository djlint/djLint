---
title: "Linter a formátovač šablon Mako"
description: "djLint lintuje a formátuje šablony Mako. Nastavte profil mako, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Mako"
---

djLint lintuje a formátuje šablony Mako. Nastavte profil `mako`, aby jim pravidla i formátování odpovídaly.

**[Co je Mako?](https://www.makotemplates.org/)**

V profilu mako má řídicí řádek jako `% if x:` i komentář `##` vždy vlastní řádek a značka, jejíž atributy závisí na řídicích řádcích, si je ponechá tak, jak jsou napsané. Bloky Pythonu a obsah `<%doc>` a `<%text>` se nemění, stejně jako script nebo style se syntaxí Mako při `--format-js` nebo `--format-css`. Řádky mezi `% if` a `% endif` a mezi značkou `<%block>` nebo `<%def>` a její uzavírací značkou, pokud má každá vlastní řádek, se odsazují jako každý jiný blok. Kód ve výrazu `${}` zůstává tak, jak je napsaný.

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=mako
```

## Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
