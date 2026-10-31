---
title: "Liquid Template Linter and Formatter"
description: "djLint est un linter de modèle Liquid et un formateur de modèle Liquid ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Liquid"
---

djLint est un linter de modèle Liquid et un formateur de modèle Liquid ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi Liquid?](https://shopify.github.io/liquid/)**

Un seul profil couvre tous les dialectes Liquid : les thèmes Shopify, Jekyll, LiquidJS (Eleventy) et Fluid (Orchard Core).

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=liquid
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

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
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
