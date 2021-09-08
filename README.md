![djLint Logo](https://raw.githubusercontent.com/Riverside-Healthcare/djlint/master/docs/_static/icon.png)

Find common formatting issues and *reformat* HTML templates.

<style>
      .types {
        text-align: center;
        font-size: 110%;
        font-style: italic;
        width: 100%;
        position: relative;
      }

      .types::after {
        position: absolute;
        top: 11px;
        left:0;
        right:0;
        border: 1px solid rgba(0,0,0,.2);
        content: "";
        z-index: -1;
      }

      .types span {
        padding: 15px;
        margin: 5px;
        background: #fff;
        z-index:1;
      }
   </style>
   <p class="types">
      <span>Django</span>
      <span>Jinja</span>
      <span>Nunjucks</span>
      <span>Handlebars</span>
   </p>

Ps, ```--check``` it out on Jinja and Handlebar templates as well!

[![codecov](https://codecov.io/gh/Riverside-Healthcare/djlint/branch/master/graph/badge.svg?token=eNTG721BAA)](https://codecov.io/gh/Riverside-Healthcare/djlint) [![test](https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml/badge.svg)](https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/dba6338b0e7a4de896b45b382574f369)](https://www.codacy.com/gh/Riverside-Healthcare/djlint/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Riverside-Healthcare/djlint&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/5febe4111a36c7e0d2ed/maintainability)](https://codeclimate.com/github/Riverside-Healthcare/djlint/maintainability) [![Downloads](https://pepy.tech/badge/djlint)](https://pepy.tech/project/djlint)[![chat](https://img.shields.io/badge/chat-discord-green)](https://discord.gg/taghAqebzU)

## Documentation

Read the [documentation](https://djlint.readthedocs.io)

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

[![djlint](https://img.shields.io/badge/html%20style-djlint-blue.svg)](https://github.com/Riverside-Healthcare/djlint)


## Contributing

Checkout the [issue](https://github.com/Riverside-Healthcare/djlint/issues) list and help where you can.
