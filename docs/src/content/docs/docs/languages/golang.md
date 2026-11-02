---
title: "Go Template Linter and Formatter"
description: "djLint lints and formats Go templates. Set the golang profile so the rules and the formatting fit them."
sidebar:
  label: "Go templates"
---

djLint lints and formats Go templates. Set the `golang` profile so the rules and the formatting fit them.

**[What are Go templates?](https://pkg.go.dev/text/template)**

Go templates (`text/template`, `html/template`) also power Hugo themes and Helm charts, so use this same profile for them.

## Using the command line

```bash
djlint /path/to/templates --profile=golang
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
