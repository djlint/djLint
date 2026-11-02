---
title: "Linter et formateur de templates Django"
description: "djLint est un linter de templates django et un formateur de templates django ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint."
sidebar:
  label: "Django"
---

djLint est un linter de templates django et un formateur de templates django ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.

**[Qu'est-ce que Django ?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### En ligne de commande

```bash
djlint /path/to/templates --profile=django
```

#### Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
