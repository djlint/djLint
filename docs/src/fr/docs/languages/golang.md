---
title: Go Template Linter and Formatter
keywords: go templates, golang, djlint, go template linter, go template formatter, golang template linter, golang template formatter, format go templates, hugo template linter, helm template linter
description: djLint est un linter de modèles Go et un formateur de modèles Go ! Profitez du profil pré-construit lorsque vous limez et formatez vos modèles avec djLint.
tool: golang
---

# {{ title }}

{{ description }}

**[C'est quoi les modèles Go ?](https://pkg.go.dev/text/template)**

Les modèles Go (`text/template`, `html/template`) sont aussi utilisés par les thèmes Hugo et les charts Helm, utilisez donc ce même profil pour eux.

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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>
