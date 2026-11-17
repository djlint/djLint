---
title: "Linter und Formatter für Jinja-Templates"
description: "djLint lintet und formatiert Jinja-Templates. Setzen Sie das Profil jinja, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Jinja"
---

djLint lintet und formatiert Jinja-Templates. Setzen Sie das Profil `jinja`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja folgt der Syntax von Jinja2, und auch die Jinjava-Templates von HubSpot folgen dem Jinja-Stil. Verwenden Sie daher für beide das Profil `jinja`. J004 und J018 schlagen `url_for` von Flask vor, ignorieren Sie sie daher in einem Projekt ohne Flask.

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=jinja
```

## In einer Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```
