---
title: Linter i formater szablonów Nunjucks
keywords: nunjucks, djlint, linter szablonów nunjucks, formater szablonów nunjucks, formatowanie szablonów nunjucks, pebble, linter szablonów pebble
description: djLint to linter i formater szablonów nunjucks! Korzystaj z gotowego profilu podczas lintowania i formatowania szablonów za pomocą djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Czym jest Nunjucks?](https://mozilla.github.io/nunjucks/)**

Szablony Pebble (Java) są zgodne z Twig, więc używaj dla nich tego samego profilu.

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
