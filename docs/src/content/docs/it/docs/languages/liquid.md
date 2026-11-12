---
title: "Linter e formattatore per template Liquid"
description: "djLint analizza e formatta i template Liquid. Imposta il profilo liquid per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Liquid"
---

djLint analizza e formatta i template Liquid. Imposta il profilo `liquid` per adattare le regole e la formattazione a questi template.

**[Che cos'è Liquid?](https://shopify.github.io/liquid/)**

Un unico profilo copre tutti i dialetti di Liquid: temi Shopify, Jekyll, LiquidJS (Eleventy) e Fluid (Orchard Core).

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=liquid
```

## Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
