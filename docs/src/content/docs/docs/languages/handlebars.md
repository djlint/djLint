---
title: "Handlebars Template Linter and Formatter"
description: "djLint lints and formats Handlebars templates. Set the handlebars profile so the rules and the formatting fit them."
sidebar:
  label: "Handlebars"
---

djLint lints and formats Handlebars templates. Set the `handlebars` profile so the rules and the formatting fit them.

**[What is Handlebars?](https://handlebarsjs.com/)**

## Using the command line

```bash
djlint /path/to/templates --profile=handlebars
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
