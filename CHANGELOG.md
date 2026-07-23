# Changelog

[Semantic Versioning](https://semver.org/)

## [Unreleased]

### Fix

- Attribute names containing punctuation beyond `-`, `.`, `:`, `@` and `*` no longer stop a tag from being wrapped over multiple lines. The attribute parser now accepts any character HTML allows in an attribute name, so Alpine key modifiers (`@keydown.prevent.?`), Angular bindings (`(click)`, `[disabled]`) and Vue shorthands (`#slot`) are formatted like every other attribute instead of leaving the whole tag on one long line. Angular bindings also reach `--format-attribute-js-json` for the first time, which already listed them.
- An unquoted attribute value with a template tag glued to the rest of the value (e.g. `src={{ MEDIA_URL }}/logo.png`, `href={{ .Permalink }}#{{ .Anchor }}`) is no longer split into a truncated value plus a bogus standalone attribute when attributes are wrapped; it stays one value, quoted when spread.

## [1.42.2] - 2026-07-22

### Fix

- Attributes containing `${...}` inside a quoted value (e.g. JS template literals like ``:name="`x[${i}]`"``) respect `max_attribute_length` again and are spread over multiple lines - a regression in 1.40.6. Unquoted Mako-style `${...}` expressions in tags are still left unformatted.
- A stray `<!--` that is not a real HTML comment (for example inside a `{# ... #}` template comment or inside a `<textarea>`/`<pre>`) no longer swallows the rest of the document. This fixes false `H025` orphan-tag reports and over-indentation of the tags that follow - a regression in 1.40.6.
- Handlebars triple-stache `{{{ ... }}}` and raw-block `{{{{ ... }}}}` expressions used as tag attributes are tokenized correctly again, fixing false `H025` orphan-tag reports - a regression in 1.40.6.
- A quoted literal brace in an attribute value (e.g. `data-x="{{"`) no longer makes the tokenizer scan into later content looking for a matching `}}`, which could collapse `<pre>`/`<textarea>` whitespace - a regression in 1.40.6.
- Spacing the `}}` of a handlebars `{{#if}}`/`{{#each}}` block-open tag is now idempotent; it no longer leaks a trailing space into the following `{{...}}` tag on later formatting passes.
- `T038` no longer reports block tags that appear only inside a handlebars comment (`{{!-- ... --}}`, `{{! ... }}`) or inside a handlebars raw block (`{{{{raw}}}} ... {{{{/raw}}}}`).
- `T039` no longer reports handlebars raw-block delimiters (`{{{{raw}}}}` / `{{{{/raw}}}}`) as unclosed template tags.
- Malformed tag attributes that the attribute parser cannot fully parse (e.g. a stray `<` or dangling `=`) are now left untouched instead of having the unparsable characters silently dropped when attributes are wrapped.
- A `<` used as a less-than operator inside a template expression in text or `<script>` content (e.g. `${a<b}`, `{{a<b}}`) is no longer mistaken for an HTML tag start, which could merge or drop following content and break idempotency - a regression in 1.40.6.
- Unquoted attribute values containing `:` or `/` (e.g. `href=https://example.com/page`) are no longer split into a truncated value plus a bogus standalone attribute when attributes are wrapped - a regression in 1.40.6.
- A nameless `="value"` attribute is no longer rewritten with the literal attribute name `None`; malformed attributes are left untouched.
- Trailing whitespace inside an indented `<textarea>`/`<pre>` is preserved instead of being collapsed by whitespace cleanup (it is verbatim content).

### Performance

- Detecting ignored/verbatim blocks (`{% comment %}`, `{% blocktrans %}`, `{% filter %}`, `<pre>`, `<script>`, etc.) is dramatically faster on templates with many `{% ... %}` tags. A lazy `[ ]*?` before the block keywords caused pathological backtracking; the equivalent greedy `[ ]*` removes it, cutting reformat time on large template-heavy files by roughly 5x.

## [1.42.1] - 2026-07-20

### Fix

- H017 and H018 no longer style `command`, `keygen` and `menuitem` - elements that were removed from the HTML standard.
- Enabling H018 together with H017 or H035 now prints a warning when linting - they enforce opposite void tag conventions, so only one should be on.

### Changed

Linter rule defaults were reviewed against a simple bar: on by default means correctness, security, clear accessibility, or a consistency check the formatter also enforces - with near-zero false positives. Four rules moved to opt-in (`--include=...`):

- T003 (endblock names): neither Django nor Jinja requires a name on `{% endblock %}`; the name demand is a style preference. The correctness checks T003 used to bundle - unclosed `{% block %}`, orphan `{% endblock %}` and mismatched endblock names, all hard template errors - moved into T038, which stays on by default, so nothing real is lost when T003 is off.
- T002 (double quotes in tags): engines accept both quote styles, no autofix exists, and quote-style rules are the canonical example of style checks that don't belong in a default tier.
- H006 (img width/height): valuable performance advice (browsers map the attributes to a default `aspect-ratio`, preventing layout shift) but performance rather than correctness, and the dimensions are frequently unknowable in a template - user uploads, CMS urls, art-directed `<picture>` sources - so the rule demands data the author may not have.
- H031 (meta keywords): major search engines have ignored keyword metadata for over a decade; recommending that it be added is outdated advice. The niche intranet-indexer use case keeps the rule available via `--include=H031`.
- H042 (label/for) moved the other way - from opt-in to on by default - after its false-positive class was removed: the rule now checks a file only when nothing in it could render an id invisibly. Any `{{ ... }}` output (form widgets), `{% include %}`/`{% extends %}` or unrecognized template tag silences the rule for that file, so where it does run, every report is a genuinely broken label association (a WCAG 1.3.1/4.1.2 failure the W3C validator also treats as an error).

## [1.42.0] - 2026-07-20

### Feature

Template languages:

- New `askama` profile for [Askama](https://askama.readthedocs.io/) (jinja-style templates in Rust). Rust expressions are never reformatted: function and `{% set %}`/`{% let %}` formatting are disabled so `some_macro!("foo")?`, char literals `'a'` and tuples keep their exact spelling, and string quotes are never rewritten. The Flask-specific `url_for` rules (J004/J018) don't apply.
- New `tera` profile for [Tera](https://keats.github.io/tera/) (Rust, used by Zola): jinja-style formatting plus Tera v2 `{% component %}`/`{% endcomponent %}` blocks and single-tag `{% set_global %}`. The Flask-specific `url_for` rules don't apply. MiniJinja needs no profile of its own - it is fully Jinja2-compatible, use `--profile=jinja`.
- New `liquid` profile for [Liquid](https://shopify.github.io/liquid/) (Shopify themes, Jekyll, Eleventy, the Rust `liquid` crate). `{% case %}`/`{% when %}`, `{% capture %}`, `{% tablerow %}`, `{% form %}`, `{% paginate %}`, `{% highlight %}` and `{% unless %}`/`{% elsif %}` indent correctly, `{%- -%}` whitespace control is handled, and the bodies of Shopify section tags (`{% schema %}`, `{% style %}`, `{% javascript %}`, `{% stylesheet %}`) are left untouched - they contain JSON, CSS or JS rather than html.
- The `golang` profile now indents template blocks: `{{ if }}`, `{{ range }}`, `{{ with }}`, `{{ block }}` and `{{ define }}` indent their contents up to the matching `{{ end }}`, with `{{ else }}`/`{{ else if }}` as branches and the `{{- -}}` whitespace-control forms included. Blocks opened and closed on one line are left alone; single tags like `{{ template }}` and lookalike variables such as `{{ .end }}` are unaffected.

New linter rules:

- T040: `{% extends %}` or `{% include %}` with a missing or empty template name - an error the engine only raises at render time, so the typo is easy to ship.
- H041: an html tag opened in one `{% block %}` and closed in a different one. The pair looks balanced in the file, but a child template overriding either block renders unbalanced html.
- H018 (off by default, enable with `--include=H018`): void tags closed with `/>` instead of `>`, e.g. `<br/>` - the trailing slash has no effect in HTML. The opposite convention of the optional H017 ("void tags should be self closing"); enable one or the other, not both.
- H042 (off by default, enable with `--include=H042`): a `<label for="...">` whose value matches no element `id` in the same file. Template-generated values are skipped; the rule is opt-in because inputs rendered by e.g. `{{ form.email }}` carry ids the linter cannot see.

Configuration:

- `indent` and `max_line_length` now fall back to `indent_size` and `max_line_length` from a `.editorconfig` at the project root. The command line and djlint config files still take precedence, and only sections applying to html (or the configured `extension`) are read.

Documentation:

- Every linter rule now has a detailed entry on the linter page - what it checks, why it matters, and a verified Don't/Do example pair - in English, French, Russian and Chinese. Askama, Tera and Liquid get language pages, logos and homepage cards, and engines covered by existing profiles (MiniJinja, Jinjava, Pebble, the Liquid dialects) are noted on the pages of the profiles that cover them.

### Fix

- H017 no longer misfires on tags that merely start with a void tag name: `<cola>` (matched by a broken `colgroup` exclusion) and custom elements like `<img-icon>` are no longer reported. `<meta>` tags, missing from the rule's void tag list, are now reported.

## [1.41.0] - 2026-07-19

### Feature

- New rule T038: block template tags with no matching end tag are now reported: `{% if %}` without `{% endif %}`, handlebars `{{#if}}` without `{{/if}}`, end tags with no opening tag, and crossed blocks like `{% if %}{% for %}{% endif %}`. Tags from `custom_blocks` are checked too; `{% block %}`/`{% endblock %}` pairs stay covered by T003.
- New rule T039: template tags that never reach their closing delimiter are now reported, e.g. `{% url 'x" user.url }}` (closed by `}}` instead of `%}`), `{{ user.name }` (missing a brace), or a tag cut off by the next tag or the end of the file. Complements T027 (unclosed string in a complete tag) and T034 (`}%` typo), which keep reporting their own cases.
- New `--rules FILE` CLI option: load a custom rules file in `.djlint_rules.yaml` format from any path, instead of only next to `pyproject.toml`.

### Changed

- The formatter now condenses runs of extra whitespace inside single-line template tags to a single space, e.g. `{% if   abc == 101 %}` becomes `{% if abc == 101 %}`. This fixes what rule T032 reports, so the linter and formatter no longer conflict. Whitespace inside string literals is preserved, including strings with backslash-escaped quotes; multiline tags, ignored blocks, the literal contents of `{% verbatim %}`/`{% raw %}` and the handlebars/golang profiles are untouched.
- The default `exclude` list is now tailored to djLint instead of copying ruff/black. Added directories that hold generated or third-party HTML: `htmlcov` (coverage.py reports), `site-packages` (installed packages' templates such as Django admin and DRF, matched in any virtualenv layout) and `_site` (Jekyll/Eleventy output). Removed Python tool caches and editor config that never contain HTML: `.ipynb_checkpoints`, `.mypy_cache`, `.pytest_cache`, `.pytype`, `.ruff_cache`, `.pants.d`, `.vscode` and `buck-out`.

### Fix

Formatter indentation:

- Closing a template block now restores the indentation of its opening tag, so HTML tags left unclosed inside the block (e.g. a wrapper `<div>` rendered by `{% if %}...{% endif %}` and closed by a later conditional) no longer shift the indentation of everything after it. When every branch of an `{% if %}/{% elif %}/{% else %}` shifts the depth equally, e.g. a `<tr>` opened in both branches, the shift is kept after `{% endif %}`.
- Template tags and expressions spanning multiple lines keep the relative indentation of their contents instead of flattening every line to the tag's level. Nested objects and arrays in e.g. `{% story ... with { ... } %}`, `{% include ... with { ... } %}` and non-JSON `{{ func(...) }}` calls are now indented by bracket depth.
- `{% endtrans %}` (Jinja/Twig block `{% trans %}`) no longer decreases the indentation level, which shifted the `{% endtrans %}` line and everything after it one level to the left.
- Multiline `{% set %}` objects nested inside HTML elements are no longer over-indented in proportion to their nesting depth.
- Self-closing custom block tags (django-components syntax, e.g. `{% component "calendar" date="2015-06-19" / %}` with `custom_blocks = "component"`) no longer indent the lines that follow them as if a block had been opened.

Formatter line breaks and spacing:

- A single-line block-form `{% set x %}...{% endset %}` is no longer expanded onto multiple lines. The block captures its content verbatim, so the added whitespace changed the value of the variable. Authored multi-line set blocks are still indented as before.
- In multi-line `{{ ... }}` function calls, a call passed as an argument no longer causes a stray space before the following comma, and the arguments after it keep the same indentation as the other arguments.
- `blank_line_after_tag` no longer inserts a blank line when the next line closes a block and decreases the indentation, e.g. between `{% endblock %}` and `</div>`.
- `blank_line_before_tag` now inserts the blank line above a comment directly preceding the tag, keeping the comment attached to the tag it documents.

Linter:

- H020 no longer reports `<slot></slot>`: an empty slot element is the standard way to declare a default slot outlet.
- H025 no longer reports a tag as an orphan when the same tag is opened in each branch of an `{% if %}/{% else %}` and closed once outside it (and vice versa for close tags), since only one branch renders.
- H025 now reports mis-nested tags whose close tag crosses another open tag, e.g. `<b>` in `<h1>blah <b>bold</h1>`.
- T003 no longer requires an endblock name when `{% endblock %}` is on the same line as its `{% block ... %}`, e.g. `{% block title %}{% endblock %}`. The formatter keeps such blocks on one line, so the linter and formatter no longer conflict.
- Linter rules no longer report errors for the literal contents of `{% verbatim %}`...`{% endverbatim %}` blocks, matching the existing treatment of jinja `{% raw %}` blocks.

Configuration:

- Comma-separated options in config files (`ignore`, `include`, `custom_blocks`, `custom_html`, `exclude`, `extend_exclude`, `ignore_blocks`, `blank_line_after_tag`, `blank_line_before_tag`) can now also be given as lists, e.g. `ignore = ["H017", "H031"]` in `pyproject.toml`; previously list values were silently ignored.
- `--max-blank-lines` given on the command line is no longer overridden by the config file, matching all other options.

## [1.40.10] - 2026-07-19

### Fix

- Fix crashes in mypyc-compiled wheels: `AttributeError: attribute 'reformat' of 'Config' objects is not writable` when linting or formatting multiple files, and `AttributeError: attribute 'start' of 'TagToken' objects is not writable` when processing a file.

## [1.40.9] - 2026-07-18

### Fix

- Indent content inside Django `{% cache %}`, `{% timezone %}`, `{% localtime %}` and `{% localize %}` blocks instead of dedenting everything after them.
- Format django-cotton component tags such as `<c-card>` and `<c-forms.input />` as block HTML tags without requiring `custom_html` configuration.
- Preserve whitespace-only content of inline elements as a single space instead of dropping it, so runs like `<b>bold</b><span> </span><i>italic</i>` keep rendering a space; non-collapsible whitespace such as U+2005 is kept verbatim.
- Preserve line breaks inside hyperscript `_` attribute values, where a newline separates commands and `--` comments run to the end of the line.
- Stop inserting line breaks into attribute values that render whitespace verbatim; only `class` and `style` values are spread over multiple lines with `format_attribute_template_tags`.
- Leave `{% comment %}` block content untouched when reformatting, e.g. bare URLs ending in `/>`.
- Apply rule-specific `djlint:off RULE` suppression to any finding overlapping the region, so reformatted guards keep linting clean.
- Avoid false H037 reports for attribute names with a conditional template prefix, e.g. `{% if x %}data-{% endif %}srcset`.
- Avoid false reports for HTML-like content inside template tag arguments, e.g. H008 on quotes in a string argument.

## [1.40.8] - 2026-07-17

### Fix

- Preserve conditional attribute names and significant whitespace in template-generated attributes.
- Keep parent closing tags aligned after multiline inline content.
- Avoid false H026 reports when `id` or `class` is followed by a spaced equals sign.
- Keep short tag contents inline when attributes contain template expressions.
- Avoid false D018/J018 reports for links using valid URI schemes.
- Indent content inside Twig `embed` blocks.
- Avoid false H037 reports for attributes in mutually exclusive template branches.
- Respect `exclude` and `extend_exclude` for explicitly provided files.
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
