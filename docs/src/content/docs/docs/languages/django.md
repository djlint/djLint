---
title: "Django Template Linter and Formatter"
description: "djLint is a django template linter and a django template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Django"
---

djLint is a django template linter and a django template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Using the Command Line

```bash
djlint /path/to/templates --profile=django
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
