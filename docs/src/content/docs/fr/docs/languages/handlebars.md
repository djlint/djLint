---
title: "Linter et formateur de templates Handlebars"
description: "djLint est un linter de templates handlebars et un formateur de templates handlebars ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint."
sidebar:
  label: "Handlebars"
---

djLint est un linter de templates handlebars et un formateur de templates handlebars ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.

**[Qu'est-ce que Handlebars ?](https://handlebarsjs.com/)**

#### En ligne de commande

```bash
djlint /path/to/templates --profile=handlebars
```

#### Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
