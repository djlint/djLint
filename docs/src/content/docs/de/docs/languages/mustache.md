---
title: "Linter und Formatter für Mustache-Templates"
description: "djLint lintet und formatiert Mustache-Templates. Setzen Sie das Profil handlebars, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Mustache"
---

djLint lintet und formatiert Mustache-Templates. Setzen Sie das Profil `handlebars`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Mustache?](https://mustache.github.io/mustache.5.html)**

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
