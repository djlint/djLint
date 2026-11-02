---
title: Linter a formátovač šablon Liquid
keywords: liquid, shopify, jekyll, eleventy, djlint, linter šablon liquid, formátovač šablon liquid, formátování šablon liquid, shopify, jekyll, eleventy, liquidjs, fluid, linter motivů shopify, linter pro jekyll
description: djLint je linter a formátovač šablon Liquid! Při lintování a formátování šablon pomocí djLint využijte připravený profil.
tool: liquid
---

# {{ title }}

{{ description }}

**[Co je Liquid?](https://shopify.github.io/liquid/)**

Jeden profil pokrývá všechny dialekty Liquid: motivy Shopify, Jekyll, LiquidJS (Eleventy) a Fluid (Orchard Core).

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
