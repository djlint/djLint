---
title: "Askama template linter and formatter"
description: "djLint lints and formats Askama templates. Set the askama profile so the rules and the formatting fit them."
sidebar:
  label: "Askama"
---

djLint lints and formats Askama templates. Set the `askama` profile so the rules and the formatting fit them.

**[What is Askama?](https://askama.readthedocs.io/)**

## Using the command line

```bash
djlint /path/to/templates --profile=askama
```

## In a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```
