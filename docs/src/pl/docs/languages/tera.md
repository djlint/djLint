---
title: Linter i formater szablonów Tera
keywords: tera, rust, zola, djlint, linter szablonów tera, formater szablonów tera, formatowanie szablonów tera
description: djLint to linter i formater szablonów Tera! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.
tool: tera
---

# {{ title }}

{{ description }}

**[Czym jest Tera?](https://keats.github.io/tera/)**

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
