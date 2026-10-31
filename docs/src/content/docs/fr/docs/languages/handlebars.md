---
title: "Handlebars Template Linter and Formatter"
description: "djLint est un linter de modèles Handlebars et un formateur de modèles Handlebars ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Handlebars"
---

djLint est un linter de modèles Handlebars et un formateur de modèles Handlebars ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi Handlebars?](https://handlebarsjs.com/)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=handlebars
```

#### Ou, utiliser un fichier de configuration

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
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
