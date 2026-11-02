---
title: "Linter et formateur de templates Mustache"
description: "djLint est un linter de templates mustache et un formateur de templates mustache ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint."
sidebar:
  label: "Mustache"
---

djLint est un linter de templates mustache et un formateur de templates mustache ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.

**[Qu'est-ce que Mustache ?](https://mustache.github.io/mustache.5.html)**

#### En ligne de commande

```bash
djlint /path/to/templates --profile=handlebars
```

#### Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

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
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
