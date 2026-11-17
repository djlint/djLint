---
title: "통합"
description: "에디터에서 djLint를 사용하고 pre-commit으로 실행하는 방법입니다."
---

어떤 에디터를 쓰든 djLint는 에디터가 찾을 수 있는 곳, 가급적 프로젝트의 가상 환경에 설치하고, 에디터를 그 환경에서 시작하거나 에디터가 그 환경의 `djlint`를 가리키도록 하세요. 그러면 에디터가 프로젝트에 고정된 버전을 실행하므로 pre-commit 훅이나 CI와 같은 결과를 얻을 수 있습니다.

## Visual Studio Code

Visual Studio Marketplace에서 [djLint 확장](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)을 설치하세요. Cursor, Windsurf, VSCodium 등 VS Code 기반 편집기에서는 [같은 확장을 Open VSX에서](https://open-vsx.org/extension/monosans/djlint) 설치합니다. 이 확장은 환경에서 djLint를 찾고, 찾지 못하면 번들된 djLint를 사용하며, djLint가 언어 서버를 지원하면 언어 서버를 사용합니다.

설정과 어떤 djLint를 실행하는지는 [README](https://github.com/djlint/djlint-vscode#readme)에서 설명합니다.

## Zed

[djLint 확장](https://github.com/djlint/djlint-zed)은 HTML과 Django, Jinja, Twig 같은 템플릿 확장의 언어에서 [언어 서버](#언어-서버)를 실행합니다. 아직 Zed 확장 레지스트리에 없으므로 개발 확장으로 설치하세요.

1. [rustup](https://rustup.rs)으로 Rust를 설치합니다. Zed는 Rust로 확장을 빌드하고 `wasm32-wasip2` 타깃도 직접 추가합니다. Homebrew나 Nix 등 다른 방법으로 설치한 Rust라면 이 타깃을 직접 추가하세요.
1. 확장을 클론합니다:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. Zed에서 명령 팔레트를 열고(macOS는 `cmd-shift-p`, 그 밖에는 `ctrl-shift-p`) **zed: install dev extension**을 실행한 뒤 클론한 `djlint-zed` 폴더를 고릅니다.

업데이트하려면 그 폴더에서 `git pull`을 실행한 다음 **zed: rebuild dev extension**을 실행하세요.

PATH에 djLint 1.49 이상이 있거나, djLint를 설치 없이 실행하는 [uv](https://docs.astral.sh/uv/)가 있어야 합니다. 언어의 포매터로 지정하는 방법과 설정은 [README](https://github.com/djlint/djlint-zed#readme)에서 설명합니다.

## Neovim

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

`htmldjango`에 `formatCommand = "djlint --reformat --quiet --warn -"`, `formatStdin = true`로 포맷터를 지정합니다.

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
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

Package Control로 SublimeLinter와 [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint)를 설치합니다. djLint는 Sublime Text가 보는 PATH에 있어야 합니다.

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

`--sarif`는 SARIF 2.1.0 문서만 stdout에 쓰므로 위와 같이 리디렉션할 수 있습니다. 활성화된 모든 규칙이 문서 링크와 함께 나열되고, 각 검사 결과에는 줄과 열이 담기며, `--check`를 함께 쓰면 다시 포맷될 파일이 `formatting` 규칙으로 보고됩니다.

## pre-commit

djLint는 [pre-commit](https://pre-commit.com) 훅으로 린터와 포맷터 모두에 사용할 수 있습니다.

아래 표의 프로필에는 각각 표에 나열한 린트용 훅과, 같은 이름에 `reformat`이 붙은 포맷용 훅이 있습니다. 예를 들어 `djlint-django`의 포맷용 훅은 `djlint-reformat-django`입니다. 이 훅들은 `--profile`과 pre-commit이 넘겨줄 파일을 지정합니다. `angular`에는 전용 훅이 없으므로 `djlint`나 `djlint-reformat`에 `args: [--profile=angular]`를 지정하세요.

| 훅                  | 프로필     | 파일                                 |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | 없음       | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

다른 확장자를 쓰는 템플릿이라면 구성에서 `files`를 재정의하고, 훅이 `types_or`를 지정한 경우에는 그것도 재정의하세요. pre-commit은 두 조건이 모두 맞아야 파일을 넘기기 때문입니다. 자세한 내용은 [pre-commit 문서](https://pre-commit.com/#pre-commit-configyaml---hooks)를 참고하세요.

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

[MegaLinter](https://megalinter.io)에는 djLint가 포함되어 있습니다. `npx mega-linter-runner --install`을 실행해 설정하고, 옵션은 [MegaLinter의 djLint 페이지](https://megalinter.io/latest/descriptors/html_djlint/)를 참고하세요.
