---
title: "Linter e formattatore per template Jinja"
description: "djLint analizza e formatta i template Jinja. Imposta il profilo jinja per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Jinja"
---

djLint analizza e formatta i template Jinja. Imposta il profilo `jinja` per adattare le regole e la formattazione a questi template.

**[Che cos'è Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja segue la sintassi di Jinja2 e anche i template Jinjava di HubSpot sono in stile Jinja, quindi usa il profilo `jinja` per entrambi.

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=jinja
```

## In un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```
