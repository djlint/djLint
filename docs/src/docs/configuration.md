---
description: djLint configuration for HTML Template Linting and Formatting. Take advantage of the many formatter options.
title: Configuration
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, configuration
---

# Configuration

Configuration is done either through your projects `pyproject.toml` file, or a `.djlintrc` file. Command line args will always override any settings in `pyproject.toml`.

The format for ``pyproject.toml`` is ``toml``.

```ini
[tool.djlint]
<config options>
```
The format for ``.djlintrc`` is ``json``.

```json
{
  "option": "value"
}
```

## ignore

Ignore linter codes.

Usage:

**pyproject.toml**

```ini
ignore="H014,H015"
```

**.djlintrc**

```json
{
  "ignore": "H014,H015"
}
```

## extension

Use to only find files with a specific extension.

Usage:

**pyproject.toml**

```ini
extension="html.dj"
```

**.djlintrc**

```json
{
  "extension": "html.dj"
}
```

## custom_blocks

Use to indent custom code blocks. For example {% raw %}`{% toc %}...{% endtoc %}`{% endraw %}

Usage:

**pyproject.toml**

```ini
custom_blocks="toc,example"
```

**.djlintrc**

```json
{
  "custom_blocks": "toc,example"
}
```

## custom_html

Use to indent custom HTML tags. For example `<mjml>` or `<simple-greeting>` or `<mj-\w+>`

Usage:

**pyproject.toml**

```ini
custom_html="mjml,simple-greeting,mj-\\w+"
```

**.djlintrc**

```json
{
  "custom_html": "mjml,simple-greeting,mj-\\w+"
}
```

## indent

Use to change the code indentation. Default is 4 (four spaces).

Usage:

**pyproject.toml**

```ini
indent=3
```

**.djlintrc**

```json
{
  "indent": "3"
}
```

## exclude

Override the default exclude paths.

Usage:

**pyproject.toml**

```ini
exclude=".venv,venv,.tox,.eggs,..."
```

**.djlintrc**

```json
{
  "exclude": ".venv,venv,.tox,.eggs,..."
}
```

## extend_exclude

Add additional paths to the default exclude.

Usage:

**pyproject.toml**

```ini
extend_exclude=".custom"
```

**.djlintrc**

```json
{
  "extend_exclude": ".custom"
}
```

## blank_line_after_tag

Add an additional blank line after {% raw %}`{% <tag> ... %}`{% endraw %} tag groups.

Usage:

**pyproject.toml**

```ini
blank_line_after_tag="load,extends,include"
```

**.djlintrc**

```json
{
  "blank_line_after_tag": "load,extends,include"
}
```

## profile

Set a profile for the template language. The profile will enable linter rules that apply to your template language, and may also change reformatting. For example, in `handlebars` there are no spaces inside {% raw %}`{{#if}}`{% endraw %} tags.

Options:

:::content

- html (default)
- django
- jinja
- nunjucks (for nunjucks and twig)
- handlebars (for handlebars and mustache)
- golang
- angular
  :::

Usage:

**pyproject.toml**

```ini
profile="django"
```

**.djlintrc**

```json
{
  "profile": "django"
}
```

## require_pragma

Only format or lint files that starts with a comment with only the text 'djlint:on'. The comment can be a HTML comment or a comment in the template language defined by the profile setting. If no profile is specified, a comment in any of the template languages is accepted.

Usage:

**pyproject.toml**

```ini
require_pragma=true
```

**.djlintrc**

```json
{
  "require_pragma": "true"
}
```

{% raw %}

```html
<!-- djlint:on -->
or {# djlint:on #} or {% comment %} djlint:on {% endcomment %} or {{ /*
djlint:on */ }} or {{!-- djlint:on --}}
```

{% endraw %}

## max_line_length

Formatter will attempt to put some html and template tags on a single line instead of wrapping them if the line length will not exceed this value.

Usage:

**pyproject.toml**

```ini
max_line_length=120
```

**.djlintrc**

```json
{
  "max_line_length": "120"
}
```

## max_attribute_length

Formatter will attempt to wrap tag attributes if the attribute length exceeds this value.

Usage:

**pyproject.toml**

```ini
max_attribute_length=10
```

**.djlintrc**

```json
{
  "max_attribute_length": "10"
}
```

## use_gitignore

Add .gitignore excludes to the default exclude.

Usage:

**pyproject.toml**

```ini
use_gitignore=True
```

**.djlintrc**

```json
{
  "use_gitignore": "True"
}
```

## format_attribute_template_tags

Formatter will attempt to format template syntax inside of tag attributes. Disabled by default.

Usage:

**pyproject.toml**

```ini
format_attribute_template_tags=true
```

**.djlintrc**

```json
{
  "format_attribute_template_tags": "true"
}
```

For example, with this option enabled, the following html will be acceptable:

```html
{% raw %}
<input class="{% if this %}
                  then something neat
              {% else %}
                  that is long stuff asdf and more even
              {% endif %}"
/>
{% endraw %}
```

## linter_output_format

Customize order of output message. Default="{code} {line} {message} {match}". If `{filename}` is not include in message, then the output will be grouped by file and a header will automatically be added to each group.

Optional variables:
::: content
- `{filename}`
- `{line}`
- `{code}`
- `{message}`
- `{match}`
:::

Usage:

**pyproject.toml**

```ini
linter_output_format="{filename}:{line}: {code} {message} {match}"
```

**.djlintrc**

```json
{
  "linter_output_format": "{filename}:{line}: {code} {message} {match}"
}
```

## preserve_leading_space

Preserve leading space on text, where possible. Ideal for non-html template files where text indent is intentional.

Usage:

**flag**

```bash
--preserve-leading-space
```

**pyproject.toml**

```ini
preserve_leading_space=true
```

**.djlintrc**

```json
{
  "preserve_leading_space": true
}
```

