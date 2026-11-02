---
title: Linter i formater szablonów Handlebars
keywords: handlebars, djlint, linter szablonów handlebars, formater szablonów handlebars, formatowanie szablonów handlebars
description: djLint lintuje i formatuje szablony Handlebars. Ustaw profil handlebars, aby reguły i formatowanie były do nich dopasowane.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Czym jest Handlebars?](https://handlebarsjs.com/)**

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Lub w pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Wszystkie opcje znajdziesz w przewodniku po konfiguracji!</a></div>
</div>
