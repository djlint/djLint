---
title: Linter a formátovač šablon Go
keywords: šablony go, golang, djlint, linter šablon go, formátovač šablon go, linter šablon golang, formátovač šablon golang, formátování šablon go, linter šablon hugo, linter šablon helm
description: djLint je linter a formátovač šablon Go! Při lintování a formátování šablon pomocí djLint využijte připravený profil.
tool: golang
---

# {{ title }}

{{ description }}

**[Co jsou šablony Go?](https://pkg.go.dev/text/template)**

Na šablonách Go (`text/template`, `html/template`) stojí také motivy Hugo a charty Helm, takže pro ně použijte stejný profil.

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Všechny možnosti najdete v průvodci konfigurací!</a></div>
</div>
