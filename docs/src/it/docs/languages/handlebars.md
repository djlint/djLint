---
title: Linter e formattatore per template Handlebars
keywords: handlebars, djlint, linter per template handlebars, formattatore per template handlebars, formattare template handlebars
description: djLint analizza e formatta i template Handlebars. Imposta il profilo handlebars per adattare le regole e la formattazione a questi template.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Che cos'è Handlebars?](https://handlebarsjs.com/)**

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
