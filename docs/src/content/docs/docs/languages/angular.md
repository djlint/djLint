---
title: "Angular Template Linter"
description: "djLint is an Angular template linter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Angular"
---

djLint is an Angular template linter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Angular?](https://angular.io/guide/template-syntax)**

#### Using the Command Line

```bash
djlint /path/to/templates --profile=angular
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="angular"
```

```toml title="djlint.toml / .djlint.toml"
profile="angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
