---
title: Linter a formátovač šablon Mustache
keywords: mustache, djlint, linter šablon mustache, formátovač šablon mustache, formátování šablon mustache
description: djLint lintuje a formátuje šablony Mustache. Nastavte profil handlebars, aby jim pravidla i formátování odpovídaly.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Co je Mustache?](https://mustache.github.io/mustache.5.html)**

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
