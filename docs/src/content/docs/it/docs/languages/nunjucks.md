---
title: "Linter e formattatore per template Nunjucks"
description: "djLint analizza e formatta i template Nunjucks. Imposta il profilo nunjucks per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Nunjucks"
---

djLint analizza e formatta i template Nunjucks. Imposta il profilo `nunjucks` per adattare le regole e la formattazione a questi template.

**[Che cos'è Nunjucks?](https://mozilla.github.io/nunjucks/)**

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=nunjucks
```

## In un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```
