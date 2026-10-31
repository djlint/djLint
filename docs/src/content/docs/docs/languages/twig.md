---
title: "Twig Template Linter and Formatter"
description: "djLint is a twig template linter and a twig template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Twig"
---

djLint is a twig template linter and a twig template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Twig?](https://twig.symfony.com/)**

Pebble (Java) templates are Twig-compatible, so use this same profile for them.

#### Using the Command Line

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
