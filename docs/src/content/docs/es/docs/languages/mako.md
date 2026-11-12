---
title: "Linter y formateador de plantillas de Mako"
description: "djLint analiza y formatea plantillas de Mako. Usa el perfil mako para que las reglas y el formato se ajusten a ellas."
sidebar:
  label: "Mako"
---

djLint analiza y formatea plantillas de Mako. Usa el perfil `mako` para que las reglas y el formato se ajusten a ellas.

**[¿Qué es Mako?](https://www.makotemplates.org/)**

Con el perfil mako, una línea de control como `% if x:` y un comentario `##` siempre ocupan una línea propia, y una etiqueta cuyos atributos dependen de líneas de control los conserva tal como se escribieron. Los bloques de Python y el contenido de `<%doc>` y `<%text>` no se tocan, ni tampoco un script o style que contiene sintaxis de Mako con `--format-js` o `--format-css`. Las líneas entre `% if` y `% endif`, y entre una etiqueta `<%block>` o `<%def>` y su etiqueta de cierre cuando cada una ocupa su propia línea, se indentan como cualquier otro bloque. El código de una expresión `${}` se queda tal como se escribió.

## Desde la línea de comandos

```bash
djlint /path/to/templates --profile=mako
```

## O bien, con un archivo de configuración

Configura djLint en el archivo `pyproject.toml`, `djlint.toml` / `.djlint.toml` o `.djlintrc` de tu proyecto.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[¡Consulta la guía de configuración para ver todas las opciones!](/es/docs/configuration/)
:::
