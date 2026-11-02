---
title: "Linter und Formatter für Go-Templates"
description: "djLint lintet und formatiert Go-Templates. Setzen Sie das Profil golang, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Go-Templates"
---

djLint lintet und formatiert Go-Templates. Setzen Sie das Profil `golang`, damit Regeln und Formatierung zu ihnen passen.

**[Was sind Go-Templates?](https://pkg.go.dev/text/template)**

Auf Go-Templates (`text/template`, `html/template`) bauen auch Hugo-Themes und Helm-Charts auf. Verwenden Sie für diese daher dasselbe Profil.

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=golang
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

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
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
