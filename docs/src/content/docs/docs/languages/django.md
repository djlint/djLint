---
title: "Django Template Linter and Formatter"
description: "djLint lints and formats Django templates. Set the django profile so the rules and the formatting fit them."
sidebar:
  label: "Django"
---

djLint lints and formats Django templates. Set the `django` profile so the rules and the formatting fit them.

**[What is Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Using the command line

```bash
djlint /path/to/templates --profile=django
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
