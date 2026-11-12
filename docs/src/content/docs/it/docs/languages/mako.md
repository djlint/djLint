---
title: "Linter e formattatore per template Mako"
description: "djLint analizza e formatta i template Mako. Imposta il profilo mako per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Mako"
---

djLint analizza e formatta i template Mako. Imposta il profilo `mako` per adattare le regole e la formattazione a questi template.

**[Che cos'è Mako?](https://www.makotemplates.org/)**

Con il profilo mako, una riga di controllo come `% if x:` e un commento `##` restano sempre su una riga a sé, e un tag i cui attributi dipendono da righe di controllo li mantiene come sono scritti. I blocchi Python e il contenuto di `<%doc>` e `<%text>` non vengono toccati, e lo stesso vale per uno script o uno style che contiene sintassi Mako con `--format-js` o `--format-css`. Le righe tra `% if` e `% endif`, e tra un tag `<%block>` o `<%def>` e il suo tag di chiusura quando ognuno sta su una riga a sé, vengono indentate come qualsiasi altro blocco. Il codice di un'espressione `${}` resta com'è scritto.

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=mako
```

## Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
