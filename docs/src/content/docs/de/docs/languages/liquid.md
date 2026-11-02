---
title: "Linter und Formatter für Liquid-Templates"
description: "djLint ist ein Linter und ein Formatter für Liquid-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren."
sidebar:
  label: "Liquid"
---

djLint ist ein Linter und ein Formatter für Liquid-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren.

**[Was ist Liquid?](https://shopify.github.io/liquid/)**

Ein Profil deckt alle Liquid-Dialekte ab: Shopify-Themes, Jekyll, LiquidJS (Eleventy) und Fluid (Orchard Core).

#### Über die Befehlszeile

```bash
djlint /path/to/templates --profile=liquid
```

#### Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile="liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile="liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
