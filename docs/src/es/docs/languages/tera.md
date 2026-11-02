---
title: Linter y formateador de plantillas de Tera
keywords: tera, rust, zola, djlint, linter de plantillas tera, formateador de plantillas tera, formatear plantillas tera
description: djLint analiza y formatea plantillas de Tera. Usa el perfil tera para que las reglas y el formato se ajusten a ellas.
tool: tera
---

# {{ title }}

{{ description }}

**[¿Qué es Tera?](https://keats.github.io/tera/)**

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile={{ tool }}
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">¡Consulta la guía de configuración para ver todas las opciones!</a></div>
</div>
