Best Practices
==============

Conditional Attributes
----------------------

Sometimes conditions are used to add classes to a tag. djLint removes whitespace inside conditional statements.

This pattern is recommended:

.. code:: html

    <div class="class1 {% if condition %}class2{% endif %}">content</div>
                      ^ space here

This pattern is not recommended:

.. code:: html

    <div class="class1{% if condition %} class2{% endif %}">content</div>
                                        ^ space here
