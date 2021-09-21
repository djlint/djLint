Configuration
=============

Ignoring Linter Rules
---------------------

Linter rules can be ignored with the `-i` or `--ignore` flag.

For example:

.. code:: bash

   djlint src -i "W013,W014"


Pyproject.toml Configuration
----------------------------

Configuration options can also be added to your projects `pyproject.toml` file. Command line args will always override any settings in `pyproject.toml`.

.. code:: toml

   [tool.djlint]
   ignore = "W013"
   extension = "html.dj"
   custom_blocks = "toc,example" # custom code blocks {% toc %}...{% endtoc %}
   indent = "    " # change indentation level
   exclude = ".venv,venv,.tox,.eggs,..." # override the default set of excluded paths
   extend_exclude = ".custom" # add paths to exclude
