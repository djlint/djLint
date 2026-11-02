---
title: Linter y formateador de plantillas de Mustache
keywords: mustache, djlint, linter de plantillas mustache, formateador de plantillas mustache, formatear plantillas mustache
description: ¡djLint es un linter y un formateador de plantillas de mustache! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[¿Qué es Mustache?](https://mustache.github.io/mustache.5.html)**

#### Desde la línea de comandos

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">¡Consulta la guía de configuración para ver todas las opciones!</a></div>
</div>
