# Changelog

[Semantic Versioning](https://semver.org/)

## [Unreleased]

### Fix

- Preserve attributes containing nested template blocks when wrapping long tags.
- Preserve template expressions used in dynamic HTML tag names.
- Preserve asterisks in HTML attribute names such as htmx response targets.
- Avoid adding trailing whitespace after function calls in multiline template expressions.
- Avoid false T002 reports for template tags inside HTML attributes.

## [1.40.7] - 2026-07-15

### Fix

- Preserve URLs enclosed in angle brackets inside template comments.

## [1.40.6] - 2026-07-13

### Performance and refactoring

- Replace repeated HTML regex scans with tokenization.

## [1.40.5] - 2026-07-12

### Fix

- Avoid false H037 reports when attribute names appear inside quoted values or other attribute names.
- Preserve template expressions in HTML attribute names when wrapping attributes.
- Preserve indentation after void tags containing markup in quoted attributes.

## [1.40.4] - 2026-07-07

### Fix

- Keep Jinja comments and set tags idempotently indented with `preserve_leading_space`.
- Avoid false H026 reports when `id` appears inside quoted attribute values.
- Avoid false D018/J018 reports for `action` parameters inside quoted template URL helper attributes.
- Report H007 when leading template tags appear before an HTML tag without a preceding doctype.
- Keep `blank_line_after_tag` from inserting blank lines inside multiline HTML attribute values, preserving idempotent reformatting for embedded template tags.
- Report T003 when `{% endblock name %}` does not match its opening `{% block name %}`.
- Report H025 when list tags are nested inside `<p>` tags.

## [1.40.3] - 2026-07-04

### Fix

- Preserve `djlint:off` blocks inside tag attributes and avoid false H025 orphan reports when a matching tag crosses a `djlint:off` block boundary.
- Keep repeated single-line Django `{% if %}` blocks idempotent after one reformat pass.

## [1.40.2] - 2026-07-03

### Fix

- Keep multiline inline-tag indentation when an inline child appears before following text.

## [1.40.1] - 2026-07-01

### Fix

- Preserve full `djlint:off` blocks before formatter passes so ignored template, script, and style content is not rewritten.
- Preserve inline template blocks embedded in rendered text or captured content so formatting does not add meaningful whitespace or misalign following content.
- Keep chained Jinja function calls and lookups intact when formatting template expressions.
- Preserve whitespace-sensitive Django `filter` blocks instead of moving punctuation or translated text around them.
- Keep Jinja/Nunjucks-trimmed `<textarea>` closing tags aligned without reformatting untrimmed textarea contents.

## [1.40.0] - 2026-07-01

### Feature

- Add `single_attribute_per_line` to wrap attributes in a Prettier-like layout using the configured indent.

## [1.39.7] - 2026-06-30

### Fix

- Preserve Jinja template comments inside formatted `<script>` and `<style>` blocks.

## [1.39.6] - 2026-06-30

### Fix

- Avoid false H025 reports for HTML-like strings inside template tags.
- Preserve Jinja template tags inside formatted `<script>` and `<style>` blocks.

### Packaging

- Revise the minimum required dependency versions:
  - click raised from 8.0.1 to 8.2.0
  - cssbeautifier lowered from 1.14.4 to 1.13.0
  - jsbeautifier lowered from 1.14.4 to 1.13.0
  - json5 raised from 0.9.11 to 0.10.0
  - pathspec lowered from 0.12 to 0.9.0
  - pyyaml lowered from 6 to 5.1
  - regex lowered from 2023 to 2021.8.21
  - tomli is lowered from 2.0.1 to 0.2.0

## [1.39.5] - 2026-06-29

### Fix

- Return 1 when no files match the requested lint or format run.
- Make `--check -` return 1 when formatting changes are needed.
- Keep progress output off stdin runs.

### Performance

- Defer runtime-only imports until the CLI code paths that need them.
- Process stdin formatting in memory instead of creating a temporary file.
- Avoid creating an executor when a run only has one worker.

## [1.39.4] - 2026-06-24

### Fix

- Fix crashes in mypyc-compiled wheels.

## [1.39.3] - 2026-06-23

### Fix

- Use Click instead of tqdm for progress output, send progress to stderr, respect `--quiet`, and honor `NO_COLOR`. Remove direct `colorama` and `tqdm` dependencies now that Click handles CLI colors and progress.
- Avoid false H025 reports after self-closing tags in Django templates.
- Avoid false H025 reports for multiline Go template attributes.
- Keep Django child-template reformatting idempotent when inline control blocks also appear inside HTML attributes.
- Respect whitespace-control dashes when applying `blank_line_after_tag` and `blank_line_before_tag`.

## [1.39.2] - 2026-06-11

v1.39.1 was not published due to mypyc compilation error.

### Packaging

- Fix mypyc compilation.

## [1.39.1] - 2026-06-11

### Fix

- Avoid false T027 reports for apostrophes inside quoted template strings.
- Format Alpine.js object methods in attributes when `format_attribute_js_json` is enabled.
- Preserve indentation after inline Jinja control-flow blocks that start with whitespace trim markers, such as `{%- if ... %}...{% endif %}`.
- Preserve safe inner quote style for Jinja function calls inside quoted HTML attributes.

## [1.39.0] - 2026-06-05

### Feature

- Add `preserve_class_newlines` / `--preserve-class-newlines` to keep authored line breaks inside multiline `class` attributes.

### Fix

- Fix Django 6.0 `{% partialdef %}` block indentation so `{% endpartialdef %}` aligns with its opener.
- Preserve multiline Django/Jinja control-flow blocks instead of condensing short bodies onto one line.
- Preserve single-line inline HTML and template tag bodies during expansion, even when they exceed `max_line_length`.

## [1.38.2] - 2026-06-05

### Fix

- Fix `python -m djlint` not working due to mypyc compilation.

## [1.38.1] - 2026-06-04

### Fix

- Match exclude paths on path boundaries.

## [1.38.0] - 2026-06-04

### Feature

- Add support for `.djlint.toml` project and global config files.

### Fix

- Preserve single-line inline HTML tag bodies when they fit within `max_line_length`.
- Avoid evaluating template expressions while formatting tag contents.

### Packaging

- Fix npm publish workflow.

## [1.37.0] - 2026-06-04

### Feature

- Add `--format-attribute-js-json` for formatting JavaScript and JSON inside HTML attributes. It also supports `format_attribute_js_json_pattern` and `format_attribute_js_json_min_props` for tuning which attributes are formatted. Thanks, @oliverhaas.
- Add `--github-output` for GitHub Actions annotations. Thanks, @iloveitaly.

### Fix

- Fix `ignore_blocks` matching when ignored blocks are indented. Thanks, @tdryer.
- Use relative paths for `--exclude` and `--use-gitignore` matching so path filters work consistently from nested directories. Thanks, @satya-waylit.
- Stop D018/J018 from flagging root links such as `href="/"`. Thanks, @SAY-5.
- Do not treat soft hyphen entities as text for H023. Thanks, @kotutuloro.
- Fix Handlebars `{{#unless}}` indentation. Thanks, @S1mplePixels.
- Fix formatting when `/>` appears inside an HTML attribute value. Thanks, @novucs.
- Improve CPU count handling for worker setup.

### Performance

- Improve formatter caching and reduce cache memory usage. Formatting is about 19% faster.

### Documentation

- Add Chinese translation. Thanks, @Twisuki.
- Add Homebrew installation instructions. Thanks, @alfawal.
- Add EFM Neovim integration documentation. Thanks, @danielebra.
- Add copy-pastable pre-commit YAML to the README. Thanks, @Pierre-Sassoulas.
- Polish linter and CLI documentation. Thanks, @jasonaowen and @dotWee.

### Packaging

- Drop Python 3.9 support.

## [1.36.4] - 2024-12-24

- Fix specific mixture of quotes and escaped quotes (e.g. in a json string in an html attribute) breaks the html. Thanks, @oliverhaas.
- Fix broken formatting of template tags inside template tags. Thanks, @oliverhass.

## [1.36.3] - 2024-11-29

This release reverts the following changes from the last release as they caused issues:

- Fix specific mixture of quotes and escaped quotes (e.g. in a json string in an html attribute) breaks the html. Issue #1048.
- Resolve exclude paths. Issue #1047.

## [1.36.2] - 2024-11-28

Fix:

- Fix specific mixture of quotes and escaped quotes (e.g. in a json string in an html attribute) breaks the html. Thanks, @oliverhaas.
- Resolve exclude paths. Thanks, @antoineauger.

Performance:

- Minor regex indent optimization. Thanks, @oliverhaas.

## [1.36.1] - 2024-11-07

- Improve performance by ~30%. Thanks, @oliverhaas.

## [1.36.0] - 2024-11-05

### Feature

- Add support for `djlint.toml` config file. The format is identical to `pyproject.toml`, but it does not use `[tool.djlint]` table.

### Fix

- Do not format HTML in attributes. Thanks, @oliverhaas.
- Fix using `js_config` instead of `css_config`.

### Performance

- Increase performance by ~30% by using regex more efficiently and caching more stuff.

## [1.35.4] - 2024-11-01

Compiled [mypyc](https://mypyc.readthedocs.io/en/stable/introduction.html) wheels are now also available, which improve performance by ~21% over Pure Python. They will be automatically installed by your package manager when available for your platform. Pure Python wheel is still available.

Other changes have been made to improve performance, thanks to @JCWasmx86. See the [commits](https://github.com/djlint/djLint/compare/v1.35.3...v1.35.4) for more details.

Formatting performance comparison with the previous version (tested on <https://github.com/openedx/edx-platform> with single thread):

| Version             | Seconds |
| ------------------- | ------- |
| v1.35.3             | 20.39   |
| v1.35.4 pure Python | 14.39   |
| v1.35.4 compiled    | 11.35   |

## [1.35.3] - 2024-10-30

This release significantly improves performance, especially for large files and large projects.

Formatting <https://github.com/openedx/edx-platform> took 87 seconds in the previous version, now it takes only 4 seconds (>2000% speedup)! Tested on a 32-core computer.

- Performance improved by caching some functions. Thanks to @JCWasmx86!
- Removed the limitation on the number of workers introduced in v1.35.0.
- Drop Python 3.8 support.

## [1.35.2] - 2024-08-29

- Fix npm publishing

## [1.35.1] - 2024-08-29

- Fix npm publishing

## [1.35.0] - 2024-08-29

- Unpin dependencies upper bounds.
- Use min(cpu_count, files_count, 4) workers. Use a thread instead of a process if only one worker will be used. This gives the best performance and low resource usage.
- Refactor the code.
- Fix max attribute length with longer regex custom html tags (#884)
- Fix Jinja formatting issues (#715)
- Fix: not detecting tabs as a valid seperation between tags (#813)
- Fix: Add ignore for sms links (#815)
- Fix: Allow attributes on <title> (#830)
