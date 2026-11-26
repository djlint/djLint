---
title: "Handlebars template linter and formatter"
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

## In a config file

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
