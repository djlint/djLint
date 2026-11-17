---
title: "Linter und Formatter für Handlebars-Templates"
description: "djLint lintet und formatiert Handlebars-Templates. Setzen Sie das Profil handlebars, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Handlebars"
---

djLint lintet und formatiert Handlebars-Templates. Setzen Sie das Profil `handlebars`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Handlebars?](https://handlebarsjs.com/)**

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=handlebars
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
