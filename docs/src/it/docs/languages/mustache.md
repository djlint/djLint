---
title: Linter e formattatore per template Mustache
keywords: mustache, djlint, linter per template mustache, formattatore per template mustache, formattare template mustache
description: djLint è un linter e un formattatore per template mustache! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Che cos'è Mustache?](https://mustache.github.io/mustache.5.html)**

#### Uso dalla riga di comando

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consulta la guida alla configurazione per conoscere tutte le opzioni!</a></div>
</div>
