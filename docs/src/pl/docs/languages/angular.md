---
title: Linter szablonów Angular
keywords: angular, djlint, linter szablonów angular, lintowanie szablonów angular
description: djLint lintuje szablony Angular. Ustaw profil angular, aby reguły były do nich dopasowane.
tool: angular
---

# {{ title }}

{{ description }}

**[Czym jest Angular?](https://angular.io/guide/template-syntax)**

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
