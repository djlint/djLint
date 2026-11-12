---
title: "Mako Template Linter and Formatter"
description: "djLint lints and formats Mako templates. Set the mako profile so the rules and the formatting fit them."
sidebar:
  label: "Mako"
---

djLint lints and formats Mako templates. Set the `mako` profile so the rules and the formatting fit them.

**[What is Mako?](https://www.makotemplates.org/)**

With the mako profile, a control line such as `% if x:` and a `##` comment always keep a line of their own, and a tag whose attributes depend on control lines keeps them as written. Python blocks and the contents of `<%doc>` and `<%text>` are left alone, and so is a script or style that holds Mako syntax under `--format-js` or `--format-css`. The lines between `% if` and `% endif`, and between a `<%block>` or `<%def>` tag and its closing tag when each has a line of its own, are indented like any other block. The code in a `${}` expression is left as written.

## Using the command line

```bash
djlint /path/to/templates --profile=mako
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::
