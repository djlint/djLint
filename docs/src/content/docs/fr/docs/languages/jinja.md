---
title: "Jinja Template Linter and Formatter"
description: "djLint est un linter de modèle jinja et un formateur de modèle jinja ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Jinja"
---

djLint est un linter de modèle jinja et un formateur de modèle jinja ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Les modèles MiniJinja sont entièrement compatibles avec Jinja2, utilisez donc ce même profil `jinja`.

Les modèles Jinjava de HubSpot sont également de style jinja, utilisez donc aussi ce profil pour eux.

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=jinja
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile="jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile="jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
