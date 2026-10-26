---
title: "Django Template Linter and Formatter"
description: "djLint est un linter de modèles django et un formateur de modèles django ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Django"
---

djLint est un linter de modèles django et un formateur de modèles django ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=django
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
