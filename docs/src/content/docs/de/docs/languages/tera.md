---
title: "Linter und Formatter für Tera-Templates"
description: "djLint lintet und formatiert Tera-Templates. Setzen Sie das Profil tera, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Tera"
---

djLint lintet und formatiert Tera-Templates. Setzen Sie das Profil `tera`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Tera?](https://keats.github.io/tera/)**

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=tera
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

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
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
