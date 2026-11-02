---
title: Linter a formátovač šablon Nunjucks
keywords: nunjucks, djlint, linter šablon nunjucks, formátovač šablon nunjucks, formátování šablon nunjucks, pebble, linter šablon pebble
description: djLint je linter a formátovač šablon Nunjucks! Při lintování a formátování šablon pomocí djLint využijte připravený profil.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Co je Nunjucks?](https://mozilla.github.io/nunjucks/)**

Šablony Pebble (Java) jsou kompatibilní s Twigem, takže pro ně použijte stejný profil.

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
