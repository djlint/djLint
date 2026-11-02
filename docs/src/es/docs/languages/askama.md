---
title: Linter y formateador de plantillas de Askama
keywords: askama, rust, djlint, linter de plantillas askama, formateador de plantillas askama, formatear plantillas askama
description: djLint analiza y formatea plantillas de Askama. Usa el perfil askama para que las reglas y el formato se ajusten a ellas.
tool: askama
---

# {{ title }}

{{ description }}

**[¿Qué es Askama?](https://askama.readthedocs.io/)**

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
