---
title: "Linter und Formatter für Jinja-Templates"
description: "djLint lintet und formatiert Jinja-Templates. Setzen Sie das Profil jinja, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Jinja"
---

djLint lintet und formatiert Jinja-Templates. Setzen Sie das Profil `jinja`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja-Templates sind vollständig Jinja2-kompatibel. Verwenden Sie daher ebenfalls das Profil `jinja`.

Auch die Jinjava-Templates von HubSpot folgen dem Jinja-Stil. Verwenden Sie dieses Profil also auch für sie.

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=jinja
```

## Oder über eine Konfigurationsdatei

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

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
