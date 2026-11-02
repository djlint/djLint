---
title: "Linter e formattatore per template Jinja"
description: "djLint analizza e formatta i template Jinja. Imposta il profilo jinja per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Jinja"
---

djLint analizza e formatta i template Jinja. Imposta il profilo `jinja` per adattare le regole e la formattazione a questi template.

**[Che cos'è Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

I template MiniJinja sono pienamente compatibili con Jinja2, quindi usa questo stesso profilo `jinja`.

Anche i template Jinjava di HubSpot sono in stile jinja, quindi usa questo profilo anche per loro.

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=jinja
```

## Oppure usa un file di configurazione

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

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
