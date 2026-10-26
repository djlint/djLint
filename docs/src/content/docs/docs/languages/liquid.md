---
title: "Liquid Template Linter and Formatter"
description: "djLint is a Liquid template linter and a Liquid template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Liquid"
---

djLint is a Liquid template linter and a Liquid template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Liquid?](https://shopify.github.io/liquid/)**

One profile covers all Liquid dialects: Shopify themes, Jekyll, LiquidJS (Eleventy) and Fluid (Orchard Core).

#### Using the Command Line

```bash
djlint /path/to/templates --profile=liquid
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile="liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
