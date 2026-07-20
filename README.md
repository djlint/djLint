<h1 align="center">
  <br>
  <a href="https://www.djlint.com"><img src="https://raw.githubusercontent.com/djlint/djLint/master/docs/src/static/img/icon.png" alt="djLint Logo" width="270"></a>
  <br>
</h1>
<h4 align="center">The missing formatter and linter for HTML templates.</h4>

<p align="center">
    <a href="https://twitter.com/intent/tweet?text=djLint%20%7C%20The%20missing%20formatter%20and%20linter%20for%20HTML%20templates.&url=https://djlint.com/&hashtags=djlint,html-templates,django,jinja,developers"><img alt="tweet" src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social" /></a>
    <a href="https://discord.gg/taghAqebzU">
     <img src="https://badgen.net/discord/online-members/taghAqebzU?icon=discord&label" alt="Discord Chat">
   </a>
    </p>
    <p align="center">
   <a href="https://pepy.tech/project/djlint">
     <img src="https://pepy.tech/badge/djlint" alt="Downloads">
   </a>
   <a href="https://www.npmjs.com/package/djlint">
       <img alt="npm" src="https://img.shields.io/npm/dt/djlint?label=npm%20downloads">
   </a>
   <a href="https://pypi.org/project/djlint/">
     <img src="https://img.shields.io/pypi/v/djlint" alt="Pypi Download">
   </a>
</p>

<h4 align="center"><a href="https://www.djlint.com">How to use</a> • <a href="https://www.djlint.com/ru/">Как пользоваться</a> • <a href="https://www.djlint.com/fr/">Utilisation</a> • <a href="https://www.djlint.com/zh/">如何使用</a></h4>
<h4 align="center">What lang are you using?</h4>

<p align="center">
   <a href="https://djlint.com/docs/languages/django/">Django</a> • <a href="https://djlint.com/docs/languages/jinja/">Jinja</a> • <a href="https://djlint.com/docs/languages/askama/">Askama</a> • <a href="https://djlint.com/docs/languages/tera/">Tera</a> • <a href="https://djlint.com/docs/languages/liquid/">Liquid</a> • <a href="https://djlint.com/docs/languages/nunjucks/">Nunjucks</a> • <a href="https://djlint.com/docs/languages/twig/">Twig</a> • <a href="https://djlint.com/docs/languages/handlebars/">Handlebars</a> • <a href="https://djlint.com/docs/languages/mustache/">Mustache</a> • <a href="https://djlint.com/docs/languages/golang/">GoLang</a> • <a href="https://djlint.com/docs/languages/angular/">Angular</a>
</p>

<p align="center">
  <img src="https://github.com/djlint/djLint/blob/aa9097660d4a2e840450de5456f656c42bc7dd34/docs/src/static/img/demo-min.gif" alt="demo" width="600">
</p>

## 🤔 For What?

Once upon a time all the other programming languages had a formatter and linter. Css, javascript, python, the c suite, typescript, ruby, php, go, swift, and you know the others. The cool kids on the block.

HTML templates were left out there on their own, in the cold, unformatted and unlinted :( The dirty corner in your repository. Something had to change.

**djLint is a community build project to and add consistency to html templates.**

## ✨ How?

Grab it from PyPI with `pip`

```bash
pip install djlint
```

Or as a standalone tool with [uv](https://docs.astral.sh/uv/)

```bash
uv tool install djlint
```

Or with [pipx](https://pipx.pypa.io/)

```bash
pipx install djlint
```

Or with the community-maintained [Homebrew formula](https://formulae.brew.sh/formula/djlint) on macOS or Linux

```bash
brew install djlint
```

_Or with npm - **warning**: the npm package is only a wrapper, its install script runs `pip install --upgrade djlint` on whatever `python3` is on your system path. npm will not manage or uninstall the actual package - prefer pip directly when possible._

```bash
npm i djlint
```

Lint your project

```bash
djlint . --extension=html.j2 --lint
```

Check your format

```bash
djlint . --extension=html.j2 --check
```

Fix my format!

```bash
djlint . --extension=html.j2 --reformat
```

Or use `pre-commit` to reformat, then lint!

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v1.41.0 # use latest version instead
    hooks:
      - id: djlint-reformat
      - id: djlint
```

## 💙 Like it?

Add a badge to your projects `readme.md`:

```md
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://www.djlint.com)
```

Add a badge to your `readme.rst`:

```rst
.. image:: https://img.shields.io/badge/html%20style-djlint-blue.svg
   :target: https://www.djlint.com
```

Looks like this:

[![djLint](https://img.shields.io/badge/html%20style-djLint-blue.svg)](https://github.com/djlint/djlint)

## 🛠️ Can I help?

Yes!

_Would you like to add a rule to the linter?_ Take a look at the [linter docs](https://djlint.com/docs/linter/) and [source code](https://github.com/djlint/djLint/blob/master/djlint/rules.yaml)

_Are you a regex pro?_ Benchmark and submit a pr with improved regex for the [linter rules](https://github.com/djlint/djLint/blob/master/djlint/rules.yaml)

## 🏃 Other Tools Of Note

- [djade](https://github.com/adamchainz/djade) A fast Django template formatter that formats template syntax whilst leaving HTML as-is, and applies fixes for older Django versions.
- [djangofmt](https://github.com/UnknownPlatypus/djangofmt) A fast, HTML-aware Django/Jinja template formatter written in Rust that formats HTML and template syntax together.
- [DjHTML](https://github.com/rtts/djhtml) A pure-Python Django/Jinja template indenter without dependencies.
- [prettier-plugin-jinja-template](https://github.com/davidodenwald/prettier-plugin-jinja-template) Prettier plugin for formatting Jinja and Django templates.
- [Twig-CS-Fixer](https://github.com/VincentLanglet/Twig-CS-Fixer) A PHP tool that lints and automatically fixes Twig coding-standard issues.
