---
title: "Twig Template Linter and Formatter"
description: "djLint est un linter de modèles twig et un formateur de modèles twig ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Twig"
---

djLint est un linter de modèles twig et un formateur de modèles twig ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi Twig?](https://twig.symfony.com/)**

Les modèles Pebble (Java) sont compatibles Twig, utilisez donc ce même profil pour eux.

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

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
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
