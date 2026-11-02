---
title: Linter y formateador de plantillas de Liquid
keywords: liquid, shopify, jekyll, eleventy, djlint, linter de plantillas liquid, formateador de plantillas liquid, formatear plantillas liquid, shopify, jekyll, eleventy, liquidjs, fluid, linter de temas shopify, linter de jekyll
description: djLint analiza y formatea plantillas de Liquid. Usa el perfil liquid para que las reglas y el formato se ajusten a ellas.
tool: liquid
---

# {{ title }}

{{ description }}

**[¿Qué es Liquid?](https://shopify.github.io/liquid/)**

Un solo perfil cubre todos los dialectos de Liquid: temas de Shopify, Jekyll, LiquidJS (Eleventy) y Fluid (Orchard Core).

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
