---
title: Linter e formattatore per template Nunjucks
keywords: nunjucks, djlint, linter per template nunjucks, formattatore per template nunjucks, formattare template nunjucks, pebble, linter per template pebble
description: djLint analizza e formatta i template Nunjucks. Imposta il profilo nunjucks per adattare le regole e la formattazione a questi template.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Che cos'è Nunjucks?](https://mozilla.github.io/nunjucks/)**

I template Pebble (Java) sono compatibili con Twig, quindi usa questo stesso profilo anche per loro.

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
