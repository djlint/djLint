---
title: Linter e formattatore per template Go
keywords: template go, golang, djlint, linter per template go, formattatore per template go, linter per template golang, formattatore per template golang, formattare template go, linter per template hugo, linter per template helm
description: djLint analizza e formatta i template Go. Imposta il profilo golang per adattare le regole e la formattazione a questi template.
tool: golang
---

# {{ title }}

{{ description }}

**[Che cosa sono i template Go?](https://pkg.go.dev/text/template)**

Anche i temi Hugo e i chart Helm si basano sui template Go (`text/template`, `html/template`), quindi usa questo stesso profilo anche per loro.

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
