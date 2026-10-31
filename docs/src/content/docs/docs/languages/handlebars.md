---
title: "Handlebars Template Linter and Formatter"
description: "djLint is a handlebars template linter and a handlebars template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Handlebars"
---

djLint is a handlebars template linter and a handlebars template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Handlebars?](https://handlebarsjs.com/)**

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
