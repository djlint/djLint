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
