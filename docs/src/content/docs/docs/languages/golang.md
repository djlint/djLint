---
title: "Go Template Linter and Formatter"
description: "djLint is a Go template linter and a Go template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint."
sidebar:
  label: "Go templates"
---

djLint is a Go template linter and a Go template formatter! Take advantage of the pre-built profile when linting and formatting your templates with djLint.

**[What are Go templates?](https://pkg.go.dev/text/template)**

Go templates (`text/template`, `html/template`) also power Hugo themes and Helm charts, so use this same profile for them.

#### Using the Command Line

```bash
djlint /path/to/templates --profile=golang
```

#### Or, Use a Config File

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile="golang"
```

```toml title="djlint.toml / .djlint.toml"
profile="golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
