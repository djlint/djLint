.. meta::
    :title lang=en: djLint | HTML Template Linter and Formatter
    :description lang=en:
        Find common syntax errors, reformat to make your HTML templates shine!
        Supports django, jinja, nunjucks, twig, handlebars, mustache, golang, and more!
    :keywords lang=en: template linter, template formatter, djLint, HTML, templates, formatter, linter


HTML Template Linter and Formatter
==================================

.. toctree::
   :hidden:
   :glob:
   :maxdepth: 1
   :titlesonly:

   Welcome<self>
   docs/getting_started
   docs/linter_rules
   docs/formatter
   docs/configuration
   docs/best_practices
   docs/changelog
   docs/integrations

.. toctree::
   :hidden:

   GitHub ↪ <https://github.com/Riverside-Healthcare/djlint>
   PyPI ↪ <https://pypi.org/project/djlint/>
   Chat ↪ <https://discord.gg/taghAqebzU>

Lint for common HTML/template issues and *format* HTML templates.

*Django · Jinja · Nunjucks · Twig · Handlebars · Mustache · GoLang*

Ps, ``--check`` it out on other templates as well!

.. image:: /_static/demo.gif

|codecov| |test| |Codacy Badge| |Maintainability| |Downloads| |chat| |version|

.. note:: djLint is not an html parser or syntax validator.


Show your format
----------------

Add a badge to your projects `readme.md`:

.. code-block:: md

   [![Code style: djLint](https://img.shields.io/badge/html%20style-djLint-blue.svg)](https://github.com/Riverside-Healthcare/djlint)


Add a badge to your `readme.rst`:

.. code-block:: rst

   .. image:: https://img.shields.io/badge/html%20style-djLint-blue.svg
      :target: https://github.com/Riverside-Healthcare/djlint


Looks like this:

.. image:: https://img.shields.io/badge/html%20style-djLint-blue.svg
   :target: https://github.com/Riverside-Healthcare/djlint


Contributing - Please Help!
---------------------------

Send a pr with a new feature, or checkout the `issue <https://github.com/Riverside-Healthcare/djlint/issues>`_ list and help where you can.

.. |codecov| image:: https://codecov.io/gh/Riverside-Healthcare/djlint/branch/master/graph/badge.svg?token=eNTG721BAA
   :target: https://codecov.io/gh/Riverside-Healthcare/djlint
.. |test| image:: https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml/badge.svg
   :target: https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml
.. |Codacy Badge| image:: https://app.codacy.com/project/badge/Grade/dba6338b0e7a4de896b45b382574f369
   :target: https://www.codacy.com/gh/Riverside-Healthcare/djlint/dashboard?utm_source=github.com&utm_medium=referral&utm_content=Riverside-Healthcare/djlint&utm_campaign=Badge_Grade
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/5febe4111a36c7e0d2ed/maintainability
   :target: https://codeclimate.com/github/Riverside-Healthcare/djlint/maintainability
.. |Downloads| image:: https://img.shields.io/pypi/dm/djlint.svg
   :target: https://pypi.org/project/djlint/
.. |chat| image:: https://img.shields.io/badge/chat-discord-green
   :target: https://discord.gg/taghAqebzU
.. |version| image:: https://img.shields.io/pypi/v/djlint
   :target: https://pypi.org/project/djlint/
   :alt: PyPI
