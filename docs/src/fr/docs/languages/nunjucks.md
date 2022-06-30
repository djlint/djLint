---
title: Nunjucks Template Linter and Formatter
keywords: nunjucks, djlint, nunjucks template linter, nunjucks template formatter, format nunjucks templates
description: djLint est un linter de modèle nunjucks et un formateur de modèle nunjucks ! Profitez du profil pré-construit lorsque vous limez et formatez vos modèles avec djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[C'est quoi Nunjucks?](https://mozilla.github.io/nunjucks/)**

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans votre projet `pyproject.toml`.

```toml
[tool.djlint]
profile="{{ tool }}"
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/fr/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>
