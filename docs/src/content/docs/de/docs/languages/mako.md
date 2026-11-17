---
title: "Linter und Formatter für Mako-Templates"
description: "djLint lintet und formatiert Mako-Templates. Setzen Sie das Profil mako, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Mako"
---

djLint lintet und formatiert Mako-Templates. Setzen Sie das Profil `mako`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Mako?](https://www.makotemplates.org/)**

Mit dem Profil mako steht eine Steuerzeile wie `% if x:` und ein `##`-Kommentar immer in einer eigenen Zeile, und ein Tag, dessen Attribute von Steuerzeilen abhängen, behält sie so, wie sie geschrieben sind. Python-Blöcke und der Inhalt von `<%doc>` und `<%text>` bleiben unverändert, ebenso ein script oder style mit Mako-Syntax bei `--format-js` oder `--format-css`. Die Zeilen zwischen `% if` und `% endif` sowie zwischen einem `<%block>`- oder `<%def>`-Tag und seinem schließenden Tag, wenn beide in einer eigenen Zeile stehen, werden wie jeder andere Block eingerückt. Der Code in einem `${}`-Ausdruck bleibt so, wie er geschrieben ist.

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=mako
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
