---
title: Linter e formattatore per template Jinja
keywords: jinja, djlint, linter per template jinja, formattatore per template jinja, formattare template jinja, minijinja, jinjava, linter per template minijinja, linter per template jinjava
description: djLint analizza e formatta i template Jinja. Imposta il profilo jinja per adattare le regole e la formattazione a questi template.
tool: jinja
---

# {{ title }}

{{ description }}

**[Che cos'è Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

I template MiniJinja sono pienamente compatibili con Jinja2, quindi usa questo stesso profilo `jinja`.

Anche i template Jinjava di HubSpot sono in stile jinja, quindi usa questo profilo anche per loro.

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
