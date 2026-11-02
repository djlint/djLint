---
title: "Linter e formattatore per template Tera"
description: "djLint è un linter e un formattatore per template Tera! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint."
sidebar:
  label: "Tera"
---

djLint è un linter e un formattatore per template Tera! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint.

**[Che cos'è Tera?](https://keats.github.io/tera/)**

#### Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=tera
```

#### Oppure usa un file di configurazione

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

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
