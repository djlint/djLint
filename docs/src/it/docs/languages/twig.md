---
title: Linter e formattatore per template Twig
keywords: twig, djlint, linter per template twig, formattatore per template twig, formattare template twig, pebble, linter per template pebble
description: djLint è un linter e un formattatore per template twig! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Che cos'è Twig?](https://twig.symfony.com/)**

I template Pebble (Java) sono compatibili con Twig, quindi usa questo stesso profilo anche per loro.

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
