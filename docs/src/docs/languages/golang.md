---
title: GoLang Template Linter and Formatter
keywords: GoLang, djlint, GoLang template linter, GoLang template formatter, format GoLang templates
description: djLint is a GoLang template linter and a GoLang template formatter! Take advantage of the pre-build profile when linting and formatting your templates with djLint.
tool: golang
---

# {{ title }}

{{ description }}

**[What is GoLang?](https://pkg.go.dev/text/template)**

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
