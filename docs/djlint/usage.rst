Getting Started
================

Installation from `Pypi <https://pypi.org/project/djlint/>`__
--------------------------------------------------------------

.. code:: sh

    pip install djlint

Linter Usage
------------

.. code:: sh

    djlint src # file or path

    # with custom extensions
    djlint src -e html.dj

Formatter Usage
-----------------

Foramtting is a beta tool. ``--check`` the output before applying changes.

Reformatting does not work with long json/html embedded into attribute data.

To check what may change in formatting run:

.. code:: sh

    djlint . --check --ignore="H014,H017"

To format code run:

.. code:: sh

    djlint . --reformat --indent=3

Stdin vs Path
-------------

djLint also works with stdin.

.. code:: sh

    echo "<div></div>" | djlint -

CLI Args
--------

.. code:: sh

    Usage: djlint [OPTIONS] SRC ...

    Djlint django template files.

    Options:
      -e, --extension TEXT  File extension to lint  [default: html]
      -i, --ignore "Codes"  Rules to be ignored. ex: "H014,H017"
      --indent              Indent spacing. ex: 3
      --reformat            Reformat the file(s).
      --check               Check formatting on the file(s).
      --quiet               Do not print diff when reformatting.
      --profile             Enable defaults by template language.
                            ops: django, jinja, nunjucks, handlebars
      -h, --help            Show this message and exit.
      --version             Get djLint version
