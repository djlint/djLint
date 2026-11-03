---
description: djLint'i düzenleyicinizde kullanın ve pre-commit ile çalıştırın.
title: Entegrasyonlar
keywords: şablon linter'ı, şablon biçimlendiricisi, djLint, HTML, şablonlar, biçimlendirici, linter, entegrasyonlar, dil sunucusu, lsp, neovim, helix
---

# Entegrasyonlar

djLint için geliştirilmiş birkaç düzenleyici entegrasyonu vardır.

Hangi düzenleyiciyi kullanırsanız kullanın, djLint'i düzenleyicinin bulabileceği bir yere, tercihen projenin sanal ortamına kurun ve düzenleyiciyi oradan başlatın ya da düzenleyiciyi o ortamdaki `djlint` komutuna yönlendirin. Böylece düzenleyici, projenizin sabitlediği sürümü çalıştırır ve pre-commit kancanızla ya da CI ile aynı sonuçları verir.

## Visual Studio Code

[djLint uzantısını](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) ya da VSCodium için [Open VSX'teki uzantıyı](https://open-vsx.org/extension/monosans/djlint) kurun. Uzantı djLint'i ortamınızda bulur, bulamazsa kendisiyle birlikte gelen sürüme geri döner ve djLint sürümünüzde dil sunucusu varsa onu kullanır.

Kodu [GitHub](https://github.com/djlint/djlint-vscode) üzerindedir.

## Neovim

djLint, Neovim'de linter ve biçimlendirici olarak kullanılabilir.

### Yerleşik LSP istemcisi (önerilen)

Neovim 0.11 ve üzeri, herhangi bir eklenti olmadan djLint'in [dil sunucusuyla](#dil-sunucusu) doğrudan konuşabilir. Bu sayede bulgular, altı çizili aralıklarla birlikte siz yazarken gelir ve biçimlendirme için `vim.lsp.buf.format()` kullanılabilir:

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Kaydederken biçimlendirmek için aynı yapılandırmaya şunu ekleyin:

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

Bkz. [Ayarlar](#ayarlar).

### conform.nvim ve nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) biçimlendirir, [nvim-lint](https://github.com/mfussenegger/nvim-lint) ise lint denetimi yapar; ikisi de djLint'i bir komut olarak çalıştırır. Bulguların altı çizili bir aralığı olmaz ve yalnızca nvim-lint'ten denetim yapmasını istediğinizde gelirler.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

::: content

- [GitHub deposu](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Biçimlendirme](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
:::

### efm-langserver

::: content

- [GitHub deposu](https://github.com/mattn/efm-langserver)

1. efm-langserver ve djLint'i Mason ile `:MasonInstall efm djlint` komutuyla kurun
1. `filetypes` listesine `htmldjango` ekleyin.
1. Biçimlendirme yapılandırmasını oluşturun:

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Dili biçimlendiriciye `htmldjango = { djlint }` ile bağlayın.

Örnek yapılandırma:

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

- [npm paketi](https://www.npmjs.com/package/coc-htmldjango)
:::

## JetBrains IDE'leri

PyCharm'da ve IntelliJ tabanlı diğer IDE'lerde ücretsiz [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) eklentisini kullanın:

1. LSP4IJ'yi Marketplace'ten kurun.
1. LSP Consoles araç penceresini açın ve yeni bir dil sunucusu ekleyin.
1. **Server** sekmesinde adı `djLint`, komutu `djlint --lsp` olarak ayarlayın; PATH üzerinde değilse projenin sanal ortamındaki `djlint` komutunun tam yolunu kullanın.
1. **Mappings** sekmesinde şablonlarınız için `*.html` gibi bir dosya adı kalıbı ekleyin. Projenin yapılandırmasında bir [profil](/tr/docs/configuration/#profile) yoksa doğru profilin seçilmesi için Django projelerinde dil kimliğini `htmldjango` olarak ayarlayın.
1. **Configuration** sekmesinde [ayarları](#ayarlar) JSON olarak, bir `djlint` anahtarı altında belirleyebilirsiniz.

Bulgular düzenleyicide görünür ve **Reformat Code**, eşlenen dosyalar için sunucuyu kullanabilir.

## Sublime Text

### LSP (önerilen)

[LSP](https://packagecontrol.io/packages/LSP) paketi [dil sunucusunu](#dil-sunucusu) çalıştırır; bu da siz yazarken bulgular ve biçimlendirme sağlar.

**Preferences: LSP Server Configurations** komutunu çalıştırın ve şunu ekleyin:

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

djLint, bir SublimeText Linter eklentisi olarak kullanılabilir. [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) üzerinden kurulabilir.

::: content

1. `cmd + shift + p`
2. SublimeLinter'ı kurun
3. SublimeLinter-contrib-djlint'i kurun
:::

djLint'in genel Python kurulumunuzda ya da `PATH` üzerinde kurulu olduğundan emin olun.

## Helix

Helix, [dil sunucusunu](#dil-sunucusu) `languages.toml` dosyasından çalıştırabilir:

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Emacs 29 ve üzeriyle birlikte gelen Eglot ile:

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Ardından bir şablonda `M-x eglot` çalıştırın. `eglot-format-buffer` şablonu biçimlendirir.

## Dil sunucusu

`djlint --lsp`, djLint'i stdio üzerinden bir dil sunucusu olarak çalıştırır. Sunucu çalışmaya devam eder; böylece düzenleyici, siz yazarken bulguları alır ve her seferinde yeni bir süreç başlatmadan belgeyi biçimlendirir.

Bulguları bildirir ve belgelerin tamamını biçimlendirir. Ek paket gerektirmez. LSP konuşan başka herhangi bir düzenleyici de aynı komutla çalıştırabilir.

### Ayarlar

Sunucu, projenin [yapılandırmasını](/tr/docs/configuration/) komut satırının yaptığı gibi her dosyanın klasöründen yukarı doğru okur. Düzenleyiciden gelen ayarlar bunun önüne geçer, ancak komut satırında olduğu gibi yalnızca bir seçeneği açabilir ya da bir değer belirleyebilir: `false`, projenin açtığı bir şeyi kapatmaz. Ayarlar [komut satırı seçeneklerinin](/tr/docs/configuration/) adlarını, alt çizgili ya da camelCase biçiminde alır; virgülle ayrılmış değerler için listeler kullanılabilir:

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Sunucu `djlint` bölümünü `workspace/configuration` ile ister. Buna yanıt veremeyen bir düzenleyici aynı anahtarları `initializationOptions` içinde gönderebilir.

İki ayarın komut satırı seçeneği yoktur:

- `use_editor_indentation`: `indent` yerine düzenleyicinin sekme boyutuyla biçimlendirir.
- `python_rules`: `python_module` içeren özel kuralları atlamak için `false` yapın; bu, projenin kodunun çalışmasını önler.

djLint `profile` değerini, aşağıdakilerden bir profil içeren ilkinden alır:

1. Düzenleyicinin ayarları.
1. Projenin yapılandırması.
1. Belgenin dili: örneğin `htmldjango`, `django` profilini çalıştırır.

Hiçbiri yoksa komut satırında olduğu gibi profilsiz çalışır. Projenin yapılandırmasındaki bir `profile` en basit seçimdir: her düzenleyicide çalışır ve ayarlanacak bir dil kimliği gerektirmez.

### Neler yapar

- Bulgular, yazmaya kısa bir ara verdikten sonra gelir. Pull diagnostics destekleyen bir düzenleyici bulguları kendisi ister, diğerlerine ise bulgular gönderilir.
- `exclude`, `extend_exclude` ve `use_gitignore` açık belgelere uygulanır. Hariç tutulan bir belgenin bulgusu olmaz ve biçimlendirilmez.
- `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` ya da `.gitignore` değiştiğinde, düzenleyici dosyaları izleyebiliyorsa yapılandırmayı yeniden yükler; izleyemiyorsa bir belge açıldığında ya da kaydedildiğinde yükler. `configuration` ya da `rules` ile belirtilen dosyalar, bir belge açıldığında ya da kaydedildiğinde yeniden okunur. Özel bir kuralın `python_module` kodundaki bir değişiklik yeniden başlatma gerektirir.
- Sunucu her seferinde tek bir iş yaptığından, yavaş bir kural kendisinden sonra gelenleri bekletir.

## GitHub Actions

Bir GitHub Actions iş akışında djLint her bulguyu bir ek açıklama (annotation) olarak bildirir; böylece bulgu, pull request'in diff'inde satır içinde görünür. Yapılandırma gerekmez: djLint iş akışını algılar ve çıktıyı otomatik olarak değiştirir.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Bunun yerine düz konsol çıktısını almak için `--no-github-output`, Actions dışında ek açıklamaları zorlamak için `--github-output` kullanın.

Ek açıklamalar tek bir pull request'e aittir. Bulguları, çalıştırmalar arası geçmişiyle birlikte deponun Security sekmesinde tutmak için onları SARIF olarak yazın ve dosyayı yükleyin:

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

Yükleme adımı, job'da ya da iş akışında `security-events: write` iznine ihtiyaç duyar.

`--sarif`, stdout'a bir SARIF 2.1.0 belgesi yazar ve başka hiçbir şey yazmaz; bu yüzden yukarıdaki gibi yönlendirilebilir. Etkin her kural, belgelerine giden bir bağlantıyla listelenir, her bulgu satırını ve sütununu taşır ve `--check` ile yeniden biçimlendirilecek bir dosya `formatting` kuralı altında bildirilir. Azure DevOps, GitLab ve çoğu düzenleyici aynı biçimi okur.

## Pre-Commit

djLint, hem linter hem de biçimlendirici olarak bir [pre-commit](https://pre-commit.com) kancası şeklinde kullanılabilir.

Depo, belirli djLint profilleri için önceden yapılandırılmış birden çok kanca sunar (bunlar yalnızca `--profile` argümanını önceden ayarlar ve pre-commit'e hangi dosya uzantılarına bakacağını söyler):

::: content

- Lint denetimi için `djlint` ve biçimlendirme için `djlint-reformat`
  Bu kancalar `--profile` ayarlamadan `*.html` ile eşleşen dosyaları arar.
- `djlint-django` ve `djlint-reformat-django`
  Bu kancalar `*.html` ile eşleşen dosyaları arar ve `--profile=django` ayarlar.
- `djlint-jinja` ve `djlint-reformat-jinja`
  Bu kancalar `*.j2`,`*.jinja` ya da `*.jinja2` ile eşleşen dosyaları arar ve `--profile=jinja` ayarlar.
- `djlint-nunjucks` ve `djlint-reformat-nunjucks`
  Bu kancalar `*.njk` ile eşleşen dosyaları arar ve `--profile=nunjucks` ayarlar.
- `djlint-handlebars` ve `djlint-reformat-handlebars`
  Bu kancalar `*.hbs` ile eşleşen dosyaları arar ve `--profile=handlebars` ayarlar.
- `djlint-liquid` ve `djlint-reformat-liquid`
  Bu kancalar `*.html` ile eşleşen dosyaları arar ve `--profile=liquid` ayarlar.
- `djlint-golang` ve `djlint-reformat-golang`
  Bu kancalar `*.gotmpl` ile eşleşen dosyaları arar ve `--profile=golang` ayarlar.
- `djlint-tera` ve `djlint-reformat-tera`
  Bu kancalar `*.html` ile eşleşen dosyaları arar ve `--profile=tera` ayarlar.
- `djlint-askama` ve `djlint-reformat-askama`
  Bu kancalar `*.html` ile eşleşen dosyaları arar ve `--profile=askama` ayarlar.
- `djlint-mako` ve `djlint-reformat-mako`
  Bu kancalar `*.html` ile eşleşen dosyaları arar ve `--profile=mako` ayarlar.
:::

Önceden tanımlanmış bu kancaların kabul ettikleri girdiler konusunda bazen fazla tutucu olduğunu unutmayın (şablonlarınız farklı bir uzantı kullanıyor olabilir); bu yüzden pre-commit, önceden tanımlanmış bu seçeneklerin herhangi birini geçersiz kılmanıza açıkça izin verir. Ek yapılandırma için [pre-commit belgelerine](https://pre-commit.com/#pre-commit-configyaml---hooks) bakın.

### Varsayılan Django örneği

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### .hbs yerine .html uzantılı Handlebars

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

Her kancayı kendi dizinine sınırlamak için `files` ya da `exclude` parametrelerini kullanabilirsiniz; böylece aynı depoda birden çok şablon dilini destekleyebilirsiniz.

## MegaLinter

djlint, [MegaLinter](https://megalinter.io) içindeki 100'den fazla linter arasında yerleşik olarak bulunur

Kurmak için `npx mega-linter-runner --install` komutunu çalıştırıp talimatları izlemeniz yeterli

::: content

- [GitHub deposu](https://github.com/oxsecurity/megalinter)
- [MegaLinter belgelerinde djlint](https://megalinter.io/latest/descriptors/html_djlint/)
:::
