---
title: "Linter e formattatore per template Django"
description: "djLint analizza e formatta i template Django. Imposta il profilo django per adattare le regole e la formattazione a questi template."
sidebar:
  label: "Django"
---

djLint analizza e formatta i template Django. Imposta il profilo `django` per adattare le regole e la formattazione a questi template.

**[Che cos'è Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=django
```

## Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
