---
title: "Linter und Formatter für Mustache-Templates"
description: "djLint ist ein Linter und ein Formatter für Mustache-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren."
sidebar:
  label: "Mustache"
---

djLint ist ein Linter und ein Formatter für Mustache-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren.

**[Was ist Mustache?](https://mustache.github.io/mustache.5.html)**

#### Über die Befehlszeile

```bash
djlint /path/to/templates --profile=handlebars
```

#### Oder über eine Konfigurationsdatei

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
