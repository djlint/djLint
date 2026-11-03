---
title: Linter a formátovač šablon Mako
keywords: mako, python, pyramid, open edx, djlint, linter šablon mako, formátovač šablon mako, formátování šablon mako
description: djLint lintuje a formátuje šablony Mako. Nastavte profil mako, aby jim pravidla i formátování odpovídaly.
tool: mako
---

# {{ title }}

{{ description }}

**[Co je Mako?](https://www.makotemplates.org/)**

V profilu mako má řídicí řádek jako `% if x:` i komentář `##` vždy vlastní řádek a značka, jejíž atributy závisí na řídicích řádcích, si je ponechá tak, jak jsou napsané. Bloky Pythonu a obsah `<%doc>` a `<%text>` se nemění, stejně jako script nebo style se syntaxí Mako při `--format-js` nebo `--format-css`. Řádky mezi `% if` a `% endif` a mezi značkou `<%block>` nebo `<%def>` a její uzavírací značkou, pokud má každá vlastní řádek, se odsazují jako každý jiný blok. Kód ve výrazu `${}` zůstává tak, jak je napsaný.

## Z příkazového řádku

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Všechny možnosti najdete v průvodci konfigurací!</a></div>
</div>
