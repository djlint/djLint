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

Formatting is a beta tool. ``--check`` the output before applying changes.

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


As a pre-commit hook
--------------------

djLint can also be used as a `pre-commit <https://pre-commit.com>`_ hook.

The repo provides multiple pre-configured hooks for specific djLint profiles (it just pre-sets the ``--profile`` argument and tells pre-commit which file extensions to look for):

* ``djlint-django`` for Django templates:

This will look for files matching ``templates/**.html`` and set ``--profile=django``.

* ``djlint-jinja``

This will look for files matching ``*.j2`` and set ``--profile=jinja``.

* ``djlint-nunjucks``

This will look for files matching ``*.njk`` and set ``--profile=nunjucks``.

* ``djlint-handlebars``

This will look for files matching ``*.hbs`` and set ``--profile=handlebars``.

* ``djlint-golang``

This will look for files matching ``*.tmpl`` and set ``--profile=golang``.

Note that these predefined hooks are sometimes too conservative in the inputs they accept (your templates may be using a different extension) so pre-commit explicitly allows you to override any of these pre-defined options.

Default Django example
^^^^^^^^^^^^^^^^^^^^^^

.. code:: yaml

    repos:
    - repo: https://github.com/Riverside-Healthcare/djLint
        rev: 0.5.10  # grab latest tag from GitHub
        hooks:
          - id: djlint-django


Handlebars with .html extension instead of .hbs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: yaml

    repos:
    - repo: https://github.com/Riverside-Healthcare/djLint
        rev: 0.5.10  # grab latest tag from GitHub
        hooks:
          - id: djlint-handlebars
            files: "\\.html"

You can use the ``files`` or ``exclude`` parameters to constrain each hook to its own directory, allowing you to support multiple templating languages within the same repo.