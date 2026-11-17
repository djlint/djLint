---
title: "Integraciones"
description: "Usa djLint en tu editor y ejecútalo con pre-commit."
---

Uses el editor que uses, instala djLint donde el editor pueda encontrarlo, idealmente en el entorno virtual del proyecto, e inicia el editor desde ahí o indícale el `djlint` de ese entorno. Así el editor ejecuta la versión que fija tu proyecto, con los mismos resultados que tu hook de pre-commit o tu CI.

## Visual Studio Code

Instala la [extensión de djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) desde Visual Studio Marketplace. Cursor, Windsurf, VSCodium y otros editores basados en VS Code instalan [la misma extensión desde Open VSX](https://open-vsx.org/extension/monosans/djlint). Busca djLint en tu entorno, recurre a uno incluido si no lo encuentra y usa el servidor de lenguaje cuando tu djLint lo tiene.

Su [README](https://github.com/djlint/djlint-vscode#readme) describe sus ajustes y qué djLint ejecuta.

## Zed

La [extensión de djLint](https://github.com/djlint/djlint-zed) ejecuta el [servidor de lenguaje](#servidor-de-lenguaje) en HTML y en los lenguajes de las extensiones de plantillas, como Django, Jinja y Twig. Todavía no está en el registro de extensiones de Zed, así que instálala como extensión de desarrollo:

1. Instala Rust con [rustup](https://rustup.rs): Zed compila la extensión con él y añade por su cuenta el target `wasm32-wasip2`. Con un Rust de otra fuente, como Homebrew o Nix, añádelo tú.
1. Clona la extensión:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. En Zed, abre la paleta de comandos (`cmd-shift-p` en macOS, `ctrl-shift-p` en el resto), ejecuta **zed: install dev extension** y elige la carpeta clonada `djlint-zed`.

Para actualizarla, ejecuta `git pull` en esa carpeta y luego **zed: rebuild dev extension**.

Necesita djLint 1.49 o posterior en el PATH, o [uv](https://docs.astral.sh/uv/), que ejecuta djLint sin instalarlo. Su [README](https://github.com/djlint/djlint-zed#readme) explica cómo convertirla en el formateador de un lenguaje y cuáles son sus ajustes.

## Neovim

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

- [Repositorio de GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Análisis](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formato](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [Repositorio de GitHub](https://github.com/mattn/efm-langserver)

Dale a `htmldjango` un formateador con `formatCommand = "djlint --reformat --quiet --warn --stdin-filename '${INPUT}' -"` y `formatStdin = true`.

### coc.nvim

- [Paquete de npm](https://www.npmjs.com/package/coc-htmldjango)

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

Instala SublimeLinter y [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) con Package Control. djLint tiene que estar en el PATH que ve Sublime Text.

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

`--sarif` escribe un documento SARIF 2.1.0 en stdout y nada más, así que se puede redirigir como arriba. Se listan todas las reglas activadas con un enlace a su documentación, cada problema lleva su línea y su columna, y con `--check` un archivo que se reformatearía se notifica bajo una regla `formatting`.

## pre-commit

djLint se puede usar como hook de [pre-commit](https://pre-commit.com), tanto de linter como de formateador.

Cada uno de estos perfiles tiene un hook que analiza, el de la lista, y otro que formatea, con el mismo nombre más `reformat`: `djlint-reformat-django` para `djlint-django`. Definen `--profile` y los archivos que pasa pre-commit. `angular` no tiene hooks propios: añade `args: [--profile=angular]` a `djlint` o a `djlint-reformat`.

| Hook                | Perfil     | Archivos                             |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | ninguno    | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Para plantillas con otras extensiones, sobrescribe `files` en tu configuración, y también `types_or` si el hook lo define, ya que pre-commit necesita que coincidan los dos. Consulta la [documentación de pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

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

[MegaLinter](https://megalinter.io) incluye djLint. Ejecuta `npx mega-linter-runner --install` para configurarlo, y consulta [su página de djLint](https://megalinter.io/latest/descriptors/html_djlint/) para ver las opciones.
