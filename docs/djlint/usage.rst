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

Reformatter Usage
-----------------

Reforamtting is a beta product. Check the output before applying changes.

Reformatting does not work with long json/html embedded into attribute data.

To check what may change in formatting run:

.. code:: sh

    djlint src --check --ignore="W013,W014"

To reformat run:

.. code:: sh

    djlint src --reformat

CLI Args
-------------

.. code:: sh

    Usage: djlint [OPTIONS] SRC ...

    Djlint django template files.

    Options:
      -e, --extension TEXT  File extension to lint  [default: html]
      -i, --ignore "Codes"  Rules to be ignored. ex: "W013,W014"
      --reformat            Reformat the file(s).
      --check               Check formatting on the file(s).
      --quiet               Do not print diff when reformatting.
      -h, --help            Show this message and exit.
