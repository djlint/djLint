---
title: Tera Template Linter and Formatter
keywords: tera, rust, zola, djlint, tera template linter, tera template formatter, format tera templates
description: djLint is a Tera template linter and a Tera template formatter! Take advantage of the pre-build profile when linting and formatting your templates with djLint.
tool: tera
---

# {{ title }}

{{ description }}

**[What is Tera?](https://keats.github.io/tera/)**

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
