---
title: "Linter für Angular-Templates"
description: "djLint lintet Angular-Templates. Setzen Sie das Profil angular, damit die Regeln zu ihnen passen."
sidebar:
  label: "Angular"
---

djLint lintet Angular-Templates. Setzen Sie das Profil `angular`, damit die Regeln zu ihnen passen.

**[Was ist Angular?](https://angular.dev/guide/templates)**

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=angular
```

## In einer Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```
