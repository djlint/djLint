---
title: Linter i formater szablonów Go
keywords: szablony go, golang, djlint, linter szablonów go, formater szablonów go, linter szablonów golang, formater szablonów golang, formatowanie szablonów go, linter szablonów hugo, linter szablonów helm
description: djLint lintuje i formatuje szablony Go. Ustaw profil golang, aby reguły i formatowanie były do nich dopasowane.
tool: golang
---

# {{ title }}

{{ description }}

**[Czym są szablony Go?](https://pkg.go.dev/text/template)**

Szablony Go (`text/template`, `html/template`) napędzają też motywy Hugo i charty Helm, więc używaj dla nich tego samego profilu.

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
