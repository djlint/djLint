---
title: "Nunjucks Template Linter and Formatter"
description: "djLint lints and formats Nunjucks templates. Set the nunjucks profile so the rules and the formatting fit them."
sidebar:
  label: "Nunjucks"
---

djLint lints and formats Nunjucks templates. Set the `nunjucks` profile so the rules and the formatting fit them.

**[What is Nunjucks?](https://mozilla.github.io/nunjucks/)**

Pebble (Java) templates are Twig-compatible, so use this same profile for them.

## Using the command line

```bash
djlint /path/to/templates --profile=nunjucks
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
