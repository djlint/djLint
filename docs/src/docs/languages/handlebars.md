---
title: Handlebars Template Linter and Formatter
keywords: handlebars, djlint, handlebars template linter, handlebars template formatter, format handlebars templates
description: djLint is a handlebars template linter and a handlebars template formatter! Take advantage of the pre-build profile when linting and formatting your templates with djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[What is Handlebars?](https://handlebarsjs.com/)**

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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>
