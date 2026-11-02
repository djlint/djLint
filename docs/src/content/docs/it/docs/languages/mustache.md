---
title: "Linter e formattatore per template Mustache"
description: "djLint è un linter e un formattatore per template mustache! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint."
sidebar:
  label: "Mustache"
---

djLint è un linter e un formattatore per template mustache! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint.

**[Che cos'è Mustache?](https://mustache.github.io/mustache.5.html)**

#### Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=handlebars
```

#### Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
