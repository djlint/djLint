---
title: Linter a formátovač šablon Jinja
keywords: jinja, djlint, linter šablon jinja, formátovač šablon jinja, formátování šablon jinja, minijinja, jinjava, linter šablon minijinja, linter šablon jinjava
description: djLint lintuje a formátuje šablony Jinja. Nastavte profil jinja, aby jim pravidla i formátování odpovídaly.
tool: jinja
---

# {{ title }}

{{ description }}

**[Co je Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Šablony MiniJinja jsou plně kompatibilní s Jinja2, takže použijte stejný profil `jinja`.

Šablony Jinjava od HubSpotu jsou také ve stylu jinja, takže pro ně použijte tento profil také.

## Z příkazového řádku

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Všechny možnosti najdete v průvodci konfigurací!</a></div>
</div>
