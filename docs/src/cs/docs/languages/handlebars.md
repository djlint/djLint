---
title: Linter a formátovač šablon Handlebars
keywords: handlebars, djlint, linter šablon handlebars, formátovač šablon handlebars, formátování šablon handlebars
description: djLint je linter a formátovač šablon Handlebars! Při lintování a formátování šablon pomocí djLint využijte připravený profil.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Co je Handlebars?](https://handlebarsjs.com/)**

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Všechny možnosti najdete v průvodci konfigurací!</a></div>
</div>
