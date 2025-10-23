<h1 align="center">
  <br>
  <a href="https://www.djlint.com"><img src="https://raw.githubusercontent.com/djlint/djLint/master/docs/src/static/img/icon.png" alt="djLint Logo" width="270"></a>
  <br>
</h1>
<h3 align="center">🏗️ Maintainers needed, please reach out on discord or email!</h3>
<h4 align="center">The missing formatter and linter for HTML templates.</h4>

<p align="center">
    <a href="https://twitter.com/intent/tweet?text=djLint%20%7C%20The%20missing%20formatter%20and%20linter%20for%20HTML%20templates.&url=https://djlint.com/&hashtags=djlint,html-templates,django,jinja,developers"><img alt="tweet" src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social" /></a>
    <a href="https://discord.gg/taghAqebzU">
     <img src="https://badgen.net/discord/online-members/taghAqebzU?icon=discord&label" alt="Discord Chat">
   </a>
    </p>
    <p align="center">
   <a href="https://codecov.io/gh/djlint/djlint">
     <img src="https://codecov.io/gh/djlint/djlint/branch/master/graph/badge.svg?token=eNTG721BAA" alt="Codecov Status">
   </a>
   <a href="https://www.codacy.com/gh/djlint/djlint/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=djlint/djlint&amp;utm_campaign=Badge_Grade">
     <img src="https://app.codacy.com/project/badge/Grade/dba6338b0e7a4de896b45b382574f369" alt="Codacy Status">
   </a>
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

<h4 align="center"><a href="https://www.djlint.com">How to use</a> • <a href="https://www.djlint.com/ru/">Как пользоваться</a> • <a href="https://www.djlint.com/fr/">Utilisation</a></h4>
<h4 align="center">What lang are you using?</h4>

<p align="center">
   <a href="https://djlint.com/docs/languages/django/">Django</a> • <a href="https://djlint.com/docs/languages/jinja/">Jinja</a> • <a href="https://djlint.com/docs/languages/nunjucks/">Nunjucks</a> • <a href="https://djlint.com/docs/languages/twig/">Twig</a> • <a href="https://djlint.com/docs/languages/handlebars/">Handlebars</a> • <a href="https://djlint.com/docs/languages/mustach/">Mustache</a> • <a href="https://djlint.com/docs/languages/golang/">GoLang</a> • <a href="https://djlint.com/docs/languages/angular/">Angular</a>
</p>

<p align="center">
  <img src="https://github.com/djlint/djLint/blob/aa9097660d4a2e840450de5456f656c42bc7dd34/docs/src/static/img/demo-min.gif" alt="demo" width="600">
</p>

## 🤔 For What?

Once upon a time all the other programming languages had a formatter and linter. Css, javascript, python, the c suite, typescript, ruby, php, go, swift, and you know the others. The cool kids on the block.

HTML templates were left out there on their own, in the cold, unformatted and unlinted :( The dirty corner in your repository. Something had to change.

**djLint is a community build project to and add consistency to html templates.**

## ✨ How?

Grab it with `pip`

```bash
pip install djlint
```

_Or with the npm experimental install - Note, this requires python and pip to be on your system path._

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

Or use ``pre-commit`` to reformat, then check !

```yaml
  - repo: https://github.com/djlint/djLint
    rev: v1.36.4  # use latest version instead
    hooks:
      - id: djlint  # For an exhaustive list check 'id' in the project's '.pre-commit-hooks.yaml'
        args: ["--reformat"]
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

**⚠️ Help Needed! ⚠️** _Good with python?_ djLint was an experimental project and is catching on with other devs. Help out with a rewrite of the formatter to improve speed and html style for edge cases. Contribute on the [2.0 branch](https://github.com/djlint/djLint/tree/block_indent)

## 🏃 Other Tools Of Note

- [DjHTML](https://github.com/rtts/djhtml) A pure-Python Django/Jinja template indenter without dependencies.
- [HTMLHint](https://htmlhint.com) Static code analysis tool you need for your HTML
- [curlylint](https://www.curlylint.org) Experimental HTML templates linting for Jinja, Nunjucks, Django templates, Twig, Liquid
