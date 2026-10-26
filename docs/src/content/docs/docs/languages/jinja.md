---
title: "Jinja Template Linter and Formatter"
description: "djLint is a jinja template linter and a jinja template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Jinja"
---

djLint is a jinja template linter and a jinja template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What is Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja templates are fully Jinja2-compatible, so use this same `jinja` profile.

HubSpot's Jinjava templates are also jinja-style, so use this profile for them too.

#### Using the Command Line

```bash
djlint /path/to/templates --profile=jinja
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile="jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
