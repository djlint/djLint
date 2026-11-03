---
title: Mako Template Linter and Formatter
keywords: mako, python, pyramid, open edx, djlint, mako template linter, mako template formatter, format mako templates
description: djLint lints and formats Mako templates. Set the mako profile so the rules and the formatting fit them.
tool: mako
---

# {{ title }}

{{ description }}

**[What is Mako?](https://www.makotemplates.org/)**

With the mako profile, a control line such as `% if x:` and a `##` comment always keep a line of their own, and a tag whose attributes depend on control lines keeps them as written. Python blocks and the contents of `<%doc>` and `<%text>` are left alone, and so is a script or style that holds Mako syntax under `--format-js` or `--format-css`. The lines between `% if` and `% endif`, and between a `<%block>` or `<%def>` tag and its closing tag when each has a line of its own, are indented like any other block. The code in a `${}` expression is left as written.

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
