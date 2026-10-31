---
title: "Angular Template Linter"
description: "djLint est un linter de templates Angular ! Profitez du profil pré-construit lorsque vous lintez et formatez vos templates avec djLint."
sidebar:
  label: "Angular"
---

djLint est un linter de templates Angular ! Profitez du profil pré-construit lorsque vous lintez et formatez vos templates avec djLint.

**[C'est quoi Angular?](https://angular.io/guide/template-syntax)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=angular
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile="angular"
```

```toml title="djlint.toml / .djlint.toml"
profile="angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
