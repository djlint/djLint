---
title: Linter a formátovač šablon Tera
keywords: tera, rust, zola, djlint, linter šablon tera, formátovač šablon tera, formátování šablon tera
description: djLint je linter a formátovač šablon Tera! Při lintování a formátování šablon pomocí djLint využijte připravený profil.
tool: tera
---

# {{ title }}

{{ description }}

**[Co je Tera?](https://keats.github.io/tera/)**

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
