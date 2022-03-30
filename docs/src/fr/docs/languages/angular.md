---
title: Angular Template Linter
keywords: angular, djlint, angular template linter, lint angular templates
description: djLint est un linter de template angulaire ! Profitez du profil pré-build lorsque vous linting et formatez vos templates avec djLint.
tool: angular
---

# {{ title }}

{{ description }}

**[C'est quoi Angular?](https://angular.io/guide/template-syntax)**

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
