# djlint

Simple Django template linter and reformatter. Ps, reformatting might work with Jinja and Handlebar templates as well! Test it out with the `--check` flag.

[![codecov](https://codecov.io/gh/Riverside-Healthcare/djlint/branch/master/graph/badge.svg?token=eNTG721BAA)](https://codecov.io/gh/Riverside-Healthcare/djlint)
[![test](https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml/badge.svg)](https://github.com/Riverside-Healthcare/djlint/actions/workflows/test.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/dba6338b0e7a4de896b45b382574f369)](https://www.codacy.com/gh/Riverside-Healthcare/djlint/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Riverside-Healthcare/djlint&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/5febe4111a36c7e0d2ed/maintainability)](https://codeclimate.com/github/Riverside-Healthcare/djlint/maintainability)

## Install

```sh
pip install djlint
```
## Linter Usage

```sh
djlint src # file or path

# with custom extensions
djlint src -e html.dj
```

## Reformatter Usage

Reforamtting is beta. Check the output before applying changes. Please PR any changes needed 👍🏽

```sh
djlint src --reformat --check

djlint src --reformat
```

## Optional args

| Arg | Definition | Default |
|:----|:-----------|:--------|
-e, --extension | File extension to lint. | default=html
--check | Checks file formatting |
--reformat | Reformats html |

## Linter Rules

### Error Codes

| Code | Meaning                                                            |
|------|--------------------------------------------------------------------|
| E001 | Variables should be wrapped in a single whitespace. Ex: {{ this }} |
| E002 | Double quotes should be used in tags. Ex {% extends "this.html" %} |

### Warning Codes

| Code | Meaning                                                      |
|------|--------------------------------------------------------------|
| W003 | Endblock should have name. Ex: {% endblock body %}.          |
| W004 | Status urls should follow {% static path/to/file %} pattern. |
| W005 | Html tag should have lang attribute. |
| W006 | Img tag should have alt, height and width attributes. |
| W007 | \<!DOCTYPE ... > should be present before the html tag. |
| W008 | Attributes should be double quoted. |
| W009 | Tag names should be lowercase. |
| W010 | Attribute names should be lowercase. |
| W011 | Attirbute values should be quoted. |
| W012 | There should be no spaces around attribute =. |
| W013 | Line is longer than 99 chars. |
| W014 | More than 2 blank lines. |
| W015 | Follow h tags with a blank line. |
| W016 | Missging title tag in html. |

## Adding Rules

A good rule consists of

  - Name
  - Code - Codes beginning with "E" signify error, and "W" warning.
  - Message - Message to display when error is found.
  - Patterns - regex expressions that will find the error.

## Contributing - Please Help!

Checkout the issue list and help where you can!
