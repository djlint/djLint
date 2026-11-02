---
title: Linter de plantillas de Angular
keywords: angular, djlint, linter de plantillas angular, analizar plantillas angular
description: djLint analiza plantillas de Angular. Usa el perfil angular para que las reglas se ajusten a ellas.
tool: angular
---

# {{ title }}

{{ description }}

**[¿Qué es Angular?](https://angular.io/guide/template-syntax)**

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
