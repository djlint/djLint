---
title: Liquid Template Linter and Formatter
keywords: liquid, shopify, jekyll, eleventy, djlint, liquid template linter, liquid template formatter, format liquid templates, shopify, jekyll, eleventy, liquidjs, fluid, shopify theme linter, jekyll linter
description: djLint is a Liquid template linter and a Liquid template formatter! Take advantage of the pre-build profile when linting and formatting your templates with djLint.
tool: liquid
---

# {{ title }}

{{ description }}

**[What is Liquid?](https://shopify.github.io/liquid/)**

One profile covers all Liquid dialects: Shopify themes, Jekyll, LiquidJS (Eleventy) and Fluid (Orchard Core).

#### Using the Command Line

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Or, Use a Config File

Configure djLint in your projects `pyproject.toml`.

```toml
[tool.djlint]
profile="{{ tool }}"
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>
