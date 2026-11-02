---
title: "Linter und Formatter für Twig-Templates"
description: "djLint ist ein Linter und ein Formatter für Twig-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren."
sidebar:
  label: "Twig"
---

djLint ist ein Linter und ein Formatter für Twig-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren.

**[Was ist Twig?](https://twig.symfony.com/)**

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
