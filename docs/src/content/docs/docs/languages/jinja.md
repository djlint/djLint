---
title: "Jinja template linter and formatter"
description: "djLint lints and formats Jinja templates. Set the jinja profile so the rules and the formatting fit them."
sidebar:
  label: "Jinja"
---

djLint lints and formats Jinja templates. Set the `jinja` profile so the rules and the formatting fit them.

**[What is Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja follows Jinja2's syntax, and HubSpot's Jinjava templates are Jinja-style too, so use the `jinja` profile for both. J004 and J018 suggest Flask's `url_for`, so ignore them in a project without Flask.

## Using the command line

```bash
djlint /path/to/templates --profile=jinja
```

## In a config file

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
