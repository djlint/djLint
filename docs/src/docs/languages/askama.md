---
title: Askama Template Linter and Formatter
keywords: askama, rust, djlint, askama template linter, askama template formatter, format askama templates
description: djLint is an Askama template linter and an Askama template formatter! Take advantage of the pre-build profile when linting and formatting your templates with djLint.
tool: askama
---

# {{ title }}

{{ description }}

**[What is Askama?](https://askama.readthedocs.io/)**

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
