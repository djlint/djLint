---
title: "Linter und Formatter für Twig-Templates"
description: "djLint lintet und formatiert Twig-Templates. Setzen Sie das Profil nunjucks, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Twig"
---

djLint lintet und formatiert Twig-Templates. Setzen Sie das Profil `nunjucks`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Twig?](https://twig.symfony.com/)**

Pebble-Templates (Java) sind Twig-kompatibel. Verwenden Sie für sie daher dasselbe Profil.

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=nunjucks
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
