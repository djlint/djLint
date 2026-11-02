---
title: Linter e formattatore per template Django
keywords: django, djlint, linter per template django, formattatore per template django, formattare template django
description: djLint analizza e formatta i template Django. Imposta il profilo django per adattare le regole e la formattazione a questi template.
tool: django
---

# {{ title }}

{{ description }}

**[Che cos'è Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consulta la guida alla configurazione per conoscere tutte le opzioni!</a></div>
</div>
