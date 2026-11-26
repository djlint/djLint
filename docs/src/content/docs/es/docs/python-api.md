---
title: "API de Python"
description: "Formatea y analiza plantillas desde tu propio código Python con la API de djLint."
---

`djlint.api` formatea y analiza texto desde un programa en Python, con los mismos resultados que la línea de comandos. Está pensado para editores, herramientas de compilación y cualquier otra cosa que tenga una plantilla en memoria. Todo lo demás del paquete puede cambiar en cualquier versión, así que usa este módulo en lugar de `djlint.settings` o `djlint.lint`. Las funciones auxiliares que importa el [ejemplo de regla personalizada](/es/docs/linter/#reglas-con-modulos-de-python), `djlint.lint.get_line`, `djlint.helpers.inside_ignored_rule` y `djlint.helpers.inside_ignored_linter_block`, también siguen funcionando.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, on_warning=None, **options)` lee la configuración que se aplica a los archivos de una carpeta. La busca hacia arriba a partir de la carpeta, igual que la línea de comandos [lo hace](/es/docs/configuration/) desde la primera ruta que recibe, y no cambia el directorio actual.

Las opciones usan los nombres de las opciones de la línea de comandos, con guiones bajos, y funcionan igual que allí: un valor definido prevalece sobre el archivo de configuración, mientras que `False`, una cadena vacía y, en la mayoría de las opciones, `0` cuentan como no indicados. Las rutas se pasan como `pathlib.Path`.

Leer la configuración lleva algo de tiempo, así que conserva el resultado mientras no cambien los archivos de los que se leyó. Se puede usar con cualquier número de textos.

Con `python_rules=False`, no se cargan las reglas personalizadas con un `python_module`, lo que impide que se ejecute el código de un proyecto en el que no confías. Sus nombres quedan en `config.skipped_rules`.

`on_warning`, una función que toma un mensaje, recibe cada aviso sobre los ajustes, como un nombre mal escrito o un código de regla que no corresponde a ninguna regla. Sin ella, cada aviso va a stderr una vez por proceso. Un archivo de configuración que no se puede leer, o un valor no válido, lanza `click.UsageError`.

## format_text

`format_text(config, text)` devuelve el texto formateado. Un texto cuya primera línea termina en CRLF se devuelve en CRLF, y cualquier otro, en LF. Con `require_pragma`, un texto sin el pragma se devuelve sin cambios. Si ni las opciones de `load_config` ni el archivo de configuración definen `indent` o `max_line_length`, los toma de las secciones del `.editorconfig` que se aplican a un archivo de la extensión configurada en la carpeta que se pasa a `load_config`, mientras que la línea de comandos los toma para cada archivo según su ruta.

## lint_text

`lint_text(config, text, filename="-")` devuelve una lista de `Finding`, en el orden del documento. `filename` es lo que se compara con `per-file-ignores`. Con `require_pragma`, un texto sin el pragma no tiene problemas.

`Finding` es una named tuple con estos campos:

- `code`: el código de la regla, como `H013`.
- `message`: lo que dice la regla.
- `match`: el comienzo del texto encontrado, hasta 20 caracteres.
- `line`, `column`: dónde empieza el problema. Las líneas se cuentan desde 1, y las columnas, desde 0.
- `end_line`, `end_column`: justo después de donde termina, que puede estar en una línea posterior.

Las columnas cuentan caracteres, no bytes ni unidades de código UTF-16.

## is_excluded

`is_excluded(config, path)` indica si `exclude`, `extend_exclude` o el gitignore dejan fuera un archivo, igual que hace la línea de comandos. `format_text` y `lint_text` no lo comprueban por sí mismas.

## Módulos de reglas

El `python_module` de una regla personalizada se importa una vez por proceso, desde la raíz del proyecto de la configuración. Para leer las reglas de otro proyecto, un programa que se mantiene en ejecución tiene que quitar de `sys.modules` todo lo que importó del primer proyecto, y quitar la raíz de ese proyecto del final de `sys.path`.
