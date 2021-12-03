:description: Integrate djLint with your favorite editor. Auto format your templates with Pre-Commit. Lint with SublimeText.

.. meta::
    :title lang=en: djLint » Integrations
    :description lang=en:
        Integrate djLint with your favorite editor. Auto format
        your templates with Pre-Commit. Lint with SublimeText.
    :keywords lang=en: template linter, template formatter, djLint, HTML, templates, formatter, linter, integrations

Integrations
============

There are several editor integrations build for djLint.

Pre-Commit
----------

djLint can be used as a `pre-commit <https://pre-commit.com>`_ hook.

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

Note that these predefined hooks are sometimes too conservative in the inputs they accept (your templates may be using a different extension) so pre-commit explicitly allows you to override any of these pre-defined options. See the `pre-commit docs <https://pre-commit.com/#pre-commit-configyaml---hooks>`_ for additional configuration

Default Django example
^^^^^^^^^^^^^^^^^^^^^^

.. code:: yaml

    repos:
    - repo: https://github.com/Riverside-Healthcare/djLint
        rev: 0.5.10  # grab latest tag from GitHub
        hooks:
          - id: djlint-django


Handlebars with .html extension instead of .hbs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: yaml

    repos:
    - repo: https://github.com/Riverside-Healthcare/djLint
        rev: 0.5.10  # grab latest tag from GitHub
        hooks:
          - id: djlint-handlebars
            files: "\\.html"

You can use the ``files`` or ``exclude`` parameters to constrain each hook to its own directory, allowing you to support multiple template languages within the same repo.

SublimeText Linter
------------------

djLint can be used as a SublimeText Linter plugin. It can be installed via `package-control <https://packagecontrol.io/packages/SublimeLinter-contrib-djlint>`_.

1. ``cmd + shft + p``
2. Install SublimeLinter
3. Install SublimeLinter-contrib-djlint

Ensure djLint is installed in your global python, or on yout ``PATH``.

coc.nvim
--------

https://www.npmjs.com/package/coc-htmldjango
