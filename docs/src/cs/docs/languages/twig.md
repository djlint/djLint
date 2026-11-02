---
title: Linter a formátovač šablon Twig
keywords: twig, djlint, linter šablon twig, formátovač šablon twig, formátování šablon twig, pebble, linter šablon pebble
description: djLint lintuje a formátuje šablony Twig. Nastavte profil nunjucks, aby jim pravidla i formátování odpovídaly.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Co je Twig?](https://twig.symfony.com/)**

Šablony Pebble (Java) jsou kompatibilní s Twigem, takže pro ně použijte stejný profil.

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
