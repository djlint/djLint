---
title: "Linter e formattatore per template Tera"
description: "djLint analizza e formatta i template Tera. Imposta il profilo tera per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Tera"
---

djLint analizza e formatta i template Tera. Imposta il profilo `tera` per adattare le regole e la formattazione a questi template.

**[Che cos'è Tera?](https://keats.github.io/tera/)**

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=tera
```

## In un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```
