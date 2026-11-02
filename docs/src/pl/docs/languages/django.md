---
title: Linter i formater szablonów Django
keywords: django, djlint, linter szablonów django, formater szablonów django, formatowanie szablonów django
description: djLint lintuje i formatuje szablony Django. Ustaw profil django, aby reguły i formatowanie były do nich dopasowane.
tool: django
---

# {{ title }}

{{ description }}

**[Czym jest Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

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
