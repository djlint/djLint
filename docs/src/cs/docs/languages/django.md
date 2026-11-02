---
title: Linter a formátovač šablon Django
keywords: django, djlint, linter šablon django, formátovač šablon django, formátování šablon django
description: djLint lintuje a formátuje šablony Django. Nastavte profil django, aby jim pravidla i formátování odpovídaly.
tool: django
---

# {{ title }}

{{ description }}

**[Co je Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

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
