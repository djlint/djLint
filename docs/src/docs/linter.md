---
description: djLint HTML Template linter includes over 30 rules! Find the definitions here. Easily expand with include custom rules!
title: Linter Rules
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, rules
---

# Linter Usage

djLint includes many rules to check the style and validity of your templates. Take full advantage of the linter by configuring it to use a preset profile for the template language of your choice.

```bash
djlint /path/to/templates --lint

# with custom extensions
djlint /path/to/templates -e html.dj --profile=django

# or to file
djlint /path/to/this.html.j2  --profile=jinja
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>

## Custom Rules

Create a file `.djlint_rules.yaml` alongside your `pyproject.toml`. Rules can be added to this files and djLint will pick them up.

A good rule follows this pattern:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Code Patterns

The first letter of a code follows the pattern:

::: content

- D: applies specifically to Django
- H: applies to html
- J: applies specifically to Jinja
- M: applies specifically to Handlebars
- N: applies specifically to Nunjucks
- T: applies generally to templates
  :::

## Rules

| Code | Meaning                                                                                      |
| ---- | -------------------------------------------------------------------------------------------- |
| D004 | (Django) Static urls should follow {% raw %}`{% static path/to/file %}`{% endraw %} pattern. |
| D018 | (Django) Internal links should use the {% raw %}`{% url ... %}`{% endraw %} pattern.         |
| H005 | Html tag should have `lang` attribute.                                                       |
| H006 | `img` tag should have `height` and `width` attributes.                                       |
| H007 | `<!DOCTYPE ... >` should be present before the html tag.                                     |
| H008 | Attributes should be double quoted.                                                          |
| H009 | Tag names should be lowercase.                                                               |
| H010 | Attribute names should be lowercase.                                                         |
| H011 | Attribute values should be quoted.                                                           |
| H012 | There should be no spaces around attribute `=`.                                              |
| H013 | `img` tag should have alt attributes.                                                        |
| H014 | More than 2 blank lines.                                                                     |
| H015 | Follow `h` tags with a line break.                                                           |
| H016 | Missing `title` tag in html.                                                                 |
| H017 | Tag should be self closing.                                                                  |
| H019 | Replace `javascript:abc()` with `on_` event and real url.                                    |
| H020 | Empty tag pair found. Consider removing.                                                     |
| H021 | Inline styles should be avoided.                                                             |
| H022 | Use HTTPS for external links.                                                                |
| H023 | Do not use entity references.                                                                |
| H024 | Omit type on scripts and styles.                                                             |
| H025 | Tag seems to be an orphan.                                                                   |
| H026 | Empty id and class tags can be removed.                                                      |
| H029 | Consider using lowercase form method values.                                                 |
| H030 | Consider adding a meta description.                                                          |
| H031 | Consider adding meta keywords.                                                               |
| H033 | Extra whitespace found in form action.                                                       |
| J004 | (Jinja) Static urls should follow {% raw %}`{{ url_for('static'..) }}`{% endraw %} pattern.  |
| J018 | (Jinja) Internal links should use the {% raw %}`{% url ... %}`{% endraw %} pattern.          |
| T001 | Variables should be wrapped in a single whitespace. Ex: {% raw %}`{{ this }}`{% endraw %}    |
| T002 | Double quotes should be used in tags. Ex {% raw %}`{% extends "this.html" %}`{% endraw %}    |
| T003 | Endblock should have name. Ex: {% raw %}`{% endblock body %}`{% endraw %}.                   |
| T027 | Unclosed string found in template syntax.                                                    |
| T028 | Consider using spaceless tags inside attribute values. {% raw %}`{%- if/for -%}`{% endraw %} |
| T032 | Extra whitespace found in template tags.                                                     |
| T034 | Did you intend to use {% raw %}{% ... %} instead of {% ... }%? {% endraw %}                  |

### Adding Rules

We welcome pull requests with new rules!

A good rule consists of

::: content

- Name
- Code
- Message - Message to display when error is found.
- Flags - Regex flags. Defaults to re.DOTALL. ex: re.I|re.M
- Patterns - regex expressions that will find the error.
- Exclude - Optional list of profiles to exclude rule from.
  :::

Please include a test to validate the rule.
