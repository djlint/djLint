---
title: "Linter e formattatore per template Askama"
description: "djLint analizza e formatta i template Askama. Imposta il profilo askama per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Askama"
---

djLint analizza e formatta i template Askama. Imposta il profilo `askama` per adattare le regole e la formattazione a questi template.

**[Che cos'è Askama?](https://askama.readthedocs.io/)**

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=askama
```

## Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
