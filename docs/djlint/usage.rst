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
---------------

Foramtting is a beta tool. ``--check`` the output before applying changes.

Reformatting does not work with long json/html embedded into attribute data.

To review what may change in formatting run:

.. code:: sh

    djlint . --check --ignore="H014,H017"

To format the code and update files run:

.. code:: sh

    djlint . --reformat --indent=3

Ignoring Code
-------------

Code can be skipped by the linter and formatter by wrapping in djlint tags:

.. code:: html

   <!-- djlint:off -->
       <bad html to ignore>
   <!-- djlint:on -->

   or

   {# djlint:off #}
       <bad html to ignore>
   {# djlint:on #}

   or

   {% comment %} djlint:off {% endcomment %}
       <bad html to ignore>
   {% comment %} djlint:on {% endcomment %}

   or

   {{ /* djlint:off */ }}
       <bad html to ignore>
   {{ /* djlint:on */ }}

   or

   {{!-- djlint:off --}}
       <bad html to ignore>
   {{!-- djlint:on --}}


Stdin vs Path
-------------

djLint also works with stdin.

.. code:: sh

    echo "<div></div>" | djlint -

Stdin can also be used to reformat code. The output will be only the formatted code without messages.

.. code:: sh

    echo "<div></div>" | djlint - --reformat

Output -

.. code:: html

    <div></div>


CLI Args
--------

.. code:: sh

    Usage: python -m djlint [OPTIONS] SRC ...

      djLint · lint and reformat HTML templates.

    Options:
      --version             Show the version and exit.
      -e, --extension TEXT  File extension to check [default: html]
      -i, --ignore TEXT     Codes to ignore. ex: "H014,H017"
      --reformat            Reformat the file(s).
      --check               Check formatting on the file(s).
      --indent INTEGER      Indent spacing. [default: 4]
      --quiet               Do not print diff when reformatting.
      --profile TEXT        Enable defaults by template language. ops: django,
                            jinja, nunjucks, handlebars, golang
      --require-pragma      Only format or lint files that starts with a comment
                            with the text 'djlint:on'
      --lint                Lint for common issues. [default option]
      --use-gitignore       Use .gitignore file to extend excludes.
      -h, --help            Show this message and exit.
