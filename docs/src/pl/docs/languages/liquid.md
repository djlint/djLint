---
title: Linter i formater szablonów Liquid
keywords: liquid, shopify, jekyll, eleventy, djlint, linter szablonów liquid, formater szablonów liquid, formatowanie szablonów liquid, shopify, jekyll, eleventy, liquidjs, fluid, linter motywów shopify, linter jekyll
description: djLint lintuje i formatuje szablony Liquid. Ustaw profil liquid, aby reguły i formatowanie były do nich dopasowane.
tool: liquid
---

# {{ title }}

{{ description }}

**[Czym jest Liquid?](https://shopify.github.io/liquid/)**

Jeden profil obejmuje wszystkie dialekty Liquid: motywy Shopify, Jekyll, LiquidJS (Eleventy) i Fluid (Orchard Core).

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Wszystkie opcje znajdziesz w przewodniku po konfiguracji!</a></div>
</div>
