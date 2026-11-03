---
title: Linter y formateador de plantillas de Mako
keywords: mako, python, pyramid, open edx, djlint, linter de plantillas mako, formateador de plantillas mako, formatear plantillas mako
description: djLint analiza y formatea plantillas de Mako. Usa el perfil mako para que las reglas y el formato se ajusten a ellas.
tool: mako
---

# {{ title }}

{{ description }}

**[¿Qué es Mako?](https://www.makotemplates.org/)**

Con el perfil mako, una línea de control como `% if x:` y un comentario `##` siempre ocupan una línea propia, y una etiqueta cuyos atributos dependen de líneas de control los conserva tal como se escribieron. Los bloques de Python y el contenido de `<%doc>` y `<%text>` no se tocan, ni tampoco un script o style que contiene sintaxis de Mako con `--format-js` o `--format-css`. Las líneas entre `% if` y `% endif`, y entre una etiqueta `<%block>` o `<%def>` y su etiqueta de cierre cuando cada una ocupa su propia línea, se indentan como cualquier otro bloque. El código de una expresión `${}` se queda tal como se escribió.

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
