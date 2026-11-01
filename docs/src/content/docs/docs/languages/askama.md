---
title: "Askama Template Linter and Formatter"
description: "djLint is an Askama template linter and an Askama template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Askama"
---

djLint is an Askama template linter and an Askama template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Askama?](https://askama.readthedocs.io/)**

#### Using the Command Line

```bash
djlint /path/to/templates --profile=askama
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="askama"
```

```toml title="djlint.toml / .djlint.toml"
profile="askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
