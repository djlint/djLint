---
title: "Integrações"
description: "Use o djLint no seu editor e execute-o com o pre-commit."
---

Seja qual for o seu editor, instale o djLint onde o editor consiga encontrá-lo, de preferência no ambiente virtual do projeto, e abra o editor a partir dele ou aponte-o para o `djlint` desse ambiente. Assim, o editor executa a versão fixada pelo seu projeto, com os mesmos resultados do seu hook de pre-commit ou da CI.

Se o projeto instala o djLint com o [npm](/pt-br/docs/getting-started/#instalacao), o comando dele é `node_modules/.bin/djlint` no projeto, ou `node_modules/.bin/djlint.cmd` no Windows. As versões do djLint no npm anteriores à 1.54.0 não o têm. Onde um editor abaixo executa `djlint`, informe esse caminho. O caminho é relativo: se o editor executa o djLint de uma pasta diferente da que tem `node_modules`, informe o caminho completo. As extensões para VS Code e Zed o encontram sozinhas.

## Visual Studio Code

Instale a [extensão do djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) pelo Visual Studio Marketplace. Cursor, Windsurf, VSCodium e outros editores baseados no VS Code instalam [a mesma extensão pelo Open VSX](https://open-vsx.org/extension/monosans/djlint). Ela encontra o djLint no seu ambiente ou, na falta dele, usa um embutido, e usa o servidor de linguagem quando o seu djLint o oferece.

O [README](https://github.com/djlint/djlint-vscode#readme) dela descreve as configurações e qual djLint ela executa.

## Zed

A [extensão do djLint](https://github.com/djlint/djlint-zed) executa o [servidor de linguagem](#servidor-de-linguagem) no HTML e nas linguagens das extensões de templates, como Django, Jinja e Twig. Ela ainda não está no registro de extensões do Zed. O [README](https://github.com/djlint/djlint-zed#readme) dela explica como instalá-la como extensão de desenvolvimento, qual djLint ela executa e como configurá-la.

## Neovim

O Neovim não dá filetype a algumas extensões de templates. Qualquer que seja a opção abaixo que você usar, registre-as primeiro:

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### Cliente LSP embutido (recomendado)

O Neovim 0.11 ou mais recente consegue se comunicar diretamente com o [servidor de linguagem](#servidor-de-linguagem) do djLint, sem nenhum plugin. Isso traz as ocorrências enquanto você digita, com os trechos sublinhados, e `vim.lsp.buf.format()` para a formatação.

O [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) a partir da v2.13.0 já traz a configuração do djLint, então com ele basta uma linha:

```lua
vim.lsp.enable("djlint")
```

Para o djLint instalado com npm no projeto, coloque `vim.lsp.config("djlint", { cmd = { "node_modules/.bin/djlint", "--lsp" } })` antes dessa linha, com `"node_modules/.bin/djlint.cmd"` no Windows.

Sem o nvim-lspconfig, ou com uma versão mais antiga, defina a configuração você mesmo:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = {
    "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
    "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
  },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Em ambos os casos, o Neovim não formata ao salvar por conta própria. Para isso, adicione também isto à sua configuração:

```lua
local group = vim.api.nvim_create_augroup("djlint_format", {})
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    if vim.lsp.get_client_by_id(args.data.client_id).name ~= "djlint" then
      return
    end
    vim.api.nvim_clear_autocmds({ group = group, buffer = args.buf })
    vim.api.nvim_create_autocmd("BufWritePre", {
      group = group,
      buffer = args.buf,
      callback = function()
        vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
      end,
    })
  end,
})
```

Veja [Configurações](#configuracoes).

### conform.nvim e nvim-lint

O [conform.nvim](https://github.com/stevearc/conform.nvim) formata e o [nvim-lint](https://github.com/mfussenegger/nvim-lint) faz o lint, executando o djLint como um comando. As ocorrências não têm trecho sublinhado e só chegam quando você pede ao nvim-lint para fazer o lint. O perfil vem da [configuração](/pt-br/docs/configuration/#profile) do projeto, como na linha de comando. Este exemplo precisa do djLint 1.49 ou mais recente.

```lua
local formatters, linters = {}, {}
for _, filetype in ipairs({
  "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
  "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
}) do
  formatters[filetype] = { "djlint" }
  linters[filetype] = { "djlint" }
end
require("conform").setup({
  formatters_by_ft = formatters,
  formatters = { djlint = { prepend_args = { "--stdin-filename", "$FILENAME" } } },
})
local lint = require("lint")
lint.linters_by_ft = linters
vim.list_extend(lint.linters.djlint.args, {
  "--stdin-filename",
  function()
    return vim.api.nvim_buf_get_name(0)
  end,
})
```

### none-ls

- [Repositório no GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatação](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [Pacote npm](https://www.npmjs.com/package/coc-htmldjango)

## IDEs da JetBrains

No PyCharm e nas outras IDEs baseadas no IntelliJ, use o plugin gratuito [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Instale o LSP4IJ pelo Marketplace.
1. Abra a janela de ferramentas LSP Consoles e adicione um novo servidor de linguagem.
1. Na aba **Server**, defina o nome como `djLint` e o comando como `djlint --lsp`, com o caminho completo do `djlint` no ambiente virtual do projeto, caso ele não esteja no PATH.
1. Na aba **Mappings**, adicione os padrões de nome de arquivo dos seus templates. Se a configuração do projeto não tiver um [perfil](/pt-br/docs/configuration/#profile), o ID de linguagem de cada padrão o escolhe:

   | Padrões                               | ID de linguagem                   |
   | ------------------------------------- | --------------------------------- |
   | `*.html`, `*.htm`                     | `html`, ou `htmldjango` no Django |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                           |
   | `*.njk`, `*.twig`                     | `nunjucks`                        |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                      |
   | `*.liquid`                            | `liquid`                          |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                          |
   | `*.tera`                              | `tera`                            |
   | `*.mako`                              | `mako`                            |

1. Na aba **Configuration**, você pode definir as [configurações](#configuracoes) em JSON, sob a chave `djlint`.

As ocorrências aparecem no editor, e o **Reformat Code** pode usar o servidor para os arquivos mapeados.

## Sublime Text

### LSP (recomendado)

O pacote [LSP](https://packagecontrol.io/packages/LSP) executa o [servidor de linguagem](#servidor-de-linguagem), que traz as ocorrências enquanto você digita e a formatação.

Execute **Preferences: LSP Server Configurations** e adicione:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

Instale o SublimeLinter e o [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) pelo Package Control. O djLint precisa estar no PATH que o Sublime Text enxerga.

## Helix

O Helix pode executar o [servidor de linguagem](#servidor-de-linguagem) a partir do `languages.toml`. Uma lista `language-servers` substitui a que o Helix tem para essa linguagem, então mantenha os servidores dele depois de `djlint`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server", "superhtml"]

[[language]]
name = "htmldjango"
language-servers = ["djlint", "djlsp", "vscode-html-language-server", "superhtml"]

[[language]]
name = "gotmpl"
language-servers = ["djlint", "gopls"]

[[language]]
name = "jinja"
language-servers = ["djlint"]

[[language]]
name = "nunjucks"
language-servers = ["djlint"]

[[language]]
name = "twig"
language-servers = ["djlint"]

[[language]]
name = "tera"
language-servers = ["djlint"]
```

O Helix não abre nenhum arquivo como `htmldjango` por conta própria. Em um projeto Django, adicione `file-types = ["html"]` a essa entrada no `.helix/languages.toml` do projeto.

## Emacs

Com o Eglot, que vem com o Emacs 29 e versões mais recentes:

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

Em seguida, execute `M-x eglot` em um template. `eglot-format-buffer` o formata. `html-mode`, `mhtml-mode` e `web-mode` não indicam uma linguagem de templates, então neles o perfil vem da [configuração](/pt-br/docs/configuration/#profile) do projeto.

## Agentes de programação

Os [plugins do djLint](https://github.com/djlint/agent-plugins) entregam ao Claude Code, Codex, GitHub Copilot CLI, Gemini CLI e OpenCode as ocorrências nos templates que eles editam, para que o agente as corrija antes de seguir em frente. O [README](https://github.com/djlint/agent-plugins#readme) deles explica como instalá-los e atualizá-los em cada agente, e como configurar o Crush, o Aider e os agentes que leem Agent Skills.

Um agente que trabalha no seu editor, como os do Cursor, Windsurf ou Zed, ou o Copilot no VS Code, vê em vez disso as ocorrências da extensão do djLint do editor.

## Servidor de linguagem

`djlint --lsp` executa o djLint como um servidor de linguagem via stdio. Ele continua em execução, então o editor recebe as ocorrências enquanto você digita e formata um documento sem iniciar um processo a cada vez.

Ele relata ocorrências e formata documentos inteiros. Não precisa de pacotes extras. Qualquer outro editor que suporte LSP pode executá-lo com o mesmo comando.

### Configurações

O servidor lê a [configuração](/pt-br/docs/configuration/) do projeto como a linha de comando faz, subindo a partir da pasta de cada arquivo. As configurações do editor prevalecem sobre ela, mas, assim como na linha de comando, só podem ativar uma opção ou definir um valor: `false` não desativa o que o projeto ativa. Elas usam os nomes das [opções da linha de comando](/pt-br/docs/configuration/), com sublinhados ou em camelCase, e listas podem ser usadas para valores separados por vírgula:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

O servidor solicita a seção `djlint` com `workspace/configuration`. Um editor que não consiga responder pode enviar as mesmas chaves em `initializationOptions`.

Duas configurações não têm opção correspondente na linha de comando:

- `use_editor_indentation`: Formata com o tamanho de tabulação do editor, em vez de `indent`.
- `python_rules`: Defina como `false` para pular as regras personalizadas com um `python_module`, o que impede que o código do projeto seja executado.

O djLint usa o `profile` da primeira destas fontes que tiver um:

1. As configurações do editor.
1. A configuração do projeto.
1. A linguagem do documento: `htmldjango` executa o perfil `django`, por exemplo.

Se nenhuma delas tiver, ele é executado sem perfil, como na linha de comando. Um `profile` na configuração do projeto é a opção mais simples: funciona em qualquer editor, sem nenhum ID de linguagem para configurar.

### O que ele faz

- As ocorrências chegam depois de uma breve pausa na digitação. Um editor com diagnósticos por pull as solicita, e qualquer outro as recebe por push.
- `exclude`, `extend_exclude` e `use_gitignore` se aplicam aos documentos abertos. Um documento excluído não tem ocorrências e não é formatado.
- Ele recarrega a configuração quando `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` ou `.gitignore` mudam, se o editor puder observar arquivos, e, caso contrário, quando um documento é aberto ou salvo. Os arquivos indicados por `configuration` ou `rules` são lidos novamente quando um documento é aberto ou salvo. Uma alteração no código do `python_module` de uma regra personalizada exige uma reinicialização.
- Uma regra lenta atrasa o que vem depois dela, porque o servidor faz uma coisa de cada vez.

## GitHub Actions

Em um workflow do GitHub Actions, o djLint relata cada ocorrência como uma anotação, para que ela apareça diretamente no diff de um pull request. Nenhuma configuração é necessária: o djLint detecta o workflow e muda a saída automaticamente.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Use `--no-github-output` para obter a saída simples do console, ou `--github-output` para forçar as anotações fora do Actions.

As anotações pertencem a um único pull request. Para manter as ocorrências na aba Security do repositório, com histórico entre as execuções, grave-as como SARIF e faça o upload do arquivo:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

A etapa de upload precisa da permissão `security-events: write` no job ou no workflow.

`--sarif` grava um documento SARIF 2.1.0 na stdout e nada mais, para que possa ser redirecionado como acima. Cada regra ativada é listada com um link para a sua documentação, cada ocorrência traz a sua linha e coluna e, com `--check`, um arquivo que seria reformatado é relatado sob uma regra `formatting`.

## pre-commit

O djLint pode ser usado como hook do [pre-commit](https://pre-commit.com), tanto como linter quanto como formatador.

Cada um destes perfis tem um hook que faz o lint, listado aqui, e um que formata, com o mesmo nome mais `reformat`: `djlint-reformat-django` para `djlint-django`. Eles definem o `--profile` e os arquivos que o pre-commit passa. `angular` não tem hooks próprios: passe `args: [--profile=angular]` para `djlint` ou `djlint-reformat`.

| Hook                | Perfil     | Arquivos                             |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | nenhum     | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Para templates com outras extensões, sobrescreva `files` na sua configuração, e também `types_or` quando o hook o define, já que o pre-commit exige que os dois correspondam. Veja a [documentação do pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

### Exemplo padrão para Django

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars com extensão .html em vez de .hbs

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

Você pode usar os parâmetros `files` ou `exclude` para restringir cada hook ao seu próprio diretório, o que permite usar várias linguagens de template no mesmo repositório.

## MegaLinter

O [MegaLinter](https://megalinter.io) inclui o djLint. Execute `npx mega-linter-runner --install` para configurá-lo. As opções estão na [página do djLint](https://megalinter.io/latest/descriptors/html_djlint/) do MegaLinter.
