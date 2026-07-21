<h1 align="center">
  <br>
  <a href="https://djlint.com"><img src="https://raw.githubusercontent.com/djlint/djLint/master/docs/src/static/img/icon.png" alt="djLint Logo" width="270"></a>
  <br>
</h1>
<h4 align="center">The missing formatter and linter for HTML templates.</h4>

<p align="center">
   <a href="https://pypi.org/project/djlint/">
     <img src="https://pepy.tech/badge/djlint" alt="Downloads">
   </a>
   <a href="https://discord.gg/taghAqebzU">
     <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Fv10%2Finvites%2FtaghAqebzU%3Fwith_counts%3Dtrue&query=%24.approximate_presence_count&label=discord&suffix=%20online&logo=discord&logoColor=white&color=5865F2" alt="Discord">
   </a>
</p>

<h4 align="center"><a href="https://djlint.com">How to use</a> • <a href="https://djlint.com/ru/">Как пользоваться</a> • <a href="https://djlint.com/fr/">Utilisation</a> • <a href="https://djlint.com/zh/">如何使用</a></h4>
<h4 align="center">What lang are you using?</h4>

<p align="center">
   <a href="https://djlint.com/docs/languages/django/">Django</a> • <a href="https://djlint.com/docs/languages/jinja/">Jinja</a> • <a href="https://djlint.com/docs/languages/twig/">Twig</a> • <a href="https://djlint.com/docs/languages/nunjucks/">Nunjucks</a> • <a href="https://djlint.com/docs/languages/handlebars/">Handlebars</a> • <a href="https://djlint.com/docs/languages/liquid/">Liquid</a> • <a href="https://djlint.com/docs/languages/golang/">Go templates</a> • <a href="https://djlint.com/docs/languages/angular/">Angular</a> • <a href="https://djlint.com/docs/languages/mustache/">Mustache</a> • <a href="https://djlint.com/docs/languages/tera/">Tera</a> • <a href="https://djlint.com/docs/languages/askama/">Askama</a>
</p>

## 🤔 For What?

Every language in your stack has a formatter and a linter. HTML templates are the exception. Generic HTML tools can't parse `{% %}` and `{{ }}`, and template engines don't care what the markup around them looks like. Templates end up in a tooling blind spot: drifting indentation, mismatched tags and inconsistent spacing that survive every code review.

djLint covers that blind spot. It understands HTML _and_ the template syntax inside it, with profiles for Django, Jinja, Twig, Nunjucks, Handlebars, Liquid, Go templates and more.

Take a template only its author could love:

```django
{% block content %}
<SECTION class="posts">


<h2>Latest posts</h2>
{%if posts%}
<ul>
{% for post in posts %}
<li>
<a href="{% url 'post' post.slug %}" class="post-link {%if post.featured%}is-featured{%endif%}" data-analytics-id="post-{{post.id}}" aria-label="Read {{post.title}}">{{post.title|title}}</a>
</li>
{% endfor %}
</ul>
{%else%}
<p>No posts yet.</p>
{%endif%}
</SECTION>
{% endblock %}
```

One `djlint --reformat --single-attribute-per-line` later:

```django
{% block content %}
    <section class="posts">
        <h2>Latest posts</h2>
        {% if posts %}
            <ul>
                {% for post in posts %}
                    <li>
                        <a
                            href="{% url 'post' post.slug %}"
                            class="post-link {% if post.featured %}is-featured{% endif %}"
                            data-analytics-id="post-{{ post.id }}"
                            aria-label="Read {{ post.title }}"
                        >{{ post.title|title }}</a>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p>No posts yet.</p>
        {% endif %}
    </section>
{% endblock %}
```

One command rebuilt the indentation, fixed the tag case, split the long tag into one attribute per line, normalized the template tags and collapsed stray blank lines.

And the linter catches what formatting can't fix: orphan tags, missing `alt` attributes, hard-coded URLs and dozens of other checks.

**[Try it on your own templates in the online playground →](https://djlint.com/demo/)**

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
djlint . --lint
```

Check your format

```bash
djlint . --check
```

Fix my format!

```bash
djlint . --reformat --single-attribute-per-line
```

Set a `--profile` to enable the rules and formatting of your template engine

```bash
djlint . --reformat --single-attribute-per-line --profile=django
```

Or use `pre-commit` to reformat, then lint!

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v1.42.1 # use latest version instead
    hooks:
      - id: djlint-reformat
      - id: djlint
```

## 🧩 Editors

- **VS Code**: install the [djLint extension](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) (also on [Open VSX](https://open-vsx.org/extension/monosans/djlint)).
- **neovim, Sublime Text, MegaLinter and more**: see the [integrations docs](https://djlint.com/docs/integrations/).

## 💙 Like it?

Add a badge to your projects `readme.md`:

```md
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://djlint.com)
```

Add a badge to your `readme.rst`:

```rst
.. image:: https://img.shields.io/badge/html%20style-djlint-blue.svg
   :target: https://djlint.com
```

Looks like this:

[![djLint](https://img.shields.io/badge/html%20style-djLint-blue.svg)](https://github.com/djlint/djlint)

## 🛠️ Can I help?

Yes!

_Would you like to add a rule to the linter?_ Take a look at the [linter docs](https://djlint.com/docs/linter/) and the [rule definitions](https://github.com/djlint/djLint/blob/master/src/djlint/rules.yaml).

Local setup takes two commands:

```bash
# install uv first: https://docs.astral.sh/uv/getting-started/installation/
uv sync

# run the test suite
uv run pytest
```

## 🏃 Other Tools Of Note

- [djade](https://github.com/adamchainz/djade) A fast Django template formatter that formats template syntax whilst leaving HTML as-is, and applies fixes for older Django versions.
- [djangofmt](https://github.com/UnknownPlatypus/djangofmt) A fast, HTML-aware Django/Jinja template formatter written in Rust that formats HTML and template syntax together.
- [DjHTML](https://github.com/rtts/djhtml) A pure-Python Django/Jinja template indenter without dependencies.
- [prettier-plugin-jinja-template](https://github.com/davidodenwald/prettier-plugin-jinja-template) Prettier plugin for formatting Jinja and Django templates.
- [prettier-plugin-twig](https://github.com/zackad/prettier-plugin-twig) Prettier plugin for formatting Twig templates.
- [Twig-CS-Fixer](https://github.com/VincentLanglet/Twig-CS-Fixer) A PHP tool that lints and automatically fixes Twig coding-standard issues.
- [ludtwig](https://github.com/MalteJanz/ludtwig) A fast Rust linter and formatter for Twig templates that also validates HTML structure and supports auto-fix.
