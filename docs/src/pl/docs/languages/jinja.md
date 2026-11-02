---
title: Linter i formater szablonów Jinja
keywords: jinja, djlint, linter szablonów jinja, formater szablonów jinja, formatowanie szablonów jinja, minijinja, jinjava, linter szablonów minijinja, linter szablonów jinjava
description: djLint to linter i formater szablonów jinja! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.
tool: jinja
---

# {{ title }}

{{ description }}

**[Czym jest Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Szablony MiniJinja są w pełni zgodne z Jinja2, więc używaj tego samego profilu `jinja`.

Szablony Jinjava od HubSpot również są w stylu jinja, więc używaj tego profilu także dla nich.

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
