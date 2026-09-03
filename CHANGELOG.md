# Changelog

[Semantic Versioning](https://semver.org/)

## [Unreleased]

## [1.45.0] - 2026-09-03

### Feature

- New rule `H043` reports a `<button>` written without a `type`. A type written inside a template block, as in `<button {% if a %}type="button"{% endif %}>`, counts.
- New rule `H044` reports a header row holding both `th` and `td` cells. The empty `td` that opens a two-axis table's header row is allowed.
- New rule `H045` reports an `<iframe>` with no accessible name. `title`, `aria-label` and `aria-labelledby` all count, as does a name written by a template tag.
- New rule `H046` reports a positive `tabindex`. `0` and `-1` are left alone, as is a value written by a template tag.
- New rule `H047` reports `aria-hidden="true"` on an element that takes focus. Hiding a decorative icon is not reported, nor is a `disabled` control or one with `tabindex="-1"`.
- New rule `H048` reports an `aria-` attribute that ARIA does not define, such as a misspelled `aria-lable`. Framework bindings like `:aria-label` are left alone.
- New rule `H049` reports a viewport that stops the page being zoomed, by `user-scalable=no` or a `maximum-scale` below 2.
- New rule `H050` reports an element html no longer defines, such as `<center>`, `<font>`, `<marquee>` or `<strike>`. Only the opening tag is reported, and a custom element whose name merely starts with one, such as `<font-picker>`, is left alone.
- New rule `H051` reports a `role` ARIA does not define for markup, such as `role="buton"`. The roles DPUB-ARIA and GRAPHICS-ARIA add count, abstract ones such as `landmark` do not, and a value written by a template tag or a framework binding such as `:role` is left alone.
- New rule `H052` reports a `<meta http-equiv="refresh">` that reloads or redirects on a timer, which fails WCAG 2.2.1. A delay of zero is an immediate redirect rather than a timer and is not reported.
- New option `--quote-style` / `quote_style` sets the quotes djLint writes inside template tags, `double` (the default) or `single`, and `T002` follows it, so `{% include 'a.html' %}` is no longer reported in a project that writes single quotes. Html attributes stay with `H008`.
- New option `--sort-attributes` / `sort_attributes` orders a tag's attributes by name, with `id` first and `class` second. A tag whose attributes are guarded by a template tag, as in `<div {% if x %}a="1"{% endif %} b="2">`, keeps the order it was written in.
- New option `--name-endblocks` / `name_endblocks` writes the block's name into the `{% endblock %}` that closes it, where the block spans several lines, making `T003` fixable by running the formatter. A block opened and closed on one line is left alone.
- New option `--no-indent-inner-html` / `no_indent_inner_html` leaves `<head>` and `<body>` at the same indent as the `<html>` that holds them, matching the default VS Code html formatter.
- New option `--keep-br-inline` / `keep_br_inline` keeps `<br>` on the line of the text it breaks instead of giving it a line of its own. `<hr>` is unaffected, and the default is unchanged.
- New option `--prefer-configuration` lets the file named by `--configuration` override the project's own `pyproject.toml` or `.djlintrc`, which have always won where the two set the same thing. The default is unchanged.
- Single quoted attribute values are rewritten to double quotes, as `H008` asks, so `<div class='a'>` becomes `<div class="a">`. Only the names the rule reports are touched, and a value holding a double quote of its own keeps its single quotes.
- Attribute names that `H010` reports are lowercased by the formatter, so `<div CLASS="a">` is fixed rather than only reported. A name the rule does not know, such as an svg `viewBox`, keeps its case, and `--ignore-case` turns it off.
- Formatting writes an entity reference as the character it names, so `&copy;` becomes `©`, which is what `H023` asks for. Entities that carry syntax or template meaning are left as written, as are `<pre>`, `<textarea>`, `<script>` and `<style>` bodies, and `--no-entity-formatting` turns it off.
- The `type` that html5 already assumes is dropped, as `H024` asks, so `<script type="text/javascript">` becomes `<script>`, and the same for `<style>` and a stylesheet `<link>`. A type that means something, such as `type="module"`, is kept.
- A form's `method` is lowercased, so `method="POST"` becomes `method="post"`, which is what `H029` asks for. A tag written inside a template tag's string is left alone.

### Changed

- `H031` is gone: the keywords meta tag it asked for no longer affects ranking, and bing treats it as a spam signal.
- `H035` is gone; `H017` already covers `meta`.
- `H036` reports only two uses of `<br>`: a run of two or more, and a break against the inside edge of a block element. Breaks that are part of the content, such as in a postal address, are left alone, and the rule is on by default.
- `T002` is on by default, and `--reformat` now writes the quotes it asks for, rewriting tag arguments and conditions such as `{% if x == 'a' %}` to the `--quote-style` in force. A string already holding the quote it would be rewritten to is left alone.
- `T028` is off by default: the whitespace it strips can be whitespace that renders, so `alt="{%- if brand -%}Acme{%- endif -%} logo"` comes out as `Acmelogo`. It stays available with `--include=T028`.
- `H014` counts blank lines the way the formatter does, so `--max-blank-lines 2` and `--preserve-blank-lines` no longer produce files the linter then rejects. A line holding only whitespace counts as blank, and the report points at the first blank line rather than the content line above it.
- `H020` leaves alone an element whose empty form carries meaning, such as a blank `<option>` holding a select open.
- `H023` no longer reports an entity for an invisible character, such as `&zwnj;`, in named, decimal or hex form.
- `--ignore-case` applies to the linter as well as the formatter, so `H009` and `H010` stay quiet when it is set.
- `--profile=all` honours every profile's `exclude` list, so `T028` no longer fires on django markup to recommend `{%- if -%}`, which django rejects.
- A GitHub annotation names the column as well as the line, so it lands on the tag rather than the start of the line.

### Fix

- Markup inside an attribute value is no longer read as a tag, so `<p title="a<br>b">` is not reported: affects `D004`, `J004`, `H006`, `H011`, `H013`, `H017`, `H018`, `H019`, `H020`, `H021`, `H022`, `H036` and `H043`.
- `D004`, `H019` and `H021` see attributes written after a template tag containing a `>`, so the inline style in `<div {% if n > 5 %}id="a"{% endif %} style="color:red">` is checked.
- Rules check the opening tag of `<script>`, `<style>`, `<pre>` and `<textarea>`, which used to be skipped along with the body, so `H024`, `D004`, `H008`, `H010`, `H011`, `H012` and `H037` can see their attributes. Only the body is skipped now, and its contents are never read as markup.
- `D018` and `J018` no longer report a link that already uses a url tag, such as `<a href="{% url 'profile' %}" data-src="lazy">`; a value now has to look like a path. `/static/` and `/media/` assets are left to `{% static %}` rather than reported as routes.
- `H005` reports `<html lang="">`, and its message asks for a non-empty `lang`.
- `H005` and `H007` ignore custom elements whose name starts with `html`, such as `<html-midi-player>`.
- `H007` reports a missing doctype in a file that opens with something it does not recognise, such as an `<?xml ... ?>` declaration.
- `H008` leaves single quoted values holding a double quote alone, such as `title='{% translate "Delete" %}'`. An attribute that merely ends in a known name, such as `data-title`, is no longer treated as that attribute.
- `H009` reports exactly the elements the formatter lowercases, so `--reformat` always clears it: `<IMG>`, `<INPUT>` and `<NAV>` are now reported, and `G`, `PATH`, `NAME` and `CACHE` are not. An uppercase name inside an attribute value, as in `<p title="x <DIV y">`, is no longer read as a tag.
- `H012` sees attributes written after a `{{ ... }}` in the same tag, so the spaced `=` in `<div {{ attrs }} class = "x">` is reported.
- `H013` accepts a valueless `alt`, so `<img src="a.png" alt>` passes as the decorative image `alt=""` already did.
- `H016` recognises a `<title>` however it is written, so `<title id='page-title'>` no longer reads as a missing title and an svg `<title>` no longer counts as the document's. The report points at the `<html>` tag.
- `H022` no longer reads an `http://` inside another attribute's value as a link, and no longer reports loopback or private hosts: `localhost`, `127.0.0.1`, `192.168.x`, `10.x` and `.local` or `.test` names.
- `H024` covers `<link rel="stylesheet" type="text/css">`.
- `H025` no longer calls a tag an orphan in a handlebars or go template: a wrapper opened in one branch of `{{#if}}...{{else}}...{{/if}}` and closed in the other is accepted, as in django and jinja.
- `H029` reads only the form's own `method` attribute, so `<form data-method="POST">` is not reported.
- `H030` stays quiet for a base layout that fills its description in per page, so a head using `{% block meta %}` is no longer reported.
- `H033` sees a form whose earlier attribute holds a `>`, as in `<form x-show="count > 0" action=" /x/">`.
- `H037` counts an attribute written without a value, so `<input required required>` is reported as the duplicate it is.
- `H042` leaves a label alone in a partial that holds no form control. A control that is commented out still counts, so the label above it is checked.
- `T001` and `T027` no longer read a delimiter inside a string as the end of the tag, so `{{ x|default('}}') }}` is reported neither as needing padding nor as holding an unclosed string. A string that really does run past the tag is still reported.
- `T032` flags extra whitespace in tags that hold a `|`, `(`, `)`, `:`, `?` or `%`, which were previously skipped. A run of spaces inside a string is still content and is left alone.
- `T034` no longer flags a `}%` written inside a string, so `{% trans "Save 50}% today" %}` is left alone.
- `T039` no longer reports a valid block tag holding a nested mapping such as `{% set a = {"x": {"y": 1}} %}`, a shape `--reformat` itself produces.
- `T040` allows an empty literal that only feeds a filter, as in `{% extends ""|default:"base.html" %}`.
- Markup written as text inside `<script>`, `<style>` or `<textarea>` is left alone; `var s = "<DIV CLASS=x>"` is no longer rewritten to `"<div CLASS=x>"`.
- An attribute value written without quotes is now quoted, as `H011` asks, so `class=one` becomes `class="one"`. A value carrying a quote of its own, such as `a=b'c`, is still left alone.
- Strings inside a `{% set %}` or a function call keep their own quotes when they hold the other kind, so `{% set s = 'say "hi"' %}` is left as written instead of escaped.
- Arguments spread over their own lines inside `{{ }}` stay where they are; the first is no longer pulled up against the opening bracket.
- Spacing is no longer added before a filter that follows a function call: `{{ _("test")|upper }}` keeps its shape.
- Handlebars sections such as `{{#if}}` are no longer taken for the start of a Jinja comment, which left everything up to the next `#}` unformatted.
- Jinja's `+` whitespace control marker is read wherever `-` is, so `{%+ if x %}` counts as a block tag, `T038` no longer misreports these blocks and the formatter indents them.
- A `{%` that opens nothing no longer hides the markup after it: a page quoting template syntax in prose, as in `<code>{%-</code>`, is formatted rather than skipped down to the next `%}`.
- `{%` written inside javascript is no longer read as a template tag; a `<script>` holding `'{%'` and `'%}'` in its code used to leave its whole line unformatted.
- A template block opened and closed on one line no longer indents everything after it, and tags beyond the built in set, such as `{% language 'de' %}text{% endlanguage %}`, are recognised as balanced on a line too.
- Extra spaces between attributes no longer count towards a tag's length: `<input id="a"  type="checkbox">` used to flip between spread and joined on every run.
- Formatting a file twice gives the same result when a `<script>` or `<style>` is followed by text. Text sitting directly against the element, as in `a<script>x</script>b`, is still left alone, since a line break there would render as a space.
- Indentation is kept for an element opened on the same line as a `<script>`, `<style>` or `<pre>`, so the children of `<a class="x">text<style>` now sit inside it, and a closing tag written after the block's end tag gives back the level it took.
- A `<pre>`, `<textarea>`, `<script>` or `<style>` opened and closed on one line no longer cancels a block opened earlier: `<pre>x</pre><script>` left the script's body indented as markup, and took a second run to settle.
- Text inside `<pre>` and `<textarea>` that looks like a djLint marker, such as `{# djlint:on #}` shown as sample code, no longer ends the verbatim block and walks its contents a level further right on every run.
- Repeated formatting with `--preserve-leading-space` no longer moves a line further right on every run, as it did for a multi-line `{# ... #}` comment and every other line inside an indented block.
- `--preserve-leading-space` no longer keeps a blank line on one run and drops it on the next when a `<pre>` or `<textarea>` is written with leading indentation; `--blank-line-after-tag` had the same drift from the second tag in its list onwards.
- With `--preserve-leading-space`, the contents of a `{{ if }}` or `{{ range }}` block no longer lose an indent level when an already formatted go template is formatted again.
- `--blank-line-before-tag` no longer splits a line to place its blank line, so a tag written after other content, such as the `{% block %}` inside a one line `{% set %}...{% endset %}`, stays where it is.
- `--blank-line-before-tag` no longer inserts a blank line into an attribute value, which grew the file on every run. `--blank-line-after-tag` already left attributes alone.
- A `djlint:off` block placed between a tag's attributes no longer crashes the formatter when it contains a backslash, and its text comes back exactly as written.
- On free-threaded Python, `--format-css` and `--format-js` no longer indent a `<style>` or `<script>` body by the wrong amount when several files are formatted at once.
- `djlint - --reformat --lint` no longer writes its report into the file: the lint findings, the `--statistics` block and the `--github-output` annotations go to stderr when stdout is carrying the formatted code. A lint-only run is unchanged.
- `--github-output` annotations no longer land in the file either: in CI, where the flag turns itself on from `$GITHUB_ACTIONS`, `cat f.html | djlint - --reformat > f.html` wrote `::warning` lines into `f.html`.
- `--statistics` prints its summary alongside GitHub annotations. It was dropped whenever the GitHub output was on, which happens by itself in a workflow.
- Line endings survive `djlint -`: a CRLF buffer piped to `--reformat` came back LF throughout. Input that `--require-pragma` skips is handed back byte for byte.
- U+2028, U+2029, U+0085, form feed and vertical tab are no longer treated as line breaks; one inside a `<script>` string was rewritten as a newline and broke the script.
- Console output is utf-8 on stdout and stderr alike, so a warning no longer reaches a Windows console as `\U0001f622` rather than an emoji.
- Input on stdin that is not valid utf-8 is reported as bad input rather than as a djLint failure.
- A closed pipe, as in `djlint . | head -1`, is no longer a failure: it printed a traceback and exited `120`.
- A file reached through more than one of the given paths, as in `djlint . templates/`, is checked once, so it is no longer reported and counted twice or written twice under `--reformat`.
- A trailing or empty entry in `custom_blocks`, `ignore_blocks`, `custom_html`, `blank_line_after_tag` or `blank_line_before_tag`, as in `ignore_blocks = "raw,"`, is ignored instead of turning off template indentation altogether or padding every template tag in the file.
- `.gitignore` is read only when `--use-gitignore` or `use_gitignore` asks for it, so a line djLint cannot parse, such as one ending in a backslash, no longer aborts every run in the project with a traceback.
- `--require-pragma` skips a file whose first line it cannot decode instead of aborting the whole run. A file that is checked and turns out undecodable is still reported as a failure.
- `--indent-js` and `--indent-css` override the indent alone, leaving other beautifier settings in the config file's `js` or `css` block, such as `wrap_line_length`, in place.
- `--ignore` and `--include` accept a space after the comma, so `--ignore "H011, H013"` no longer reports `H013`.

### Performance

- Linting a large file is many times faster: a 120KB page went from 13 seconds to 0.15, and a 1.7MB run of 60 files from 28 seconds to 1.6. Linting a file with many findings is several times faster too.
- Formatting is about a quarter faster, for around a tenth of a megabyte more memory: 575 templates from a large Django project took 2.6 seconds of processor time under 1.44.2 and take 1.9 now.

### Docs

- The `H026` page no longer claims an empty `class` or `id` cannot be targeted: an attribute presence selector such as `div[class]` does match one, so removing the attribute can change how a page is styled.
- The GitHub Actions integration is documented: djLint annotates a pull request's diff with findings by itself, and `--github-output` / `--no-github-output` override that.
- `--allow-empty-input` appears in the command line reference, which had been missing it.
- `H042` is no longer documented as off by default, which it stopped being in 1.42.1.
- The before-and-after example on the formatter page has been corrected: it showed a template tag with single quotes, which the formatter rewrites now that `T002` is on by default.
- Code samples on the site are highlighted in full again, after attribute names, punctuation and other tokens had lost their colours.
- The playground tells a browser without web workers that it needs one, instead of failing first.

## [1.44.2] - 2026-08-08

### Fix

- `H037` no longer reports two attributes whose names differ only before a `.` as duplicates (`data-a.checked` and `data-b.checked`, or alpine's `x-on:click.prevent` and `x-on:keyup.prevent`).
- An attribute whose name merely ends in the name a rule looks for is no longer mistaken for it. `data-alt` and `data-x.alt` left `H013` silent on an image with no `alt`, `data-lang` and `xml:lang` silenced `H005`, `data-height` and `data-width` silenced `H006`, `data-name="description"` silenced `H030` and `data-name="keywords"` silenced `H031`, and `data-x.id` satisfied a `<label for>` for `H042`.
- A name written inside an attribute value is no longer read as an attribute. `title="alt=x"` left `H013` silent, `class="language-en"` silenced `H005`, and `title="the ID=5"` was reported by `H010` as an uppercase attribute name.
- `H005` no longer reports a tag whose name only starts with `html`, such as `<htmlx>`, and points at the `<html>` tag itself rather than at everything up to the last `>` in the file.

## [1.44.1] - 2026-08-07

### Fix

- Formatting no longer changes what the page renders. A space that shows was dropped (`<span>a</span><span> b </span>` rendered as `ab`, `a{% if x %} b {% endif %}c` as `abc`), a space that shows nothing was added (`<span>     </span>` became `<span> </span>`), and moving a tag onto its own line could add one (`x<img>y`, or across a comment as in `a{# c #}<img>`). Whitespace is now kept where it renders and dropped where it does not.
- A line break inside an attribute value is kept, so a `title` tooltip no longer loses a line and a `data-` value read by script no longer comes back different. Line breaks in `class`, `style`, `srcset` and `sizes` mean nothing and are still joined.
- Indentation inside `<pre>` and `<textarea>` is left alone when the closing tag has something after it on its line (`<pre>  a\n  b</pre> tail`).
- Whitespace css does not collapse, such as U+2005, is text, and is no longer stripped from the edges of an element or of the file.
- Two indenting fixes: a line that closes one tag and opens another (`</b><i>`) indents its contents again, and a line that closes more tags than it opens unindents even when a whole tag ends it (`</b><small></small>`). Both left the lines after them at the wrong level.
- `--line-break-after-multiline-tag` now applies only to tags actually written over several lines, as its help says. It was holding back the content of every element, splitting tags that fit on one line.
- A `class` value is tidied wherever it was written: `class=" a  b "` becomes `class="a b"`. A tag whose attribute value holds a line break is spread over lines, since it cannot fit on one.

## [1.44.0] - 2026-08-04

### Feature

- New `--allow-empty-input` option, and the matching `allow_empty_input` config key, exits `0` instead of `2` when the given paths match no files.

### Fix

- An html close tag inside an inline `{% if %}...{% endif %}` no longer dedents everything that follows it by one level, collapsing nested structures toward column 0 - a regression in 1.43.0. A close tag already at the content level of the template block it sits in is held there, but the level it was denied was then taken off the end of the line instead, so `{% if r %}</strong>{% endif %}` moved the rest of the block left. The matching open tag never took a level to give back, since `{% endif %}` had already returned it.
- A run where every file found was skipped by `exclude`, `extend_exclude`, `use_gitignore` or `require_pragma` now exits `0` instead of `1`. Skipping them is the configuration doing its job, and it is what lets `exclude` work under pre-commit, which passes the names of every staged file. Paths that match no files at all now exit `2` rather than `1`, so exit `1` means only that djLint found something to report.
- An unhandled error exits `2` instead of `1`, so a crash is no longer indistinguishable from a lint error. The traceback is still printed.
- An unrecognized `--profile`, or `profile` in a config file, is now a usage error. A typo used to lint with a silently different rule set and exit `0`, and raised `KeyError` with `--require-pragma`.
- A directory whose name matches the file extension (`build.html/`) is no longer picked up as a template and opened as a file, crashing the run.
- `No files to check!` is written to stderr instead of stdout, where formatted code is written.
- Input piped to `djlint - --reformat` that `--require-pragma` skips is handed back byte for byte instead of being replaced by `No files to check!`.

## [1.43.2] - 2026-08-01

### Fix

- `blank_line_before_tag` no longer inserts a blank line when the previous line opens a block and increases the indentation, e.g. between `<div>` and `{% block %}`. Since 1.41.0 `blank_line_after_tag` has left the closing edge of a block alone (`{% endblock %}` before `</div>`), while the opening edge kept its padding, so a template using both options came out lopsided.

## [1.43.1] - 2026-07-28

### Fix

- `H025` no longer reports the closing tag of a multi-line `<script>` or `<style>` as an orphan - a regression in 1.43.0. A genuinely unmatched `</script>` is still reported.

## [1.43.0] - 2026-07-27

### Feature

- New `--stdin-filename` option gives content piped in on stdin (`djlint -`) its real path, so `per-file-ignores` matches against that name and linter messages report it. Per-file ignores were previously dead for piped input, since nothing matches the name `-`. Path separators are normalized as they are for files on disk.

### Fix

- An apostrophe inside a template tag nested in an attribute value (`title="{% translate "You don't have permission" %}"`) no longer swallows the rest of the document, which made `H025` report every enclosing element as an orphan. A template tag in a value is now skipped whole unless it holds a `>`, so a quoted literal like `a="{{"` is still left alone.
- A line that starts with a closing tag and ends with a whole tag (`</span>tail<textarea>y</textarea>`) unindents again; everything after it stayed one level too deep.
- A template block tag followed by a whole html tag on the same line (`{% endif %} <td class="x">y</td>`) indents as a block tag again, so `{% endif %}` unindents and `{% else %}` aligns with its `{% if %}`. A line only takes that shape once the tag fits on one line, so reformatting an already formatted file moved it.
- A tag opened after the end of a verbatim block on the same line (`</pre> <span>x`) is tracked again; its closing tag took a level from a tag opened before the block, dedenting that tag's siblings.
- A template control block written across lines is kept that way when it opens against a tag (`<div>{% if x %}`), and the choice is no longer applied to the wrong block. Blocks were paired with the source by position, which does not line up with the expanded html; they are now matched by tag and contents.
- A tag whose `style`, `srcset`, `data-srcset` or `sizes` value was written over several lines is no longer spread over multiple lines and pulled back together on the next run. `max_attribute_length` is now measured against what is written out, not against padding that the rewrite drops.
- A `<pre>` or `<textarea>` opened on a line that also holds a self-contained comment (`<pre>x<!--c-->`) is recognized as opening a verbatim block again. Its contents were re-indented instead of left alone, and the closing `</pre>` gained an indent level on every run - unbounded whitespace growth inside preformatted text.
- A closing tag that starts its line no longer dedents when the tag it closes was opened after text on an earlier line (`text <b>bold` / `</b> tail`). The loss accumulated, so a document repeating that shape drifted further left with each occurrence. A closing tag with nothing to pair against still dedents as before.
- A `<` inside a one-line `<script>`, `<style>`, `<textarea>` or `<title>` no longer counts as a tag when indenting. `<script>var a = '<span>'</script>` left a phantom open `<span>` on the tag stack, leaving everything after it one level too deep.
- An inline element that opens after text on its line and closes on a later line no longer dedents everything that follows it by one level (`text <b>bold` / `more</b> tail` inside a `<p>`) - a regression in 1.40.8. The wrong output was idempotent, so it survived later runs.
- A Go template comment `{{/* ... */}}` is no longer read as a block close tag. It starts with `{{/`, the handlebars block-close prefix, so it popped a block off the stack: `H037` reported `Duplicate attribute found.` for mutually exclusive attributes such as `<a {{if .A}}href="a"{{else}}{{/* c */}}href="b"{{end}}>`, and the formatter unindented the rest of the block. A comment renders as nothing, so `H037` no longer treats one as a template-generated attribute name prefix either.
- A tag that merely touches an ignored block is no longer treated as being inside it. A tag ending exactly where an ignored block starts - such as `{% if x %}{# comment #}` - was skipped by the linter, most visibly making `T038` report `End tag has no matching block tag` for a balanced `{% if %}`. Affects every rule that skips ignored blocks (`H025`, `H037`, `H041`, `H042`, `T002`, `T003`, `T027`, `T038`, `T039`) and every kind of ignored block.
- A bare `djlint:off` pragma no longer ignores the tag written immediately before it. `<img>{# djlint:off #}` silently dropped every error on that `<img>`, while `<img>{# djlint:off H013 #}` correctly reported it - a pragma covers what follows it, not what precedes it.

## [1.42.3] - 2026-07-23

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
