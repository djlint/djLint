---
title: "Best Practices"
description: "Best practices for using djLint to format HTML templates."
sidebar:
  label: "Best practices"
---

## Spaces Around Conditional Attributes

Sometimes conditions are used to add classes to a tag. djLint removes whitespace inside conditional statements.

This pattern is recommended:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

This pattern is not recommended:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` and Spaceless Conditional Attributes

If the `format_attribute_template_tags` option is enabled, conditional attributes should use spaceless tags, for example `{% if a -%}` in nunjucks and jinja, to remove the spaces inside the tag.

djLint will format long attributes onto multiple lines, and the whitespace saved inside of attributes could break your code.

This pattern is recommended:

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

Each marked position is a spaceless tag.

This pattern is not recommended:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

After formatting this could look like:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
