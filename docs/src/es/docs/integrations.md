---
description: Integra djLint con tu editor favorito. Formatea automáticamente tus plantillas con Pre-Commit. Analiza tu código con SublimeText.
title: Integraciones
keywords: linter de plantillas, formateador de plantillas, djLint, HTML, plantillas, formateador, linter, integraciones, servidor de lenguaje, lsp, neovim, helix
---

# Integraciones

Existen varias integraciones de djLint con editores.

Uses el editor que uses, instala djLint donde el editor pueda encontrarlo, idealmente en el entorno virtual del proyecto, e inicia el editor desde ahí o indícale el `djlint` de ese entorno. Así el editor ejecuta la versión que fija tu proyecto, con los mismos resultados que tu hook de pre-commit o tu CI.

## Visual Studio Code

Instala la [extensión de djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), o [la de Open VSX](https://open-vsx.org/extension/monosans/djlint) para VSCodium. Busca djLint en tu entorno, recurre a uno incluido si no lo encuentra y usa el servidor de lenguaje cuando tu djLint lo tiene.

Su código está en [GitHub](https://github.com/djlint/djlint-vscode).

## Neovim

djLint se puede usar como linter y como formateador en Neovim.

### Cliente LSP integrado (recomendado)

Neovim 0.11 o posterior puede comunicarse directamente con el [servidor de lenguaje](#servidor-de-lenguaje) de djLint, sin ningún plugin. Así obtienes los problemas mientras escribes, con los rangos subrayados, y `vim.lsp.buf.format()` para formatear:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Para formatear al guardar, añade esto a la misma configuración:

```lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = {
    "*.html", "*.jinja", "*.jinja2", "*.j2",
    "*.hbs", "*.handlebars", "*.liquid", "*.gotmpl",
  },
  callback = function(args)
    vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
  end,
})
```

Consulta [Ajustes](#ajustes).

### conform.nvim y nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formatea y [nvim-lint](https://github.com/mfussenegger/nvim-lint) analiza el código, ejecutando djLint como comando. Los problemas no tienen rango subrayado y solo llegan cuando le pides a nvim-lint que analice.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

::: content

- [Repositorio de GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Análisis](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formato](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
:::

### efm-langserver

::: content

- [Repositorio de GitHub](https://github.com/mattn/efm-langserver)

1. Instala efm-langserver y djLint con Mason mediante `:MasonInstall efm djlint`
1. Añade `htmldjango` a `filetypes`.
1. Crea la configuración de formato:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Conecta el lenguaje con el formateador mediante `htmldjango = { djlint }`.

Configuración de ejemplo:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}

require("lspconfig").efm.setup({
    filetypes = { "htmldjango" },
    init_options = { documentFormatting = true },
    settings = {
        rootMarkers = { ".git/" },
        languages = {
            htmldjango = { djlint },
        },
    },
})
```

:::

### coc.nvim

::: content

- [Paquete de npm](https://www.npmjs.com/package/coc-htmldjango)
:::

## IDE de JetBrains

En PyCharm y los demás IDE basados en IntelliJ, usa el plugin gratuito [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Instala LSP4IJ desde el Marketplace.
1. Abre la ventana de herramientas LSP Consoles y añade un nuevo servidor de lenguaje.
1. En la pestaña **Server**, pon `djLint` como nombre y `djlint --lsp` como comando, con la ruta completa del `djlint` del entorno virtual del proyecto si no está en el PATH.
1. En la pestaña **Mappings**, añade un patrón de nombres de archivo para tus plantillas, como `*.html`. Si la configuración del proyecto no tiene [perfil](/es/docs/configuration/#profile), pon `htmldjango` como ID de lenguaje en un proyecto de Django, para que se elija el correcto.
1. En la pestaña **Configuration**, puedes definir [ajustes](#ajustes) en JSON, bajo una clave `djlint`.

Los problemas aparecen en el editor, y **Reformat Code** puede usar el servidor para los archivos asociados.

## Sublime Text

### LSP (recomendado)

El paquete [LSP](https://packagecontrol.io/packages/LSP) ejecuta el [servidor de lenguaje](#servidor-de-lenguaje), que muestra los problemas mientras escribes y permite formatear.

Ejecuta **Preferences: LSP Server Configurations** y añade:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

djLint se puede usar como plugin de linter de SublimeText. Se puede instalar mediante [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shift + p`
2. Instala SublimeLinter
3. Instala SublimeLinter-contrib-djlint
:::

Asegúrate de que djLint esté instalado en tu Python global o en tu `PATH`.

## Helix

Helix puede ejecutar el [servidor de lenguaje](#servidor-de-lenguaje) desde `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, que viene incluido en Emacs 29 y posteriores:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Después ejecuta `M-x eglot` en una plantilla. `eglot-format-buffer` la formatea.

## Servidor de lenguaje

`djlint --lsp` ejecuta djLint como servidor de lenguaje a través de stdio. Se mantiene en ejecución, así que un editor recibe los problemas mientras escribes y formatea un documento sin iniciar un proceso cada vez.

Informa de los problemas y formatea documentos completos. No necesita paquetes adicionales. Cualquier otro editor compatible con LSP puede ejecutarlo con el mismo comando.

### Ajustes

El servidor lee la [configuración](/es/docs/configuration/) del proyecto igual que la línea de comandos, desde la carpeta de cada archivo hacia arriba. Los ajustes del editor prevalecen sobre ella, pero, igual que en la línea de comandos, solo pueden activar una opción o asignar un valor: `false` no desactiva lo que el proyecto activa. Usan los nombres de las [opciones de la línea de comandos](/es/docs/configuration/), con guiones bajos o en camelCase, y se pueden usar listas para los valores separados por comas:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

El servidor pide la sección `djlint` con `workspace/configuration`. Un editor que no pueda responder puede enviar las mismas claves en `initializationOptions`.

Hay dos ajustes que no tienen opción de línea de comandos:

- `use_editor_indentation`: formatea con el tamaño de tabulación del editor, en lugar de `indent`.
- `python_rules`: ponlo en `false` para omitir las reglas personalizadas con un `python_module`, lo que impide que se ejecute el código del proyecto.

djLint toma el `profile` de la primera de estas fuentes que tenga uno:

1. Los ajustes del editor.
1. La configuración del proyecto.
1. El lenguaje del documento: `htmldjango` ejecuta el perfil `django`, por ejemplo.

Si no hay ninguno, se ejecuta sin perfil, igual que en la línea de comandos. Un `profile` en la configuración del proyecto es la opción más sencilla: funciona en cualquier editor, sin ningún ID de lenguaje que configurar.

### Qué hace

- Los problemas llegan tras una breve pausa al escribir. Un editor con diagnósticos de tipo pull los solicita, y a cualquier otro se le envían.
- `exclude`, `extend_exclude` y `use_gitignore` se aplican a los documentos abiertos. Un documento excluido no tiene problemas y no se formatea.
- Recarga la configuración cuando cambian `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` o `.gitignore`, si el editor puede vigilar archivos, y si no, cuando se abre o se guarda un documento. Los archivos indicados por `configuration` o `rules` se vuelven a leer cuando se abre o se guarda un documento. Un cambio en el código del `python_module` de una regla personalizada requiere reiniciar.
- Una regla lenta retrasa lo que viene después, porque el servidor hace una sola cosa a la vez.

## GitHub Actions

En un flujo de trabajo de GitHub Actions, djLint informa de cada problema como una anotación, para que aparezca en línea en el diff de una pull request. No hace falta configurar nada: djLint detecta el flujo de trabajo y cambia la salida automáticamente.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Usa `--no-github-output` para obtener la salida de consola normal, o `--github-output` para forzar las anotaciones fuera de Actions.

Las anotaciones pertenecen a una sola pull request. Para conservar los problemas en la pestaña Security del repositorio, con historial entre ejecuciones, escríbelos en formato SARIF y sube el archivo:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

El paso de subida necesita el permiso `security-events: write` en el job o en el flujo de trabajo.

`--sarif` escribe un documento SARIF 2.1.0 en stdout y nada más, así que se puede redirigir como arriba. Se listan todas las reglas activadas con un enlace a su documentación, cada problema lleva su línea y su columna, y con `--check` un archivo que se reformatearía se notifica bajo una regla `formatting`. Azure DevOps, GitLab y la mayoría de los editores leen el mismo formato.

## Pre-Commit

djLint se puede usar como hook de [pre-commit](https://pre-commit.com), tanto de linter como de formateador.

El repositorio ofrece varios hooks preconfigurados para perfiles concretos de djLint (simplemente predefinen el argumento `--profile` y le indican a pre-commit qué extensiones de archivo buscar):

::: content

- `djlint` para analizar y `djlint-reformat` para formatear
  Buscará archivos que coincidan con `*.html` sin definir `--profile`.
- `djlint-django` y `djlint-reformat-django`
  Buscará archivos que coincidan con `*.html` y definirá `--profile=django`.
- `djlint-jinja` y `djlint-reformat-jinja`
  Buscará archivos que coincidan con `*.j2`,`*.jinja` o `*.jinja2` y definirá `--profile=jinja`.
- `djlint-nunjucks` y `djlint-reformat-nunjucks`
  Buscará archivos que coincidan con `*.njk` y definirá `--profile=nunjucks`.
- `djlint-handlebars` y `djlint-reformat-handlebars`
  Buscará archivos que coincidan con `*.hbs` y definirá `--profile=handlebars`.
- `djlint-liquid` y `djlint-reformat-liquid`
  Buscará archivos que coincidan con `*.html` y definirá `--profile=liquid`.
- `djlint-golang` y `djlint-reformat-golang`
  Buscará archivos que coincidan con `*.gotmpl` y definirá `--profile=golang`.
- `djlint-tera` y `djlint-reformat-tera`
  Buscará archivos que coincidan con `*.html` y definirá `--profile=tera`.
- `djlint-askama` y `djlint-reformat-askama`
  Buscará archivos que coincidan con `*.html` y definirá `--profile=askama`.
:::

Ten en cuenta que estos hooks predefinidos a veces son demasiado conservadores con las entradas que aceptan (puede que tus plantillas usen otra extensión), por lo que pre-commit te permite explícitamente sobrescribir cualquiera de estas opciones predefinidas. Consulta la [documentación de pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks) para más opciones de configuración.

### Ejemplo predeterminado para Django

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars con la extensión .html en lugar de .hbs

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-handlebars
        files: "\\.html"
        types_or: ["html"]
      - id: djlint-handlebars
        files: "\\.html"
        types_or: ["html"]
```

Puedes usar los parámetros `files` o `exclude` para limitar cada hook a su propio directorio, lo que te permite trabajar con varios lenguajes de plantillas en el mismo repositorio.

## MegaLinter

djlint viene integrado de forma nativa entre los más de 100 linters de [MegaLinter](https://megalinter.io)

Para instalarlo, simplemente ejecuta `npx mega-linter-runner --install` y sigue las instrucciones

::: content

- [Repositorio de GitHub](https://github.com/oxsecurity/megalinter)
- [djlint en la documentación de MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
:::
