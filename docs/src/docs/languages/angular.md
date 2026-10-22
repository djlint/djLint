---
title: Angular Template Linter
keywords: angular, djlint, angular template linter, lint angular templates
description: djLint is an Angular template linter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.
tool: angular
---

# {{ title }}

{{ description }}

**[What is Angular?](https://angular.io/guide/template-syntax)**

#### Using the Command Line

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>
