---
title: "Tera template linter and formatter"
description: "djLint lints and formats Tera templates. Set the tera profile so the rules and the formatting fit them."
sidebar:
  label: "Tera"
---

djLint lints and formats Tera templates. Set the `tera` profile so the rules and the formatting fit them.

**[What is Tera?](https://keats.github.io/tera/)**

## Using the command line

```bash
djlint /path/to/templates --profile=tera
```

## In a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```
