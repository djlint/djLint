---
title: "Linter und Formatter für Nunjucks-Templates"
description: "djLint ist ein Linter und ein Formatter für Nunjucks-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren."
sidebar:
  label: "Nunjucks"
---

djLint ist ein Linter und ein Formatter für Nunjucks-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren.

**[Was ist Nunjucks?](https://mozilla.github.io/nunjucks/)**

Pebble-Templates (Java) sind Twig-kompatibel. Verwenden Sie für sie daher dasselbe Profil.

#### Über die Befehlszeile

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
