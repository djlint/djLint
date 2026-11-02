---
title: Linter e formattatore per template Liquid
keywords: liquid, shopify, jekyll, eleventy, djlint, linter per template liquid, formattatore per template liquid, formattare template liquid, shopify, jekyll, eleventy, liquidjs, fluid, linter per temi shopify, linter per jekyll
description: djLint analizza e formatta i template Liquid. Imposta il profilo liquid per adattare le regole e la formattazione a questi template.
tool: liquid
---

# {{ title }}

{{ description }}

**[Che cos'è Liquid?](https://shopify.github.io/liquid/)**

Un unico profilo copre tutti i dialetti di Liquid: temi Shopify, Jekyll, LiquidJS (Eleventy) e Fluid (Orchard Core).

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consulta la guida alla configurazione per conoscere tutte le opzioni!</a></div>
</div>
