---
title: Django Template Linter and Formatter
keywords: django, djlint, django template linter, django template formatter, format django templates
description: djLint is a django template linter and a django template formatter! Take advantage of the pre-build profile when linting and formatting your templates with djLint.
tool: django
---

# {{ title }}

{{ description }}

**[What is Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Using the Command Line

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Or, Use a Config File

Configure djLint in your projects `pyproject.toml`.

```toml
[tool.djlint]
profile="{{ tool }}"
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>

## Real Life Examples!

<div class="mb-5">

- [Django](https://github.com/django/django) source code [reformatted](https://github.com/Riverside-Healthcare/djLint/compare/django-source...Riverside-Healthcare:djLint:django-djlint)
- [Wagtail](https://github.com/wagtail/wagtail) source code [reformatted](https://github.com/Riverside-Healthcare/djLint/compare/wagtail-source...Riverside-Healthcare:djLint:wagtail-djlint)

</div>
