---
title: Mustache Template Linter and Formatter
keywords: mustache, djlint, mustache template linter, mustache template formatter, format mustache templates
description: djLint is a mustache template linter and a mustache template formatter! Take advantage of the pre-build profile when linting and formatting your templates with djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[What is Mustache?](http://mustache.github.io/mustache.5.html)**

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
