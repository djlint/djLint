---
title: "Linter und Formatter für Askama-Templates"
description: "djLint lintet und formatiert Askama-Templates. Setzen Sie das Profil askama, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Askama"
---

djLint lintet und formatiert Askama-Templates. Setzen Sie das Profil `askama`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Askama?](https://askama.readthedocs.io/)**

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=askama
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
