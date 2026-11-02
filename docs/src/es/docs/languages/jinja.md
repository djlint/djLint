---
title: Linter y formateador de plantillas de Jinja
keywords: jinja, djlint, linter de plantillas jinja, formateador de plantillas jinja, formatear plantillas jinja, minijinja, jinjava, linter de plantillas minijinja, linter de plantillas jinjava
description: djLint analiza y formatea plantillas de Jinja. Usa el perfil jinja para que las reglas y el formato se ajusten a ellas.
tool: jinja
---

# {{ title }}

{{ description }}

**[¿Qué es Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Las plantillas de MiniJinja son totalmente compatibles con Jinja2, así que usa este mismo perfil `jinja`.

Las plantillas Jinjava de HubSpot también son de estilo jinja, así que usa también este perfil para ellas.

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
