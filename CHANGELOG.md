# Changelog

[Semantic Versioning](https://semver.org/)

## [Unreleased]

### Feature

- Formatting rewrites a single quoted attribute value to double quotes, which is what `H008` asks for, so `<div class='a'>` becomes `<div class="a">`. Only the names the rule reports are touched, so `data-x='b'` is left as written, and a value holding a double quote of its own keeps the single quotes it needs.
- New option `--keep-br-inline` / `keep_br_inline` keeps `<br>` on the line of the text it breaks instead of giving it a line of its own, which reads better in a long block of prose. `<hr>` is unaffected, and the default is unchanged.
- Formatting drops the `type` that html5 already assumes, so `<script type="text/javascript">` becomes `<script>` and the same for `<style>` and a stylesheet `<link>`. A type that means something, such as `type="module"` or `type="application/json"`, is kept. This is what `H024` asks for.
- Formatting lowercases a form's `method`, so `method="POST"` becomes `method="post"`. `method` is an enumerated attribute, so the page submits the same either way, and this is what `H029` asks for.
- Formatting writes an entity reference as the character it names, so `&copy;` becomes `©` and `&#8364;` becomes `€`, which is what `H023` asks for. The entities that have to survive are untouched: `&lt;`, `&amp;` and the rest carry syntax, and an invisible one such as `&zwnj;` cannot be reviewed as a literal. An entity naming nothing, such as the misspelled `&mdsah;`, is left as written for the rule to go on reporting, and a `<pre>`, `<textarea>`, `<script>` or `<style>` body is left alone. `--no-entity-formatting` turns it off.
- New option `--quote-style` / `quote_style` chooses the quotes djLint writes around strings inside template tags, `double` (the default, and what it has always written) or `single`. `T002` asks for whichever is configured, so `{% include 'a.html' %}` is no longer reported in a project that writes single quotes. Quoting of html attributes is unchanged and stays with `H008`.
- Formatting lowercases an attribute name written in another case, the same eleven names `H010` reports, so `<div CLASS="a">` is fixed rather than only complained about. A name the rule does not know, such as an svg `viewBox` or an angular input, keeps the case it carries, and `--ignore-case` turns the whole thing off as it already does for tag names.
- New rule `H043` reports a `<button>` written without a `type`. A button with no type submits the form around it, so one meant to run a script reloads the page instead, and pressing Enter anywhere in the form triggers it. html-validate ships the same check in its recommended set.
- New rule `H044` reports a header row holding both `th` and `td` cells. A stray cell there is read as data by a screen reader and styled unlike the columns beside it, and the mixture is legal html, so nothing else catches it. Each row is judged on its own and an empty `td` opening the row is skipped, so neither the explanation row the html specification puts in a `thead` nor the corner cell the W3C accessibility tutorial asks for is reported.

### Changed

- `H031` is gone. Google stopped using the keywords meta tag for ranking in 2009 and bing treats it as a spam signal, so a rule asking for one was recommending markup that has no effect.
- `H036` reports only the two uses of `<br>` the html specification rules out: a run of two or more breaks, and a break against the inside edge of a block element. A break that is part of the content, as in the postal address the specification gives as its own conforming example, is left alone, so the rule is on by default now rather than flagging every `<br>`.
- `T002` is on by default, and `--reformat` now writes the quotes it asks for. The formatter rewrites the arguments of `{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}` and `{% now %}` to the `--quote-style` in force, and the rule leaves alone the one string it cannot rewrite, the one already holding the quote it would be rewritten to.
- `H035` is gone. `H017` already covers `meta`, so the two always reported the same tag together and `H035` could never say anything `H017` did not.
- `H023` no longer reports an entity naming a character that is invisible, which its own rationale said it exempted. It flagged `&zwnj;`, `&zwj;`, `&#8203;` and `&hairsp;`, and `&zwnj;` is not optional in persian and arabic text, where the literal cannot be reviewed in a diff. The allow list now covers the entities that carry syntax and the invisible ones alike, in named, decimal and hex form.
- `T028` is off by default. The whitespace its advice strips is whitespace that renders: `alt="{%- if brand -%}Acme{%- endif -%} logo"` renders as `Acmelogo`, and an svg `d="M12 {%- if big -%}20{%- endif -%} 4Z"` becomes a different path. It stays available with `--include=T028`.
- `H014` counts blank lines the way the formatter does. It reported a run of two whatever the settings said, so `--max-blank-lines 2` and `--preserve-blank-lines` both produced files the linter then rejected. A run has to be longer than the configuration keeps now, a line holding only whitespace counts as blank, and the report points at the first blank line rather than at the content line above it.
- `H020` leaves an element whose empty form carries meaning: a blank `<option>` holding a select open, a `<tbody>` a script fills in, a `<canvas>`, `<template>` or `<noscript>`. Its exempt names are anchored too, so `<theadx>` is no longer read as `<thead>`.
- `--ignore-case` reaches the linter. It turned off the formatter's case fixing while `H009` and `H010` went on reporting the case the user had just asked djLint to leave alone.
- `--profile=all` honours every `exclude` list. It is every template language at once, so a rule switched off for one of them was running under it: `T028` fired on django markup and recommended `{%- if -%}`, which django rejects.

### Fix

- `H016` no longer takes an svg `<title>` for the document's own. An svg title names the graphic, so a page whose only title is inside one was treated as having a title. The report now points at the `<html>` tag rather than at the first twenty characters of the document.
- `T001` no longer reads a delimiter written inside a string as the end of the tag, so `{{ x|default('}}') }}` is no longer reported as needing padding.
- `D004`, `J004`, `H011`, `H019`, `H021` and `H022` no longer read markup written inside an attribute value as a tag of its own, so `<p title="<a href='javascript:x()'>">` is left alone.
- `D004`, `H019` and `H021` see an attribute written after a template tag that holds a `>`. The scan stopped at the first bracket, so `<div {% if n > 5 %}id="a"{% endif %} style="color:red">` hid the inline style.
- `H019` and `H021` no longer read a name that merely ends in a known one as that attribute, so `data-href` and `data-style` are left alone.
- `H007` reports a document whose first construct it does not recognise instead of going quiet. An `<?xml ... ?>` declaration, a go or handlebars `{{ ... }}`, or a malformed `<!doctypehtml>` at the top of the file made the whole check fail rather than match, so the documents most likely to be missing a doctype were the ones never looked at.
- `T032` sees a tag that holds a filter, a call or a colon. Its pattern read the regex grouping in its own character class as literal characters, so any tag containing `|`, `(`, `)`, `:`, `?` or `%` before the extra whitespace was skipped, which is most of them. A run of spaces inside a string is still content and is left alone.
- `T040` allows an empty literal that only feeds a filter, since `{% extends ""|default:"base.html" %}` resolves to a name and renders.
- `T038` no longer calls a project's own paired tag an orphan. `{% mytag %}...{% endmytag %}` was reported because the closing side is recognised generically while the opening side is known only from a list, so every custom block looked unmatched. An end tag nothing opened is still reported.
- `T027` no longer reads a closing delimiter written inside a string as the end of the tag, so `{{ x|default('}}') }}` is no longer reported as holding an unclosed string. A string that really does run past the tag is still reported.
- `H037` counts an attribute written without a value, so `<input required required>` is reported as the duplicate it is.
- `H012` sees an attribute written after a `{{ ... }}` in the same tag. The scan stopped on the second brace, so `<div {{ attrs }} class = "x">` hid the spaced `=`.
- `H042` leaves a partial that holds a label but no form control alone. The control belongs to the template that includes it, so there was nothing in the file to match against. A control that is commented out still counts, so the label above it is checked.
- `H009` reports exactly the elements the formatter lowercases, so `--reformat` always clears it. It named `G`, `PATH`, `NAME` and `CACHE`, which the formatter does not know, so those were reported and never fixed, while `<IMG>`, `<INPUT>` and `<NAV>` were fixed and never reported. An uppercase name written inside an attribute value, as in `<p title="x <DIV y">`, is no longer read as a tag.
- `H005` reports `<html lang="">`, which names no language and is the case the rule exists for. Its message now says a non-empty `lang`, which is what it has always meant.
- `H013` accepts a valueless `alt`. `<img src="a.png" alt>` is the same as `alt=""`, the decorative image the rule already allowed.
- `T034` no longer reads a `}%` written inside a string as the typo it looks for, so `{% trans "Save 50}% today" %}` is left alone.
- A rule that looks for a tag no longer reads markup written inside an attribute value as a tag of its own. `<p title="a<br>b">` was reported by `H036` and `H017`, `<div title="<button>x</button>">` by `H043`, and `<p title="an <img src=x>">` by `H013`. Affects `H006`, `H013`, `H017`, `H018`, `H020`, `H036` and `H043`.
- `H029` no longer reads a name that merely ends in `method` as the form's own, so `<form data-method="POST">` is not reported. The formatter's rewrite already had that boundary, so the rule was asking for something `--reformat` would not do.
- `H044` no longer reports a header row whose cells sit in sibling branches of a template block. Only one of `{% if x %}<th>A</th>{% else %}<td>A</td>{% endif %}` is ever rendered, so there is no mixture.
- The linter reads the opening tag of a `<script>`, `<style>`, `<pre>` or `<textarea>` again. It was skipping the whole element, so no rule could see those tags: `H024` could never report the `type="text/javascript"` it exists for, `D004` was blind to the `<script src>` its own pattern names, and `H008`, `H010`, `H011`, `H012` and `H037` ignored the attributes on all four. Only the body is skipped now, and a body is no longer read as markup at all, so an apostrophe in a `//` comment or a `<div>` in a javascript string cannot derail the rules that pair tags.
- `H025` no longer calls a tag an orphan in a handlebars or go template. It read `{% %}` branches only, so a wrapper opened in one branch of `{{#if}}...{{else}}...{{/if}}` or `{{if}}...{{else}}...{{end}}` and closed in the other was reported, the same shape it has always accepted in django and jinja.
- `T039` no longer reports a valid block tag that holds a nested mapping. Braces are counted now, so the `}}` closing `{% set a = {"x": {"y": 1}} %}` ends the literal rather than the tag. `--reformat` writes exactly that shape by dropping the space, so formatting a file could turn a clean run into a failing one.
- `H016` no longer reports a document that has a `<title>`. It accepted a title only when its attributes came from a hardcoded list and were double quoted, so `<title id='page-title'>` or an htmx `<title hx-swap-oob="true">` read as no title at all.
- `H008` leaves a single quoted value that holds a double quote, such as `title='{% translate "Delete" %}'`. Obeying the rule there means escaping the inner quotes, which is worse than the markup it complained about. A name that merely ends in a known one, as in `data-title`, is no longer read as that attribute either.
- `H022` no longer reads an `http://` written inside another attribute's value as a link, and no longer reports a loopback or private host: `localhost`, `127.0.0.1`, `192.168.x`, `10.x` and a `.local` or `.test` name are not external links.
- `H024` covers `<link rel="stylesheet" type="text/css">`, the commonest place the attribute is still written, and no longer reads `data-type=` as `type=`.
- `D018` and `J018` no longer report a link that already does what they ask. `<a href="{% url 'profile' %}" data-src="lazy">` was reported because a `data-src` holding any single word counted as a hardcoded path, and `<form action=" {% url 'search' %}">` because the padding was read as part of the value. A value has to look like a path now, and a `/static/` or `/media/` asset is left to `{% static %}` rather than reported as a route.
- `H033` sees a form whose earlier attribute holds a `>`, as in `<form x-show="count > 0" action=" /x/">`. The scan could not step over a quoted value, so it stopped at the first bracket.
- `H043` steps over a template block, so `<button {% if n > 5 %}type="button"{% endif %}>` is no longer reported as having no type.
- `H030` stays quiet for a base layout that fills its description in per page. It looked for a literal `<meta name="description">` and nothing else, so a head using `{% block meta %}` or `{% include "_seo.html" %}` was reported, and the only way to satisfy it was to hardcode one description for the whole site.
- `H005` and `H007` no longer report a custom element whose name merely starts with `html`, such as `<html-midi-player>`.
- `djlint - --reformat --lint` no longer writes its report into the file. The findings and `Linted 1 file, found 1 error.` went to stdout after the formatted code, and an editor piping a buffer through djLint writes stdout back to the file. The lint report, the `--statistics` block and the `--github-output` annotations now go to stderr when stdout is carrying the file. A lint-only run is unchanged.
- `--github-output` defaults to `$GITHUB_ACTIONS`, so this reached CI with no flag typed: `cat f.html | djlint - --reformat > f.html` wrote `::warning` lines into `f.html`.
- Markup written as text inside a `<script>`, `<style>` or `<textarea>` is no longer rewritten. `var s = "<DIV CLASS=x>"` came back as `"<div CLASS=x>"`, changing what the script produced and what the textarea showed.
- An attribute value written without quotes is now quoted, which is what `H011` asks for. Quoting used to happen only when the tag was long enough to be spread over several lines, so `class=one` kept its shape or became `class="one"` depending on how much else was in the tag. A value carrying a quote of its own, as in `a=b'c`, is still left alone.
- Line endings survive `djlint -`. A CRLF buffer piped to `--reformat` came back LF throughout, while the same file reformatted in place kept it, so formatting on save rewrote every line. Input that `--require-pragma` skips is now handed back byte for byte, line endings included.
- Line endings are no longer guessed with `str.splitlines()`, which also breaks on U+2028, U+2029, U+0085, form feed and vertical tab. One of those inside a `<script>` string was rewritten as a newline, breaking the script.
- A `djlint:off` block written between the attributes of a tag no longer crashes the formatter when it contains a backslash, and its text is put back as written instead of being read as a regex replacement.
- A `wrap_line_length` in the `css` or `js` settings no longer drops the tail of a `<style>` or `<script>` body. The block is laid out at two indent levels to find the lines the beautifier owns, and a width that wraps differently at the two left the extra lines with nothing to pair against.
- A file reached through more than one of the given paths, such as `djlint . templates/`, is now checked once instead of once per path. It was reported twice, counted twice, and with `--reformat` written by two workers at the same time.
- A trailing or empty entry in `custom_blocks`, `ignore_blocks`, `custom_html`, `blank_line_after_tag` or `blank_line_before_tag`, as in `ignore_blocks = "raw,"`, is now dropped. It used to build a pattern that matched everywhere: `ignore_blocks` silently turned off all template indentation, and the `blank_line_*` options padded every template tag in the file.
- A `.gitignore` is read only when `--use-gitignore` or `use_gitignore` asks for it. pathspec rejects patterns git accepts and ignores, such as one ending in a backslash, so a single line in it aborted every run in that project with a traceback and an invitation to report a bug.
- Text inside `<pre>` and `<textarea>` that looks like a djLint marker no longer ends the verbatim block. `&lt;!-- x -->`, `-->` and `{# djlint:on #}` shown as sample code let the formatter indent the rest of the block, adding a level on every run, so repeated runs walked the contents further and further right.
- Formatting repeatedly with `--preserve-leading-space` no longer walks a line further right on every run. A line the formatter indented kept its own leading space too, so a multi-line `{# ... #}` comment, the closing brace of a multi-line `{% set ... %}` and every other line inside an indented block gained one indent level per run, without bound.
- With `--preserve-leading-space`, the contents of a `{{ if }}` or `{{ range }}` block lost an indent level when an already formatted go template was formatted again. The block tag keeps its own indent under that option, and the patterns that recognise it are anchored to the start of the line.
- `--single-attribute-per-line` no longer flips a tag between one line and many on alternate runs. Spreading a tag rewrites `href = "..."` as `href="..."`, which measured short enough to be put back on one line, and long enough to be spread again on the run after that.
- `--blank-line-before-tag` no longer splits a line to place its blank line. A tag written after other content on the same line, such as the `{% block %}` inside a one line `{% set %}...{% endset %}`, was moved to a line of its own, which broke up a block whose body is captured verbatim and left the file formatting differently on the next run.
- `--blank-line-before-tag` no longer inserts a blank line into an attribute value, which added one more line on every run. `--blank-line-after-tag` already left attributes alone.
- `--format-css` and `--format-js` no longer add a blank line before the closing `</style>` or `</script>` tag on every run.
- A template block opened and closed on one line, such as `{% language 'de' %}text{% endlanguage %}`, no longer indents everything after it. Only `if`, `for`, `unless`, `block`, `with` and the two nunjucks async tags were recognised as balanced on a single line.
- Arguments spread over their own lines inside `{{ }}` stay where they are. The first was pulled up against the opening bracket while the rest kept their lines.
- A filter written straight after a function call keeps its place: `{{ _("test")|upper }}` is no longer respaced to `{{ _("test") |upper }}`.
- `{{#if}}` and other handlebars sections are no longer read as the start of a Jinja `{#` comment, which made everything up to the next `#}` count as a comment and left it unformatted.
- Jinja's `+` whitespace control marker is now read wherever `-` is. `{%+ if x %}` was not recognised as a block tag and `{%+ endif %}` not as an end tag, so `T038` reported a balanced block as unmatched and let an unbalanced one through, `{% endblock body +%}` was read as naming a block `body +`, and the formatter left these blocks unindented.
- `T038` no longer reports a balanced `{% if %}` or `{% for %}` in a file that opens with `---` and has another `---` line inside the block. The second `---` was read as the end of yaml front matter, putting the opening tag in a region the linter skips while its end tag stayed outside. Front matter is now only the block a file opens with, closed by a `---` alone on its line, and holding no `{% %}` tag.
- `H025` no longer calls a tag an orphan when a `{% for %}...{% else %}...{% endfor %}` is written inside the `{% else %}` of an `{% if %}`. The loop's else was taken for a branch of the enclosing conditional.
- On free-threaded Python, `--format-css` and `--format-js` no longer share the beautifier indent level between the threads formatting different files, which could indent a `<style>` or `<script>` body by the wrong amount.
- Console output is utf-8 on stderr as well as on stdout. A warning could reach a Windows console as `\U0001f622` rather than an emoji, and a template's own text quoted in a lint message came out in the console codepage.
- Input on stdin that is not valid utf-8 is reported as bad input rather than as a djLint failure.
- A closed pipe, as in `djlint . | head -1`, is no longer a djLint failure. It printed a traceback and exited `120`.
- `--statistics` now prints its summary alongside GitHub annotations. It was silently dropped whenever the GitHub output was on, which happens by itself inside a workflow.
- Formatting a file twice gives the same file when a `<script>` or `<style>` is followed by text. The closing tag was left glued to whatever came next on the first run and broken onto its own line on the second. Text that really does sit against the element, as in `a<script>x</script>b`, is still left alone, because a line break there renders as a space.
- A `{%` written inside javascript is no longer read as a template tag. A `<script>` holding `'{%'` and `'%}'` in its code stopped the whole line it was on from being formatted, so the markup around it kept whatever layout it arrived with.
- A tag is measured as it will be written when deciding whether to spread its attributes over several lines. Extra spaces between attributes counted towards the length, so `<input id="a"  type="checkbox">` was spread, measured short enough to be joined again, and spread once more on the next run.
- A `{%` that opens nothing no longer hides the markup after it. A page quoting template syntax in prose, as in `<code>{%-</code>`, or holding a typo such as `{% x }%`, went unformatted from there to the next `%}` anywhere below, because everything between was read as one template tag. An opener written directly against a `<` or `>`, and one followed by a second opener before any closing delimiter, are text now.
- `--preserve-leading-space` no longer keeps a blank line on one run and drops it on the next. Whitespace is trimmed in two passes under that option, and the second pass was still deciding what counts as a verbatim block from the positions the first pass had shifted, so a `<pre>` or `<textarea>` written with leading indentation moved every decision after it out of place. `--blank-line-after-tag` had the same drift from the second tag in its list onwards.
- A template block opened and closed on one line no longer indents everything after it. `{% if a %}y{% endif %}<p>` left the `{% if %}` counted as open, so the first closing tag below it restored the indent to that phantom block's level and the rest of the file sat one level too deep until the next run pulled it back.
- An element opened on the same line as a `<script>`, `<style>` or `<pre>` keeps its indent. Everything before the block's opening tag went uncounted, so the children of `<a class="x">text<style>` sat outside it, and a closing tag written after such a block's end tag now gives back the level it took.
- `--preserve-leading-space` no longer moves a line back and forth on every run. A line opening with text and holding a short element, such as `&amp;<small> text </small>`, was recognised as one only while it sat at the left margin, so each run indented it and the next pulled it back, and `--check` never came out clean.

### Performance

- Linting a large file is many times faster. The pattern that finds `djlint:off` blocks opened with a bare `|`, so its first alternative was empty and it matched at every offset in the file: a 120KB page produced 129,326 spans, and every tag the linter looked at was checked against all of them. That page went from 13 seconds to 0.15, and a 1.7MB run of 60 files from 28 seconds to 1.6.
- Deciding whether a finding sits in an ignored block no longer walks every ignored span. The spans are merged and sorted once per file and looked up by bisection, which cut the linter's own time on a 25KB template by close to half.
- Linting a file with many findings is several times faster: locating a match's line no longer scans the file, and de-duplicating findings no longer compares every pair.
- Reformatting is around 15% faster: patterns built from the configuration are compiled once instead of on every tag, and each line is tokenized once instead of up to three times.

### Docs

- The `H026` page no longer claims nothing can target an empty `class` or `id`. A class or id selector does not match one, but an attribute presence selector such as `div[class]` does, so removing the attribute is visible to a stylesheet written that way.
- The GitHub Actions integration is documented: djLint reports findings as annotations on a pull request's diff by itself, and `--github-output` / `--no-github-output` override that.
- The command line reference lists `--allow-empty-input`, which it had been missing, and a test now keeps it in step with `djlint --help`.
- `H042` is no longer described as off by default, which it stopped being in 1.42.1.

### Tests

- Formatting a file twice now has to give the same result as formatting it once, checked across the option combinations that reach the whitespace passes.

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
