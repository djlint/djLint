---
title: Linter i formater szablonów Mustache
keywords: mustache, djlint, linter szablonów mustache, formater szablonów mustache, formatowanie szablonów mustache
description: djLint to linter i formater szablonów mustache! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Czym jest Mustache?](https://mustache.github.io/mustache.5.html)**

#### Z wiersza poleceń

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Wszystkie opcje znajdziesz w przewodniku po konfiguracji!</a></div>
</div>
