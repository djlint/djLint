---
title: "Mustache Template Linter and Formatter"
description: "djLint is a mustache template linter and a mustache template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Mustache"
---

djLint is a mustache template linter and a mustache template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Mustache?](https://mustache.github.io/mustache.5.html)**

#### Using the Command Line

```bash
djlint /path/to/templates --profile=handlebars
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
