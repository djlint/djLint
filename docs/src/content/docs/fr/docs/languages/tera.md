---
title: "Tera Template Linter and Formatter"
description: "djLint est un linter de modèle Tera et un formateur de modèle Tera ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Tera"
---

djLint est un linter de modèle Tera et un formateur de modèle Tera ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi Tera?](https://keats.github.io/tera/)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=tera
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile="tera"
```

```toml title="djlint.toml / .djlint.toml"
profile="tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
