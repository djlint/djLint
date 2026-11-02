---
title: "통합"
description: "자주 쓰는 에디터와 djLint를 통합하세요. Pre-Commit으로 템플릿을 자동 포맷하고, SublimeText에서 린트하세요."
sidebar:
  label: "통합"
---

djLint를 위한 에디터 통합이 여러 가지 있습니다.

어떤 에디터를 쓰든 djLint는 에디터가 찾을 수 있는 곳, 가급적 프로젝트의 가상 환경에 설치하고, 에디터를 그 환경에서 시작하거나 에디터가 그 환경의 `djlint`를 가리키도록 하세요. 그러면 에디터가 프로젝트에 고정된 버전을 실행하므로 pre-commit 훅이나 CI와 같은 결과를 얻을 수 있습니다.

## Visual Studio Code

[djLint 확장](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)을 설치하세요. VSCodium에서는 [Open VSX에 있는 확장](https://open-vsx.org/extension/monosans/djlint)을 설치합니다. 이 확장은 환경에서 djLint를 찾고, 찾지 못하면 번들된 djLint를 사용하며, djLint가 언어 서버를 지원하면 언어 서버를 사용합니다.

코드는 [GitHub](https://github.com/djlint/djlint-vscode)에 있습니다.

## Neovim

Neovim에서 djLint를 린터와 포맷터로 사용할 수 있습니다.

### 내장 LSP 클라이언트(권장)

Neovim 0.11 이상은 플러그인 없이 djLint의 [언어 서버](#언어-서버)와 직접 통신할 수 있습니다. 입력하는 동안 범위에 밑줄이 그어진 검사 결과를 받을 수 있고, `vim.lsp.buf.format()`으로 포맷할 수 있습니다.

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

저장할 때 포맷하려면 같은 구성에 다음을 추가합니다.

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

[설정](#설정)을 참고하세요.

### conform.nvim과 nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim)은 포맷을, [nvim-lint](https://github.com/mfussenegger/nvim-lint)는 린트를 맡으며, 둘 다 djLint를 명령으로 실행합니다. 검사 결과에 밑줄이 그어진 범위가 없고, nvim-lint에 린트를 요청할 때만 결과가 나타납니다.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [GitHub 저장소](https://github.com/nvimtools/none-ls.nvim)
- [린트](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [포맷](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [GitHub 저장소](https://github.com/mattn/efm-langserver)

1. Mason에서 `:MasonInstall efm djlint`로 efm-langserver와 djLint를 설치합니다.
1. `filetypes`에 `htmldjango`를 추가합니다.
1. 포맷 구성을 만듭니다.

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. `htmldjango = { djlint }`로 언어와 포맷터를 연결합니다.

구성 예시:

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

- [npm 패키지](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains IDE

PyCharm을 비롯한 IntelliJ 기반 IDE에서는 무료 플러그인인 [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij)를 사용하세요.

1. Marketplace에서 LSP4IJ를 설치합니다.
1. LSP Consoles 도구 창을 열고 새 언어 서버를 추가합니다.
1. **Server** 탭에서 이름을 `djLint`로, 명령을 `djlint --lsp`로 설정합니다. PATH에 없다면 프로젝트 가상 환경에 있는 `djlint`의 전체 경로를 사용합니다.
1. **Mappings** 탭에서 `*.html`과 같은 템플릿 파일 이름 패턴을 추가합니다. 프로젝트 구성에 [프로필](/ko/docs/configuration/#profile)이 없다면, 올바른 프로필이 선택되도록 Django 프로젝트에서는 언어 ID를 `htmldjango`로 설정합니다.
1. **Configuration** 탭에서 `djlint` 키 아래에 JSON으로 [설정](#설정)을 지정할 수 있습니다.

검사 결과가 에디터에 표시되고, 매핑된 파일에서는 **Reformat Code**가 이 서버를 사용할 수 있습니다.

## Sublime Text

### LSP(권장)

[LSP](https://packagecontrol.io/packages/LSP) 패키지는 [언어 서버](#언어-서버)를 실행해 입력하는 동안 검사 결과를 보여 주고 포맷 기능을 제공합니다.

**Preferences: LSP Server Configurations**를 실행하고 다음을 추가합니다.

```json
{
  "djlint": {
    "enabled": true,
    "command": ["djlint", "--lsp"],
    "selector": "text.html"
  }
}
```

### SublimeLinter

djLint를 SublimeText Linter 플러그인으로 사용할 수 있습니다. [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint)에서 설치할 수 있습니다.

1. `cmd + shift + p`
2. SublimeLinter 설치
3. SublimeLinter-contrib-djlint 설치

djLint가 전역 Python이나 `PATH`에 설치되어 있는지 확인하세요.

## Helix

Helix는 `languages.toml`에서 [언어 서버](#언어-서버)를 실행할 수 있습니다.

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Emacs 29 이상에 포함된 Eglot에서는 다음과 같이 합니다.

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

그런 다음 템플릿에서 `M-x eglot`을 실행합니다. `eglot-format-buffer`로 템플릿을 포맷할 수 있습니다.

## 언어 서버

`djlint --lsp`는 djLint를 stdio로 통신하는 언어 서버로 실행합니다. 서버가 계속 실행되므로, 에디터는 입력하는 동안 검사 결과를 받고 매번 프로세스를 시작하지 않고도 문서를 포맷할 수 있습니다.

서버는 검사 결과를 보고하고 문서 전체를 포맷합니다. 추가 패키지는 필요하지 않습니다. LSP를 지원하는 다른 에디터라면 어디서든 같은 명령으로 실행할 수 있습니다.

### 설정

서버는 명령줄과 마찬가지로 각 파일의 폴더에서 위쪽으로 프로젝트의 [구성](/ko/docs/configuration/)을 읽습니다. 에디터의 설정이 구성보다 우선하지만, 명령줄에서처럼 옵션을 켜거나 값을 지정하는 것만 가능합니다. `false`로는 프로젝트가 켠 옵션을 끌 수 없습니다. 설정 이름은 [명령줄 옵션](/ko/docs/configuration/)의 이름을 밑줄 표기나 camelCase로 쓰며, 쉼표로 구분하는 값에는 리스트를 쓸 수 있습니다.

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

서버는 `workspace/configuration`으로 `djlint` 섹션을 요청합니다. 이 요청에 응답할 수 없는 에디터는 같은 키를 `initializationOptions`로 보낼 수 있습니다.

다음 두 설정에는 대응하는 명령줄 옵션이 없습니다.

- `use_editor_indentation`: `indent` 대신 에디터의 탭 크기로 포맷합니다.
- `python_rules`: `false`로 설정하면 `python_module`이 있는 사용자 정의 규칙을 건너뛰므로, 프로젝트의 코드가 실행되지 않습니다.

djLint는 다음 중 `profile`이 지정된 첫 번째 항목에서 그 값을 가져옵니다.

1. 에디터의 설정
1. 프로젝트의 구성
1. 문서의 언어. 예를 들어 `htmldjango`는 `django` 프로필로 실행합니다.

셋 다 없으면 명령줄에서처럼 프로필 없이 실행합니다. 프로젝트 구성에 `profile`을 지정하는 것이 가장 간단합니다. 언어 ID를 설정할 필요 없이 모든 에디터에서 동작하기 때문입니다.

### 동작 방식

- 검사 결과는 입력을 잠시 멈춘 뒤에 나타납니다. 풀 진단(pull diagnostics)을 지원하는 에디터는 결과를 요청하고, 그 밖의 에디터에는 결과를 푸시합니다.
- `exclude`, `extend_exclude`, `use_gitignore`는 열린 문서에도 적용됩니다. 제외된 문서에는 검사 결과가 없고 포맷도 하지 않습니다.
- 에디터가 파일을 감시할 수 있다면 `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig`, `.gitignore`가 바뀔 때, 그렇지 않다면 문서를 열거나 저장할 때 구성을 다시 불러옵니다. `configuration`이나 `rules`로 지정한 파일은 문서를 열거나 저장할 때 다시 읽습니다. 사용자 정의 규칙의 `python_module` 코드를 바꾸었다면 서버를 다시 시작해야 합니다.
- 서버는 한 번에 한 가지 작업만 하므로, 느린 규칙이 있으면 그 뒤의 작업이 지연됩니다.

## GitHub Actions

GitHub Actions 워크플로에서 djLint는 각 검사 결과를 주석(annotation)으로 보고하므로, 풀 리퀘스트의 diff에 인라인으로 표시됩니다. 따로 구성할 필요는 없습니다. djLint가 워크플로를 감지해 자동으로 출력 방식을 바꿉니다.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

일반 콘솔 출력을 받으려면 `--no-github-output`을, Actions 밖에서도 주석을 강제로 출력하려면 `--github-output`을 사용하세요.

주석은 하나의 풀 리퀘스트에만 속합니다. 실행 기록과 함께 저장소의 Security 탭에 검사 결과를 남기려면 결과를 SARIF로 작성해 파일을 업로드하세요.

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

업로드 단계에는 잡이나 워크플로에 `security-events: write` 권한이 필요합니다.

`--sarif`는 SARIF 2.1.0 문서만 stdout에 쓰므로 위와 같이 리디렉션할 수 있습니다. 활성화된 모든 규칙이 문서 링크와 함께 나열되고, 각 검사 결과에는 줄과 열이 담기며, `--check`를 함께 쓰면 다시 포맷될 파일이 `formatting` 규칙으로 보고됩니다. Azure DevOps, GitLab과 대부분의 에디터가 같은 형식을 읽습니다.

## Pre-Commit

djLint는 [pre-commit](https://pre-commit.com) 훅으로 린터와 포맷터 모두에 사용할 수 있습니다.

저장소에는 특정 djLint 프로필에 맞게 미리 구성된 훅이 여러 개 있습니다. 이 훅들은 `--profile` 인수를 미리 지정하고, pre-commit에 어떤 파일 확장자를 찾을지 알려 줄 뿐입니다.

- 린트용 `djlint`와 포맷용 `djlint-reformat`
  `--profile`을 지정하지 않고 `*.html`과 일치하는 파일을 찾습니다.
- `djlint-django`와 `djlint-reformat-django`
  `*.html`과 일치하는 파일을 찾고 `--profile=django`를 지정합니다.
- `djlint-jinja`와 `djlint-reformat-jinja`
  `*.j2`,`*.jinja`, `*.jinja2` 중 하나와 일치하는 파일을 찾고 `--profile=jinja`를 지정합니다.
- `djlint-nunjucks`와 `djlint-reformat-nunjucks`
  `*.njk`와 일치하는 파일을 찾고 `--profile=nunjucks`를 지정합니다.
- `djlint-handlebars`와 `djlint-reformat-handlebars`
  `*.hbs`와 일치하는 파일을 찾고 `--profile=handlebars`를 지정합니다.
- `djlint-liquid`와 `djlint-reformat-liquid`
  `*.html`과 일치하는 파일을 찾고 `--profile=liquid`를 지정합니다.
- `djlint-golang`과 `djlint-reformat-golang`
  `*.gotmpl`과 일치하는 파일을 찾고 `--profile=golang`을 지정합니다.
- `djlint-tera`와 `djlint-reformat-tera`
  `*.html`과 일치하는 파일을 찾고 `--profile=tera`를 지정합니다.
- `djlint-askama`와 `djlint-reformat-askama`
  `*.html`과 일치하는 파일을 찾고 `--profile=askama`를 지정합니다.

이렇게 미리 정의된 훅은 받아들이는 입력이 지나치게 보수적일 때가 있으므로(템플릿에 다른 확장자를 쓰고 있을 수도 있습니다), pre-commit에서는 미리 정의된 옵션을 무엇이든 재정의할 수 있습니다. 추가 구성은 [pre-commit 문서](https://pre-commit.com/#pre-commit-configyaml---hooks)를 참고하세요.

### 기본 Django 예시

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### .hbs 대신 .html 확장자를 쓰는 Handlebars

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

`files`나 `exclude` 파라미터로 훅마다 대상 디렉터리를 제한하면, 한 저장소에서 여러 템플릿 언어를 지원할 수 있습니다.

## MegaLinter

djlint는 [MegaLinter](https://megalinter.io)의 100개가 넘는 린터에 기본으로 포함되어 있습니다.

설치하려면 `npx mega-linter-runner --install`을 실행하고 안내를 따르기만 하면 됩니다.

- [GitHub 저장소](https://github.com/oxsecurity/megalinter)
- [MegaLinter 문서의 djlint 항목](https://megalinter.io/latest/descriptors/html_djlint/)
