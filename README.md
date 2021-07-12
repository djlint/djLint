# djlint

Simple Django template linter.

## Install

```sh
pip install djlint
```

## Usage

```sh
djlint <file or path>
```

## Optional args

| Arg | Definition | Default |
|:----|:-----------|:--------|
-e, --extension | File extension to lint. | default=html


## Rules


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
