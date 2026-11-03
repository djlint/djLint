---
title: Linter e formattatore per template Mako
keywords: mako, python, pyramid, open edx, djlint, linter per template mako, formattatore per template mako, formattare template mako
description: djLint analizza e formatta i template Mako. Imposta il profilo mako per adattare le regole e la formattazione a questi template.
tool: mako
---

# {{ title }}

{{ description }}

**[Che cos'è Mako?](https://www.makotemplates.org/)**

Con il profilo mako, una riga di controllo come `% if x:` e un commento `##` restano sempre su una riga a sé, e un tag i cui attributi dipendono da righe di controllo li mantiene come sono scritti. I blocchi Python e il contenuto di `<%doc>` e `<%text>` non vengono toccati, e lo stesso vale per uno script o uno style che contiene sintassi Mako con `--format-js` o `--format-css`. Le righe tra `% if` e `% endif`, e tra un tag `<%block>` o `<%def>` e il suo tag di chiusura quando ognuno sta su una riga a sé, vengono indentate come qualsiasi altro blocco. Il codice di un'espressione `${}` resta com'è scritto.

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
