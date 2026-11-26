---
title: "Entegrasyonlar"
description: "djLint'i düzenleyicinizde kullanın ve pre-commit ile çalıştırın."
---

Hangi düzenleyiciyi kullanırsanız kullanın, djLint'i düzenleyicinin bulabileceği bir yere, tercihen projenin sanal ortamına kurun ve düzenleyiciyi oradan başlatın ya da düzenleyiciyi o ortamdaki `djlint` komutuna yönlendirin. Böylece düzenleyici, projenizin sabitlediği sürümü çalıştırır ve pre-commit kancanızla ya da CI ile aynı sonuçları verir.

Proje djLint'i [npm](/tr/docs/getting-started/#kurulum) ile kuruyorsa komutu projede `node_modules/.bin/djlint`, Windows'ta ise `node_modules/.bin/djlint.cmd` olur. Aşağıdaki düzenleyicilerde `djlint` çalıştırılan yerlerde bu yolu verin. Yol görelidir, bu yüzden düzenleyiciyi proje kökünde başlatın. VS Code ve Zed uzantıları onu kendileri bulur.

## Visual Studio Code

[djLint uzantısını](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) Visual Studio Marketplace'ten kurun. Cursor, Windsurf, VSCodium ve VS Code tabanlı diğer editörler [aynı uzantıyı Open VSX'ten](https://open-vsx.org/extension/monosans/djlint) kurar. Uzantı djLint'i ortamınızda bulur, bulamazsa kendisiyle birlikte gelen sürüme geri döner ve djLint sürümünüzde dil sunucusu varsa onu kullanır.

Uzantının [README](https://github.com/djlint/djlint-vscode#readme) dosyası, ayarlarını ve hangi djLint'i çalıştırdığını anlatır.

## Zed

[djLint uzantısı](https://github.com/djlint/djlint-zed), [dil sunucusunu](#dil-sunucusu) HTML'de ve Django, Jinja, Twig gibi şablon uzantılarının dillerinde çalıştırır. Henüz Zed'in uzantı kayıt defterinde olmadığından onu geliştirme uzantısı olarak kurun:

1. Rust'ı [rustup](https://rustup.rs) ile kurun: Zed uzantıyı onunla derler ve `wasm32-wasip2` hedefini kendisi ekler. Rust'ı Homebrew ya da Nix gibi başka bir yoldan kurduysanız bu hedefi kendiniz ekleyin.
1. Uzantıyı klonlayın:

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. Zed'de komut paletini açın (macOS'ta `cmd-shift-p`, diğerlerinde `ctrl-shift-p`), **zed: install dev extension** komutunu çalıştırın ve klonlanan `djlint-zed` klasörünü seçin.

Güncellemek için o klasörde `git pull`, ardından **zed: rebuild dev extension** çalıştırın.

PATH'te ya da projede npm ile kurulu djLint 1.49 veya daha yenisi ya da djLint'i kurulum olmadan çalıştıran [uv](https://docs.astral.sh/uv/) gerekir. Uzantının [README](https://github.com/djlint/djlint-zed#readme) dosyası, onu bir dilin biçimlendiricisi olarak nasıl ayarlayacağınızı gösterir ve ayarlarını anlatır.

## Neovim

Neovim bazı şablon uzantılarına dosya türü atamaz. Aşağıdaki seçeneklerden hangisini kullanırsanız kullanın, önce bunları kaydedin:

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### Yerleşik LSP istemcisi (önerilen)

Neovim 0.11 ve üzeri, herhangi bir eklenti olmadan djLint'in [dil sunucusuyla](#dil-sunucusu) doğrudan konuşabilir. Bu sayede bulgular, altı çizili aralıklarla birlikte siz yazarken gelir ve biçimlendirme için `vim.lsp.buf.format()` kullanılabilir:

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

Kaydederken biçimlendirmek için aynı yapılandırmaya şunu ekleyin:

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

Bkz. [Ayarlar](#ayarlar).

### conform.nvim ve nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) biçimlendirir, [nvim-lint](https://github.com/mfussenegger/nvim-lint) ise lint denetimi yapar; ikisi de djLint'i bir komut olarak çalıştırır. Bulguların altı çizili bir aralığı olmaz ve yalnızca nvim-lint'ten denetim yapmasını istediğinizde gelirler. Profil, komut satırında olduğu gibi projenin [yapılandırmasından](/tr/docs/configuration/#profile) gelir. Bu örnek djLint 1.49 veya daha yenisini gerektirir.

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

- [GitHub deposu](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Biçimlendirme](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [npm paketi](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains IDE'leri

PyCharm'da ve IntelliJ tabanlı diğer IDE'lerde ücretsiz [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) eklentisini kullanın:

1. LSP4IJ'yi Marketplace'ten kurun.
1. LSP Consoles araç penceresini açın ve yeni bir dil sunucusu ekleyin.
1. **Server** sekmesinde adı `djLint`, komutu `djlint --lsp` olarak ayarlayın; PATH üzerinde değilse projenin sanal ortamındaki `djlint` komutunun tam yolunu kullanın.
1. **Mappings** sekmesinde şablonlarınızın dosya adı kalıplarını ekleyin. Projenin yapılandırmasında bir [profil](/tr/docs/configuration/#profile) yoksa profili her kalıbın dil kimliği seçer:

   | Kalıplar                              | Dil kimliği                    |
   | ------------------------------------- | ------------------------------ |
   | `*.html`, `*.htm`                     | `html`, Django'da `htmldjango` |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                        |
   | `*.njk`, `*.twig`                     | `nunjucks`                     |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                   |
   | `*.liquid`                            | `liquid`                       |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                       |
   | `*.tera`                              | `tera`                         |
   | `*.mako`                              | `mako`                         |

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

SublimeLinter'ı ve [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) paketini Package Control ile kurun. djLint, Sublime Text'in gördüğü PATH üzerinde olmalıdır.

## Helix

Helix, [dil sunucusunu](#dil-sunucusu) `languages.toml` dosyasından çalıştırabilir. Bir `language-servers` listesi, Helix'in o dil için kullandığı listenin yerini alır; bu yüzden Helix'in kendi sunucularını `djlint` ardından koruyun:

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

Helix hiçbir dosyayı kendiliğinden `htmldjango` olarak açmaz. Bir Django projesinde, projenin `.helix/languages.toml` dosyasında bu girdiye `file-types = ["html"]` ekleyin.

## Emacs

Emacs 29 ve üzeriyle birlikte gelen Eglot ile:

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

Ardından bir şablonda `M-x eglot` çalıştırın. `eglot-format-buffer` şablonu biçimlendirir. `html-mode`, `mhtml-mode` ve `web-mode` bir şablon dili belirtmez; bu modlarda profil projenin [yapılandırmasından](/tr/docs/configuration/#profile) gelir.

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

`--sarif`, stdout'a bir SARIF 2.1.0 belgesi yazar ve başka hiçbir şey yazmaz; bu yüzden yukarıdaki gibi yönlendirilebilir. Etkin her kural, belgelerine giden bir bağlantıyla listelenir, her bulgu satırını ve sütununu taşır ve `--check` ile yeniden biçimlendirilecek bir dosya `formatting` kuralı altında bildirilir.

## pre-commit

djLint, hem linter hem de biçimlendirici olarak bir [pre-commit](https://pre-commit.com) kancası şeklinde kullanılabilir.

Bu profillerin her birinin burada listelenen, lint denetimi yapan bir kancası ve biçimlendiren, aynı adı `reformat` ile taşıyan bir kancası vardır: `djlint-django` için `djlint-reformat-django`. Kancalar `--profile` değerini ve pre-commit'in ileteceği dosyaları ayarlar. `angular` profilinin kendine ait kancası yoktur: `djlint` ya da `djlint-reformat` kancasına `args: [--profile=angular]` verin.

| Kanca               | Profil     | Dosyalar                             |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | yok        | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Başka uzantılı şablonlar için yapılandırmanızda `files` değerini, kanca ayarlıyorsa `types_or` değerini de geçersiz kılın, çünkü pre-commit ikisinin de eşleşmesini ister. Ayrıntılar için [pre-commit belgelerine](https://pre-commit.com/#pre-commit-configyaml---hooks) bakın.

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

[MegaLinter](https://megalinter.io) djLint'i içerir. Kurmak için `npx mega-linter-runner --install` komutunu çalıştırın, seçenekler için [djLint sayfasına](https://megalinter.io/latest/descriptors/html_djlint/) bakın.
