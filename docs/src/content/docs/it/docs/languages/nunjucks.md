---
title: "Linter e formattatore per template Nunjucks"
description: "djLint è un linter e un formattatore per template nunjucks! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint."
sidebar:
  label: "Nunjucks"
---

djLint è un linter e un formattatore per template nunjucks! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint.

**[Che cos'è Nunjucks?](https://mozilla.github.io/nunjucks/)**

I template Pebble (Java) sono compatibili con Twig, quindi usa questo stesso profilo anche per loro.

#### Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
