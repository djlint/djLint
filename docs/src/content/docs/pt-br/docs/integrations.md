---
title: "Integrações"
description: "Use o djLint no seu editor e execute-o com o pre-commit."
sidebar:
  label: "Integrações"
---

Existem várias integrações com editores criadas para o djLint.

Seja qual for o seu editor, instale o djLint onde o editor consiga encontrá-lo, de preferência no ambiente virtual do projeto, e abra o editor a partir dele ou aponte-o para o `djlint` desse ambiente. Assim, o editor executa a versão fixada pelo seu projeto, com os mesmos resultados do seu hook de pre-commit ou da CI.

## Visual Studio Code

Instale a [extensão do djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), ou [a do Open VSX](https://open-vsx.org/extension/monosans/djlint) para o VSCodium. Ela encontra o djLint no seu ambiente ou, na falta dele, usa um embutido, e usa o servidor de linguagem quando o seu djLint o oferece.

O código dela está no [GitHub](https://github.com/djlint/djlint-vscode).

## Neovim

O djLint pode ser usado como linter e formatador no Neovim.

### Cliente LSP embutido (recomendado)

O Neovim 0.11 ou mais recente consegue se comunicar diretamente com o [servidor de linguagem](#servidor-de-linguagem) do djLint, sem nenhum plugin. Isso traz as ocorrências enquanto você digita, com os trechos sublinhados, e `vim.lsp.buf.format()` para a formatação:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Para formatar ao salvar, adicione isto à mesma configuração:

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

Veja [Configurações](#configurações).

### conform.nvim e nvim-lint

O [conform.nvim](https://github.com/stevearc/conform.nvim) formata e o [nvim-lint](https://github.com/mfussenegger/nvim-lint) faz o lint, executando o djLint como um comando. As ocorrências não têm trecho sublinhado e só chegam quando você pede ao nvim-lint para fazer o lint.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [Repositório no GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatação](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [Repositório no GitHub](https://github.com/mattn/efm-langserver)

1. Instale o efm-langserver e o djLint com o Mason, via `:MasonInstall efm djlint`
1. Adicione `htmldjango` a `filetypes`.
1. Crie a configuração de formatação:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Associe a linguagem ao formatador com `htmldjango = { djlint }`.

Exemplo de configuração:

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

### coc.nvim

- [Pacote npm](https://www.npmjs.com/package/coc-htmldjango)

## IDEs da JetBrains

No PyCharm e nas outras IDEs baseadas no IntelliJ, use o plugin gratuito [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij):

1. Instale o LSP4IJ pelo Marketplace.
1. Abra a janela de ferramentas LSP Consoles e adicione um novo servidor de linguagem.
1. Na aba **Server**, defina o nome como `djLint` e o comando como `djlint --lsp`, com o caminho completo do `djlint` no ambiente virtual do projeto, caso ele não esteja no PATH.
1. Na aba **Mappings**, adicione um padrão de nome de arquivo para os seus templates, como `*.html`. Se a configuração do projeto não tiver um [perfil](/pt-br/docs/configuration/#profile), defina o ID de linguagem como `htmldjango` em um projeto Django, para que o perfil certo seja escolhido.
1. Na aba **Configuration**, você pode definir as [configurações](#configurações) em JSON, sob a chave `djlint`.

As ocorrências aparecem no editor, e o **Reformat Code** pode usar o servidor para os arquivos mapeados.

## Sublime Text

### LSP (recomendado)

O pacote [LSP](https://packagecontrol.io/packages/LSP) executa o [servidor de linguagem](#servidor-de-linguagem), que traz as ocorrências enquanto você digita e a formatação.

Execute **Preferences: LSP Server Configurations** e adicione:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

O djLint pode ser usado como um plugin de linter do SublimeText. Ele pode ser instalado pelo [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

1. `cmd + shift + p`
2. Instale o SublimeLinter
3. Instale o SublimeLinter-contrib-djlint

Certifique-se de que o djLint esteja instalado no seu Python global ou no seu `PATH`.

## Helix

O Helix pode executar o [servidor de linguagem](#servidor-de-linguagem) a partir do `languages.toml`:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Com o Eglot, que vem com o Emacs 29 e versões mais recentes:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Em seguida, execute `M-x eglot` em um template. `eglot-format-buffer` o formata.

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

`--sarif` grava um documento SARIF 2.1.0 na stdout e nada mais, para que possa ser redirecionado como acima. Cada regra ativada é listada com um link para a sua documentação, cada ocorrência traz a sua linha e coluna e, com `--check`, um arquivo que seria reformatado é relatado sob uma regra `formatting`. O Azure DevOps, o GitLab e a maioria dos editores leem o mesmo formato.

## Pre-Commit

O djLint pode ser usado como hook do [pre-commit](https://pre-commit.com), tanto como linter quanto como formatador.

O repositório oferece vários hooks pré-configurados para perfis específicos do djLint (eles apenas predefinem o argumento `--profile` e informam ao pre-commit quais extensões de arquivo procurar):

- `djlint` para lint e `djlint-reformat` para formatação
  Procura arquivos que correspondam a `*.html` sem definir `--profile`.
- `djlint-django` e `djlint-reformat-django`
  Procura arquivos que correspondam a `*.html` e define `--profile=django`.
- `djlint-jinja` e `djlint-reformat-jinja`
  Procura arquivos que correspondam a `*.j2`,`*.jinja` ou `*.jinja2` e define `--profile=jinja`.
- `djlint-nunjucks` e `djlint-reformat-nunjucks`
  Procura arquivos que correspondam a `*.njk` e define `--profile=nunjucks`.
- `djlint-handlebars` e `djlint-reformat-handlebars`
  Procura arquivos que correspondam a `*.hbs` e define `--profile=handlebars`.
- `djlint-liquid` e `djlint-reformat-liquid`
  Procura arquivos que correspondam a `*.html` e define `--profile=liquid`.
- `djlint-golang` e `djlint-reformat-golang`
  Procura arquivos que correspondam a `*.gotmpl` e define `--profile=golang`.
- `djlint-tera` e `djlint-reformat-tera`
  Procura arquivos que correspondam a `*.html` e define `--profile=tera`.
- `djlint-askama` e `djlint-reformat-askama`
  Procura arquivos que correspondam a `*.html` e define `--profile=askama`.

Observe que esses hooks predefinidos às vezes são conservadores demais nas entradas que aceitam (seus templates podem usar uma extensão diferente), por isso o pre-commit permite explicitamente sobrescrever qualquer uma dessas opções predefinidas. Consulte a [documentação do pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks) para outras configurações.

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

O djlint vem integrado nativamente entre os mais de 100 linters do [MegaLinter](https://megalinter.io)

Para instalá-lo, basta executar `npx mega-linter-runner --install` e seguir as instruções

- [Repositório no GitHub](https://github.com/oxsecurity/megalinter)
- [djlint na documentação do MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
