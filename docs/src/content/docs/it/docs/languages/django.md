---
title: "Linter e formattatore per template Django"
description: "djLint è un linter e un formattatore per template django! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint."
sidebar:
  label: "Django"
---

djLint è un linter e un formattatore per template django! Sfrutta il profilo già pronto per il lint e la formattazione dei tuoi template con djLint.

**[Che cos'è Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Uso dalla riga di comando

```bash
djlint /path/to/templates --profile=django
```

#### Oppure usa un file di configurazione

Configura djLint nel file `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` del tuo progetto.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Consulta la guida alla configurazione per conoscere tutte le opzioni!](/it/docs/configuration/)
:::
