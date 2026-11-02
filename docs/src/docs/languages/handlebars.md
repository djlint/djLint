---
title: Handlebars Template Linter and Formatter
keywords: handlebars, djlint, handlebars template linter, handlebars template formatter, format handlebars templates
description: djLint lints and formats Handlebars templates. Set the handlebars profile so the rules and the formatting fit them.
tool: handlebars
---

# {{ title }}

{{ description }}

**[What is Handlebars?](https://handlebarsjs.com/)**

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
