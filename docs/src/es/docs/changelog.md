---
description: Registro de cambios de djLint. Consulta las novedades de las versiones recientes y qué funcionalidades puedes esperar en tu próxima actualización.
title: Registro de cambios
keywords: linter de plantillas, formateador de plantillas, djLint, HTML, plantillas, formateador, linter, registro de cambios
---

{% raw %}

# Registro de cambios

El registro de cambios ahora se incluye en cada [versión](https://github.com/djlint/djLint/releases).

## 1.0.2

::: content

- Corrección de errores [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- Corrección de errores [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- Corrección de errores [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- Corrección de errores [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- Se añadió la opción `--warn` para devolver los errores como advertencias.
  :::

## 0.7.5

::: content

- Corrección de errores [#187](https://github.com/djlint/djLint/issues/187)
- Se mejoró la compatibilidad con el front matter de `yaml` en los archivos de plantilla
- Se añadió la regla T032 para [#123](https://github.com/djlint/djLint/issues/123)
- Se añadió la regla H033 para [#124](https://github.com/djlint/djLint/issues/124)
- Los perfiles del linter pasaron a ser inclusivos en lugar de exclusivos para [#178](https://github.com/djlint/djLint/issues/178)
- Se añadió `.djlintrc` como archivo de configuración alternativo para [#188](https://github.com/djlint/djLint/issues/188)
  :::

## 0.7.4

::: content

- Corrección de errores [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- Corrección de errores [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Se eliminó Py3.6 de `pyproject.toml`.
  :::

## 0.7.2

::: content

- Corrección de errores [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- Corrección de errores [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- Se añadió configuración para etiquetas HTML personalizadas
- Corrección de errores
  :::

## 0.6.9

::: content

- Se añadieron los perfiles HTML y Angular
- Se permitieron algunas entidades en la regla #H023
- Corrección de errores
  :::

## 0.6.8

::: content

- Corrección de errores
- Se actualizó la documentación
  :::

## 0.6.7

::: content

- Se añadió la opción de configuración `format_attribute_template_tags` para activar de forma opcional el formateo de las etiquetas de plantilla dentro de los atributos
- Se añadió la opción de configuración `linter_output_format` para personalizar el orden de las variables del mensaje del linter
- Se añadieron las reglas H030 y H031 para comprobar las etiquetas meta
  :::

## 0.6.6

::: content

- Corrección de errores
  :::

## 0.6.5

::: content

- Las rutas de salida pasaron a ser relativas a la raíz del proyecto
- Corrección de errores
  :::

## 0.6.4

::: content

- Corrección de errores
  :::

## 0.6.3

::: content

- Se añadió compatibilidad con la etiqueta `blocktrans` de django
- Corrección de errores
  :::

## 0.6.2

::: content

- Corrección de errores
  :::

## 0.6.1

::: content

- Corrección de errores
- La regla T028 pasó a ser más estricta y con un mensaje más claro
  :::

## 0.6.0

::: content

- Se añadió la regla T027 para detectar cadenas sin cerrar en la sintaxis de plantilla
- Se añadió la regla T028 para detectar la falta de etiquetas con control de espacios en los atributos
- Se añadió la regla H029 para comprobar que el method de los formularios esté en minúsculas
- El formateador ahora ignora las etiquetas blocktranslate de django que no tienen "trimmed"
- Corrección de errores
  :::

## 0.5.9a

::: content

- Se añadió compatibilidad con python 3.10 en las pruebas
- Se añadió un hook de pre-commit
  :::

## 0.5.9

::: content

- Se añadió la opción `--use-gitignore` para ampliar las exclusiones
- Se cambió la detección de las exclusiones por defecto
- Se corrigieron las rutas de exclusión en windows
- Se corrigió el formateo de las etiquetas `{%...%}` en los atributos
- Se corrigió el formateo de los bucles for y de las condiciones anidadas en los atributos
  :::

## 0.5.8

::: content

- Se añadió la opción require_pragma
- Se actualizó DJ018 para detectar `data-src` y `action` en los inputs
- Se corrigió la sintaxis para ignorar en línea
- Se añadió la opción `--lint` como marcador para el uso por defecto
- Corrección de errores
  :::

## 0.5.7

::: content

- Corrección de errores
  :::

## 0.5.6

::: content

- Se añadió la regla H026 para encontrar etiquetas id y class vacías
- Corrección de errores
  :::

## 0.5.5

::: content

- Se unificaron los ajustes y se simplificó el código
- Corrección de errores
  :::

## 0.5.4

::: content

- Se añadió la regla H020 para encontrar pares de etiquetas vacíos
- Se añadió la regla H021 para encontrar estilos en línea
- Se añadió la regla H022 para encontrar enlaces http
- Se añadió la regla H023 para encontrar referencias de entidad
- Se añadió la regla H024 para encontrar el type en scripts y estilos
- Se añadió la regla H025 para comprobar las etiquetas huérfanas. Gracias a https://stackoverflow.com/a/1736801/10265880
- Se mejoró el formateo de los atributos
- Se actualizó la opción `blank_line_after_tag` para añadir un salto de línea sin importar la posición
- Se corrigió el formateo de la etiqueta `trans` de django
- Se añadió el formateo de los estilos en línea
- Se añadió el formateo de las condiciones de plantilla dentro de los atributos
- Se añadió srcset como posible ubicación de URL en las reglas del linter
- Se aceleró el formateo
- Un agradecimiento especial a [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- Se cambió la salida estándar de las opciones `--reformat/check` para que solo imprima el nuevo html cuando la entrada es stdin
  :::

## 0.5.2

::: content

- Se separó el requisito de `alt` de H006 en H013
- Se añadió un archivo opcional de reglas personalizadas
- Se añadió `golang` como opción de perfil
- Se corrigió el formateo de los bloques ignorados que contienen comentarios en línea
- Se añadió texto por defecto a las opciones `--indent` y `-e`
- Las reglas de URL ahora aceptan #
- Se corrigió la codificación de archivos en Windows
- Se corrigió la expresión regular de las etiquetas de plantilla de una sola línea
- Se corrigió `blank_line_after_tag` en las etiquetas con espacio inicial
  :::

## 0.5.1

::: content

- Se añadió la regla H019
- Se corrigieron errores en DJ018 y H012
  :::

## 0.5.0

::: content

- Se corrigieron varios errores de coincidencia de expresiones regulares en las reglas del linter
- El linter ya no devuelve errores en los bloques ignorados
- Se añadió la opción de ignorar un bloque de código en el linter o el formateador con las etiquetas `{% djlint:off %}...{% djlint:on %}`
  :::

## 0.4.9

::: content

- Se corrigió el error [#35](https://github.com/djlint/djLint/issues/35)
  :::

## 0.4.8

::: content

- Se corrigió el error [#34](https://github.com/djlint/djLint/issues/34)
  :::

## 0.4.7

::: content

- La etiqueta `source` pasó a las etiquetas de una sola línea
  :::

## 0.4.6

::: content

- Se corrigió el error [#31](https://github.com/djlint/djLint/issues/31)
  :::

## 0.4.5

::: content

- Se añadieron buenas prácticas a la documentación
- Se añadió la opción `--profile` para definir las reglas por defecto del linter y del formateador
- Se añadieron reglas del linter para los patrones de URL de jinja
  :::

## 0.4.4

::: content

- La configuración de indentación pasó de cadena a entero. `--indent 3`
  :::

## 0.4.3

::: content

- Se añadió una opción de línea de comandos para el espaciado de la indentación. `--indent=" "`
  :::

## 0.4.2

::: content

- Se añadió la posibilidad de añadir espacio en blanco adicional después de las etiquetas con la opción `blank_line_after_tag`
  :::

## 0.4.1

::: content

- Se añadió la posibilidad de procesar varios archivos o carpetas a la vez
  :::

## 0.4.0

::: content

- Se corrigió el formateo de las etiquetas `{# ... #}` de django
- Se añadió la indentación de las etiquetas figcaption, details y summary
- Se añadió la posibilidad de sobrescribir o ampliar la lista de rutas excluidas en `pyproject.toml`
  :::

## 0.3.9

::: content

- Se actualizó el tratamiento de los atributos
  :::

## 0.3.8

::: content

- Se añadió compatibilidad con stdin
  :::

## 0.3.7

::: content

- Se corrigió el formateo de las etiquetas `small`, `dt` y `dd`
  :::

## 0.3.6

::: content

- El formateador ahora admite los bloques de apertura `{%-` de Nunjucks
  :::

## 0.3.5

::: content

- Se añadió compatibilidad con más bloques de Django
- Se añadió compatibilidad con bloques personalizados
- Se añadió compatibilidad con la configuración en `pyproject.toml`
  :::

## 0.3.4

::: content

- Se corrigió el formato de la etiqueta con control de espacios `-%}` de Nunjucks
  :::

## 0.3.3

::: content

- Las etiquetas `div` cortas ahora pueden quedar en una sola línea
  :::

## 0.3.2

::: content

- Se corrigió el formateo de los comentarios de Django
- El formateador ahora ignora textarea
  :::

## 0.3.1

::: content

- Se actualizó la expresión regular del formateo de atributos
- Se actualizó la regla del linter W010
  :::

## 0.3.0

::: content

- El código de salida pasa a ser 1 si hubo algún cambio de formato
- Se añadió compatibilidad con las etiquetas `asset` de Jinja
  :::

## 0.2.9

::: content

- Se actualizó la expresión regular de W018
- Se eliminaron los mensajes del linter duplicados
- Se actualizó E001 para Handlebars
  :::

## 0.2.8

::: content

- Se corrigió un error de la barra de progreso con versiones antiguas de Click
  :::

{% endraw %}
