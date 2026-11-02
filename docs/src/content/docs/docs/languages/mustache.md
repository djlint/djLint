---
title: "Mustache Template Linter and Formatter"
description: "djLint lints and formats Mustache templates. Set the handlebars profile so the rules and the formatting fit them."
sidebar:
  label: "Mustache"
---

djLint lints and formats Mustache templates. Set the `handlebars` profile so the rules and the formatting fit them.

**[What is Mustache?](https://mustache.github.io/mustache.5.html)**

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
