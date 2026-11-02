---
title: "Linter per template Angular"
description: "djLint è un linter per template Angular! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint."
sidebar:
  label: "Angular"
---

djLint è un linter per template Angular! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint.

**[Che cos'è Angular?](https://angular.io/guide/template-syntax)**

#### Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=angular
```

#### Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile="angular"
```

```toml title="djlint.toml / .djlint.toml"
profile="angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
