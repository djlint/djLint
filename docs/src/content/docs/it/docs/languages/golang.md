---
title: "Linter e formattatore per template Go"
description: "djLint analizza e formatta i template Go. Imposta il profilo golang per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Template Go"
---

djLint analizza e formatta i template Go. Imposta il profilo `golang` per adattare le regole e la formattazione a questi template.

**[Che cosa sono i template Go?](https://pkg.go.dev/text/template)**

Anche i temi Hugo e i chart Helm si basano sui template Go (`text/template`, `html/template`), quindi usa questo stesso profilo anche per loro.

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=golang
```

## Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
