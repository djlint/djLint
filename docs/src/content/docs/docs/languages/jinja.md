---
title: "Jinja Template Linter and Formatter"
description: "djLint lints and formats Jinja templates. Set the jinja profile so the rules and the formatting fit them."
sidebar:
  label: "Jinja"
---

djLint lints and formats Jinja templates. Set the `jinja` profile so the rules and the formatting fit them.

**[What is Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja templates are fully Jinja2-compatible, so use this same `jinja` profile.

HubSpot's Jinjava templates are also jinja-style, so use this profile for them too.

## Using the command line

```bash
djlint /path/to/templates --profile=jinja
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
