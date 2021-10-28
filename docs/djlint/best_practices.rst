Best Practices
==============

Spaces Around Conditional Attributes
------------------------------------

Sometimes conditions are used to add classes to a tag. djLint removes whitespace inside conditional statements.

This pattern is recommended:

.. code:: html

    <div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                      ^ space here

This pattern is not recommended:

.. code:: html

    <div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                        ^ space here

Spaceless Conditional Attributes
--------------------------------

Conditional attributes should use spaceless tags, for example ``{% if a -%}`` in nunjuck and jinja, to remove spaces inside the.

djLint will format long attributes onto multiple lines, and the whitespace saved inside of attributes could break your code.

This pattern is recommended:

.. code:: html

    <input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"/>
                                 ^                       ^      ^        ^-- spaceless tags

This pattern is not recommended:

.. code:: html

    <input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}"/>

After formatting this could look like:

.. code:: html

    <input value="{% if database %}
                      {{ database.name }}
                  {% else %}
                      blah
                  {% endif %}"/>
