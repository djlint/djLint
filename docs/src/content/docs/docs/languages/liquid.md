---
title: "Liquid Template Linter and Formatter"
description: "djLint lints and formats Liquid templates. Set the liquid profile so the rules and the formatting fit them."
sidebar:
  label: "Liquid"
---

djLint lints and formats Liquid templates. Set the `liquid` profile so the rules and the formatting fit them.

**[What is Liquid?](https://shopify.github.io/liquid/)**

One profile covers all Liquid dialects: Shopify themes, Jekyll, LiquidJS (Eleventy) and Fluid (Orchard Core).

## Using the command line

```bash
djlint /path/to/templates --profile=liquid
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
