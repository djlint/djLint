---
title: Nunjucks Template Linter and Formatter
keywords: nunjucks, djlint, nunjucks template linter, nunjucks template formatter, format nunjucks templates, pebble, pebble template linter
description: djLint lints and formats Nunjucks templates. Set the nunjucks profile so the rules and the formatting fit them.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[What is Nunjucks?](https://mozilla.github.io/nunjucks/)**

Pebble (Java) templates are Twig-compatible, so use this same profile for them.

## Using the command line

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>
