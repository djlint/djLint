---
title: "Tera Template Linter and Formatter"
description: "djLint is a Tera template linter and a Tera template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Tera"
---

djLint is a Tera template linter and a Tera template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Tera?](https://keats.github.io/tera/)**

#### Using the Command Line

```bash
djlint /path/to/templates --profile=tera
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="tera"
```

```toml title="djlint.toml / .djlint.toml"
profile="tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
