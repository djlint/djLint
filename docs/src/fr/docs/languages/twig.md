---
title: Twig Template Linter and Formatter
keywords: twig, djlint, twig template linter, twig template formatter, format twig templates
description: djLint est un linter de modèles twig et un formateur de modèles twig ! Profitez du profil pré-construit lorsque vous limez et formatez vos modèles avec djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

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
    <span class="icon is-large"><i class="fas fa-2x fa-arrow-circle-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/fr/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>