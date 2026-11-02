---
title: Go Template Linter and Formatter
keywords: go templates, golang, djlint, go template linter, go template formatter, golang template linter, golang template formatter, format go templates, hugo template linter, helm template linter
description: djLint lints and formats Go templates. Set the golang profile so the rules and the formatting fit them.
tool: golang
---

# {{ title }}

{{ description }}

**[What are Go templates?](https://pkg.go.dev/text/template)**

Go templates (`text/template`, `html/template`) also power Hugo themes and Helm charts, so use this same profile for them.

## Using the command line

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Or, use a config file

Configure djLint in your project's `pyproject.toml`, `djlint.toml` / `.djlint.toml`, or `.djlintrc` file.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>
