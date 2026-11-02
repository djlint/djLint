---
title: Linter y formateador de plantillas de Go
keywords: plantillas go, golang, djlint, linter de plantillas go, formateador de plantillas go, linter de plantillas golang, formateador de plantillas golang, formatear plantillas go, linter de plantillas hugo, linter de plantillas helm
description: ¡djLint es un linter y un formateador de plantillas de Go! Aprovecha el perfil predefinido al analizar y formatear tus plantillas con djLint.
tool: golang
---

# {{ title }}

{{ description }}

**[¿Qué son las plantillas de Go?](https://pkg.go.dev/text/template)**

Las plantillas de Go (`text/template`, `html/template`) también son la base de los temas de Hugo y los charts de Helm, así que usa este mismo perfil para ellos.

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
