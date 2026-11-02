---
title: "Linter a formátovač šablon Go"
description: "djLint je linter a formátovač šablon Go! Při lintování a formátování šablon pomocí djLint využijte připravený profil."
sidebar:
  label: "Šablony Go"
---

djLint je linter a formátovač šablon Go! Při lintování a formátování šablon pomocí djLint využijte připravený profil.

**[Co jsou šablony Go?](https://pkg.go.dev/text/template)**

Na šablonách Go (`text/template`, `html/template`) stojí také motivy Hugo a charty Helm, takže pro ně použijte stejný profil.

#### Z příkazového řádku

```bash
djlint /path/to/templates --profile=golang
```

#### Nebo v konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

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
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::
