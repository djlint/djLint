---
title: "Askama Template Linter and Formatter"
description: "djLint est un linter de modèle Askama et un formateur de modèle Askama ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Askama"
---

djLint est un linter de modèle Askama et un formateur de modèle Askama ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi Askama?](https://askama.readthedocs.io/)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=askama
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile="askama"
```

```toml title="djlint.toml / .djlint.toml"
profile="askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
