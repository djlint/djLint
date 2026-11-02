---
title: Linter y formateador de plantillas de Nunjucks
keywords: nunjucks, djlint, linter de plantillas nunjucks, formateador de plantillas nunjucks, formatear plantillas nunjucks, pebble, linter de plantillas pebble
description: djLint analiza y formatea plantillas de Nunjucks. Usa el perfil nunjucks para que las reglas y el formato se ajusten a ellas.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[¿Qué es Nunjucks?](https://mozilla.github.io/nunjucks/)**

Las plantillas de Pebble (Java) son compatibles con Twig, así que usa este mismo perfil para ellas.

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
