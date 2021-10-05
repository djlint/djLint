![djLint Logo](https://raw.githubusercontent.com/Riverside-Healthcare/djlint/master/docs/_static/icon.png)

Find common formatting issues and *reformat* HTML templates.

***[Django](https://django.readthedocs.io/en/stable/ref/templates/language.html) · [Jinja](https://jinja2docs.readthedocs.io/en/stable/) · [Nunjucks](https://mozilla.github.io/nunjucks/) · [Handlebars](https://handlebarsjs.com) · [Mustache](http://mustache.github.io/mustache.5.html) · [GoLang](https://golang.org/doc/)***

Ps, ``--check`` it out on other templates as well!

[![codecov](https://codecov.io/gh/Riverside-Healthcare/djlint/branch/master/graph/badge.svg?token=eNTG721BAA)](https://codecov.io/gh/Riverside-Healthcare/djlint) [![test](https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml/badge.svg)](https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/dba6338b0e7a4de896b45b382574f369)](https://www.codacy.com/gh/Riverside-Healthcare/djlint/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Riverside-Healthcare/djlint&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/5febe4111a36c7e0d2ed/maintainability)](https://codeclimate.com/github/Riverside-Healthcare/djlint/maintainability) [![Downloads](https://pepy.tech/badge/djlint)](https://pepy.tech/project/djlint)[![chat](https://img.shields.io/badge/chat-discord-green)](https://discord.gg/taghAqebzU) [![PyPI](https://img.shields.io/pypi/v/djlint)](https://pypi.org/project/djlint/)

## Documentation

Read the [documentation](https://djlint.com)

## Installation and Usage

**djLint** can be installed with `pip install djlint`, and is easy to run:

```sh
# to lint a directory
djlint /path

# to lint a directory with custom extension
djlint /path -e html.dj

# to check formatting on a file
djlint /path/file.html.j2 --check

# to reformt a directory without printing the file diff
djlint /path --reformat --quiet

# using stdin
echo "<div></div>" | djlint -

```

## Show your format

Add a badge to your projects ```readme.md```:

```md
[![Code style: djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://github.com/Riverside-Healthcare/djlint)
```

Add a badge to your ```readme.rst```:

```rst
.. image:: https://img.shields.io/badge/html%20style-djlint-blue.svg
   :target: https://github.com/Riverside-Healthcare/djlint
```
Looks like this:

[![djLint](https://img.shields.io/badge/html%20style-djLint-blue.svg)](https://github.com/Riverside-Healthcare/djlint)


## Contributing

Send a pr with a new feature, or checkout the [issue](https://github.com/Riverside-Healthcare/djlint/issues) list and help where you can.
