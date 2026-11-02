---
title: Linter i formater szablonów Twig
keywords: twig, djlint, linter szablonów twig, formater szablonów twig, formatowanie szablonów twig, pebble, linter szablonów pebble
description: djLint lintuje i formatuje szablony Twig. Ustaw profil nunjucks, aby reguły i formatowanie były do nich dopasowane.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Czym jest Twig?](https://twig.symfony.com/)**

Szablony Pebble (Java) są zgodne z Twig, więc używaj dla nich tego samego profilu.

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
