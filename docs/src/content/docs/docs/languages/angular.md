---
title: "Angular Template Linter"
description: "djLint lints Angular templates. Set the angular profile so the rules fit them."
sidebar:
  label: "Angular"
---

djLint lints Angular templates. Set the `angular` profile so the rules fit them.

**[What is Angular?](https://angular.io/guide/template-syntax)**

## Using the command line

```bash
djlint /path/to/templates --profile=angular
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
