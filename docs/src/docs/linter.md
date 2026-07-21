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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>

## Enabling or Disabling Rules

Most rules are enabled by default. Rules can be disabled in the command line with the `--ignore` flag. Rules can be enabled with the `--include` flag.

For example:

```bash
djlint . --lint --include=H017,H035 --ignore=H013,H015
```

This can also be done through the [{{ "configuration" | i18n }}]({{ "lang_code_url" | i18n }}/docs/configuration) file.

## Rules

| Code | Meaning                                                                                      | Default |
| ---- | -------------------------------------------------------------------------------------------- | ------- |
| D004 | (Django) Static urls should follow {% raw %}`{% static path/to/file %}`{% endraw %} pattern. | ✔️      |
| D018 | (Django) Internal links should use the {% raw %}`{% url ... %}`{% endraw %} pattern.         | ✔️      |
| H005 | Html tag should have `lang` attribute.                                                       | ✔️      |
| H006 | `img` tag should have `height` and `width` attributes.                                       | -       |
| H007 | `<!DOCTYPE ... >` should be present before the html tag.                                     | ✔️      |
| H008 | Attributes should be double quoted.                                                          | ✔️      |
| H009 | Tag names should be lowercase.                                                               | ✔️      |
| H010 | Attribute names should be lowercase.                                                         | ✔️      |
| H011 | Attribute values should be quoted.                                                           | ✔️      |
| H012 | There should be no spaces around attribute `=`.                                              | ✔️      |
| H013 | `img` tag should have alt attributes.                                                        | ✔️      |
| H014 | More than 2 blank lines.                                                                     | ✔️      |
| H015 | Follow `h` tags with a line break.                                                           | ✔️      |
| H016 | Missing `title` tag in html.                                                                 | ✔️      |
| H017 | Void tags should be self closing (conflicts with: H018).                                     | -       |
| H018 | Void tags are self closing by nature and must end with ">", not "/>" (conflicts with: H017). | -       |
| H019 | Replace `javascript:abc()` with `on_` event and real url.                                    | ✔️      |
| H020 | Empty tag pair found. Consider removing.                                                     | ✔️      |
| H021 | Inline styles should be avoided.                                                             | ✔️      |
| H022 | Use HTTPS for external links.                                                                | ✔️      |
| H023 | Do not use entity references.                                                                | ✔️      |
| H024 | Omit type on scripts and styles.                                                             | ✔️      |
| H025 | Tag seems to be an orphan.                                                                   | ✔️      |
| H026 | Empty id and class tags can be removed.                                                      | ✔️      |
| H029 | Consider using lowercase form method values.                                                 | ✔️      |
| H030 | Consider adding a meta description.                                                          | ✔️      |
| H031 | Consider adding meta keywords.                                                               | -       |
| H033 | Extra whitespace found in form action.                                                       | ✔️      |
| J004 | (Jinja) Static urls should follow {% raw %}`{{ url_for('static'..) }}`{% endraw %} pattern.  | ✔️      |
| J018 | (Jinja) Internal links should use the {% raw %}`{% url ... %}`{% endraw %} pattern.          | ✔️      |
| T001 | Variables should be wrapped in whitespace. Ex: {% raw %}`{{ this }}`{% endraw %}             | ✔️      |
| T002 | Double quotes should be used in tags. Ex {% raw %}`{% extends "this.html" %}`{% endraw %}    | -       |
| T003 | Endblock should have name. Ex: {% raw %}`{% endblock body %}`{% endraw %}.                   | -       |
| T027 | Unclosed string found in template syntax.                                                    | ✔️      |
| T028 | Consider using spaceless tags inside attribute values. {% raw %}`{%- if/for -%}`{% endraw %} | ✔️      |
| T032 | Extra whitespace found in template tags.                                                     | ✔️      |
| T034 | Did you intend to use {% raw %}{% ... %} instead of {% ... }%? {% endraw %}                  | ✔️      |
| H035 | Meta tags should be self closing.                                                            | -       |
| H036 | Avoid use of `br` tags.                                                                      | -       |
| H037 | Duplicate attribute found.                                                                   | ✔️      |
| T038 | Block tag has no matching end tag.                                                           | ✔️      |
| T039 | Unclosed template tag found.                                                                 | ✔️      |
| T040 | Missing or empty template name in extends or include tag.                                    | ✔️      |
| H041 | Tag is closed in a different template block than it was opened.                              | ✔️      |
| H042 | Label for attribute has no matching element id in this file.                                 | ✔️      |

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

### Rule Details

<!-- prettier-ignore-start -->
<!-- the examples below are verified against djlint itself; prettier's html style would change what they demonstrate -->

{% raw %}

#### T001

`Variables should be wrapped in a whitespace.`

Template syntax like `{{user.name}}` without inner padding is harder to scan and diff, and inconsistent spacing across a codebase makes grep-based refactors (searching for a variable or tag) unreliable because the same expression exists in multiple spellings. Both Django and Jinja style guides write `{{ var }}` and `{% tag %}` with single spaces.

Not applied to the handlebars and golang profiles.

Don't:

```html
{{user.name}}
```

Do:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Off by default; enable with `--include=T002`.

Mixing single and double quotes in template tags (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) makes the same template name appear in two spellings, so searches and bulk renames miss half the occurrences. Standardizing on double quotes keeps tag arguments consistent with HTML attribute quoting in the rest of the file.

Single quotes inside HTML attribute values (e.g. `<span title="{% trans 'x' %}">`) are not flagged, since the attribute's double quotes force single quotes there.

Don't:

```html
{% extends 'base.html' %}
```

Do:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

When a `{% block %}` spans many lines or blocks are nested, a bare `{% endblock %}` gives no clue which block it closes, so it is easy to end the wrong one while editing; child templates then override the wrong content. Naming the endblock documents the pairing and lets both djLint and Django (which raises TemplateSyntaxError on a mismatched endblock name) catch a block closed in the wrong place. Pairing errors (unclosed blocks, orphan endblocks and mismatched names) are correctness checks handled by T038.

Off by default; enable with `--include=T003`.

A name is not required when the block opens and closes on the same line, e.g. `{% block title %}``{% endblock %}`.

Don't:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Do:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Hardcoding /static/ paths bypasses Django's `{% static %}` tag, so templates break when STATIC_URL changes (e.g. moving assets to a CDN or a subpath deployment) and never pick up hashed filenames from ManifestStaticFilesStorage, causing 404s or stale cached assets in production.

Don't:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Do:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Hardcoding /static/ paths bypasses Flask/Jinja's url_for('static', ...), so assets 404 when the app is mounted under a URL prefix or the static folder/host is changed, and cache-busting query strings added by the framework are lost.

Don't:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Do:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have lang attribute.`

Without a lang attribute on `<html>`, screen readers guess the pronunciation rules and may read the page in the wrong language, and browsers cannot correctly offer translation, hyphenation, or locale-aware quotation marks. Declaring the page language is WCAG 2.1 success criterion 3.1.1 (Level A).

Don't:

```html
<!DOCTYPE html>
<html>
</html>
```

Do:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Off by default; enable with `--include=H006`.

When an `<img>` has no width and height, the browser cannot reserve space before the image downloads, so surrounding content jumps as images load. This layout shift degrades Cumulative Layout Shift (a Core Web Vitals metric) and can make users mis-click while the page settles.

Don't:

```html
<img src="cat.png" alt="Cat">
```

Do:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Without a `<!DOCTYPE>` before the `<html>` tag, browsers render the page in quirks mode, emulating legacy box-model and layout behavior, so CSS renders inconsistently across browsers. Template tags and comments before the doctype are fine; only the `<html>` tag itself must be preceded by it.

Don't:

```html
<html lang="en">
</html>
```

Do:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Mixed quote styles make attribute values harder to scan and grep for, and single-quoted values break as soon as the content contains an apostrophe. Double quotes are the convention used by HTML specs, formatters, and most style guides, so standardizing on them keeps templates consistent with the wider ecosystem.

Don't:

```html
<div class='content'></div>
```

Do:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

HTML parsers accept uppercase tag names, but XHTML and XML serializations are case-sensitive and reject them, and mixed casing makes text search and diff review unreliable (grepping for `<h1>` misses `<H1>`). Lowercase tag names keep templates portable and consistent.

Don't:

```html
<H1>Welcome</H1>
```

Do:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Uppercase attribute names are invalid in XHTML/XML serializations and defeat text search across templates (grepping for src= misses SRC=). The DOM normalizes HTML attribute names to lowercase anyway, so uppercase spellings add inconsistency with no benefit.

Don't:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Do:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Unquoted attribute values end at the first whitespace, so a value like class=btn primary silently drops everything after the space (the browser treats "primary" as a separate boolean attribute). Values that come from template variables are especially fragile: any rendered space, "=", or ">" corrupts the tag. Quoting makes the value boundary explicit and safe.

Don't:

```html
<div class=test></div>
```

Do:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

With spaces around "=", the tag reads as three separate tokens, and it is one edit away from breaking apart: a line wrap or truncation in the middle leaves a bare boolean attribute plus stray text. Keeping name="value" contiguous is also what simple text tooling (grep, search-and-replace) assumes, so mixed spacing makes attributes hard to find and refactor reliably.

Don't:

```html
<div class = "test"></div>
```

Do:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Without an alt attribute, screen readers announce the image's file name or nothing at all, failing WCAG 1.1.1 (Non-text Content). The alt text is also what users see when the image fails to load. Decorative images should carry an explicit empty alt="" so assistive technology knows to skip them; that also satisfies this rule.

Don't:

```html
<img src="cat.jpg" height="200" width="300">
```

Do:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Runs of blank lines have no effect on the rendered page (HTML collapses whitespace) but bloat templates and create noisy diffs when neighboring lines change. djLint's formatter removes them entirely by default (keeping at most `max_blank_lines` blank lines, which defaults to 0), so leftover runs indicate unformatted code.

Don't:

```html
<div>one</div>


<p>two</p>
```

Do:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Headings are block-level landmarks that define the document outline; cramming the next element onto the same line as the closing h tag hides that structure in the source and makes edits to either element show up as changes to both in diffs. A line break after each heading keeps the template's visual structure aligned with the rendered outline.

Don't:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Do:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

The HTML spec requires a title element in every document. Without one, browser tabs, bookmarks, and history show a raw URL instead of a page name, search engines lose the primary label for the page, and screen-reader users lose the first thing announced on load, failing WCAG 2.4.2 (Page Titled, Level A).

Only fires on files containing a complete `<html>`...`</html>` document, so partials and child templates that extend a base are never flagged. SPA shells that set the title client-side still need a static `<title>`: it is what appears on first paint, in crawlers, and when JavaScript fails.

Don't:

```html
<html lang="en">
<body>Content</body>
</html>
```

Do:

```html
<html lang="en">
<head>
<title>My page</title>
</head>
<body>Content</body>
</html>
```

#### H017

`Void tags should be self closing.`

Templates that must also parse as XML/XHTML (or feed XML-based tooling) reject void elements written without a closing slash, and mixing `<br>` with `<br />` across a codebase produces inconsistent diffs. This rule enforces the XHTML-style convention so every void element is closed the same way.

Off by default; enable with `--include=H017`. Mutually exclusive with H018; enable only one of the two conventions.

Don't:

```html
<br>
<meta charset="utf-8">
```

Do:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Hardcoded internal URLs silently go stale when a route's path changes in urls.py, producing broken links and dead form actions that no test on the URLconf will catch. `{% url %}` resolves the path from the route name, so renaming a path updates every link at once.

Don't:

```html
<a href="/accounts/login">Login</a>
```

Do:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

In the HTML living standard the trailing slash on a void element has no meaning (the parser ignores it), so writing `<br />` implies XML-style self-closing behavior HTML does not have and can mislead readers into adding slashes to non-void tags, where a stray / is silently dropped and masks unclosed-tag bugs. This rule enforces plain > endings on void elements.

Off by default; enable with `--include=H018`. Mutually exclusive with H017; enable only one of the two conventions. SVG `<path />` is exempt, since SVG is XML and requires the slash.

Don't:

```html
<br />
<meta charset="utf-8" />
```

Do:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Hardcoded internal URLs break silently when a route's path changes or the app is mounted under a prefix, leaving dead links and form actions posting to 404s. url_for() builds the URL from the endpoint name, so route changes propagate to every template automatically.

Don't:

```html
<a href="/accounts/login">Login</a>
```

Do:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

javascript: URLs break middle-click and open-in-new-tab, do nothing when JavaScript is disabled or fails to load, are blocked by strict Content Security Policies, and are a classic XSS injection sink. Use a real URL for the href and attach the behavior with an event handler instead. Under a strict CSP, inline on* handlers are blocked as well: the onclick shown is the minimal in-template fix; prefer attaching the listener with addEventListener from a script file.

Don't:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Do:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

An empty tag pair renders no content but still creates a DOM node that can pick up margins, borders, or flex/grid gaps from stylesheets, producing phantom spacing that is hard to trace; it is usually leftover markup from an earlier edit. Tags that are legitimately empty in normal markup (td, th, li, dt, dd, slot) are exempt. Tags carrying any attribute (JS mount points like `<div id="app">``</div>`, icon-font elements like `<i class="fa fa-user">``</i>`) are not flagged either; only fully attribute-less empty pairs match.

Don't:

```html
<p>Saved.</p>
<span> </span>
```

Do:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Inline styles carry higher specificity than any stylesheet selector, so overriding them later requires !important; they are blocked by Content Security Policies without 'unsafe-inline' in style-src; and they scatter presentation across templates, so a theme or design change means editing markup instead of one stylesheet. Move the declaration to a CSS class. One legitimate exception: HTML email templates, where many email clients strip `<style>` blocks and inline styles are the standard technique; exclude your email template directories or disable this rule for them.

Don't:

```html
<div style="color: red;">Wrong username or password.</div>
```

Do:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Plain http:// subresources on a page served over HTTPS are mixed content: browsers block scripts, stylesheets, and iframes outright and auto-upgrade or warn on images. An `<a>` link to an http:// page is not mixed content, but it still sends visitors over an unencrypted connection open to interception and tampering. References to internal hosts that genuinely have no TLS will be flagged too; silence those spots with a `{# djlint:off H022 #}` block rather than disabling the rule.

Don't:

```html
<a href="http://example.com">Example</a>
```

Do:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

HTML5 documents are UTF-8, so the literal character works everywhere and is what reviewers actually read; a typo in an entity reference (e.g. `&mdsah;`) is not caught by the browser and renders verbatim as broken text. djLint allows only the entities that carry syntactic meaning or are invisible on screen, such as `&lt;`, `&gt;`, `&amp;`, `&quot;`, `&nbsp;` and `&shy;`.

Don't:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Do:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript and text/css are the HTML5 defaults for `<script>` and `<style>`, so the attribute is dead weight the browser ignores; the WHATWG spec explicitly says to omit it. Dropping it also avoids stale MIME strings that break the element when copied onto module scripts (where type="module" actually matters).

Don't:

```html
<script type="text/javascript" src="app.js">
```

Do:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

A tag without its matching opening or closing tag forces the browser's error recovery to guess where the element ends, so following markup gets swallowed into the wrong element; layout, CSS selectors, and JavaScript DOM queries then break silently and differently across browsers. H025 also reports an `<ol>` or `<ul>` opened inside a `<p>`: the HTML parser closes the paragraph before the list, so the markup never nests the way it is written.

Don't:

```html
<div>
  <p>Hello</p>
```

Do:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

An empty id or class attribute does nothing (no styles or scripts can target it), and an empty id is invalid HTML (the id value must not be the empty string). It usually signals a template bug where a variable was meant to be interpolated, so removing or filling it keeps that bug from hiding in plain sight.

Don't:

```html
<div id="" class="">content</div>
```

Do:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

A quote that is opened but never closed inside `{% ... %}` or `{{ ... }}` makes the template engine mis-parse the tag: Django and Jinja either raise a TemplateSyntaxError at render time or silently swallow the rest of the tag's arguments as string content, so the page 500s or renders with missing arguments.

Don't:

```html
{% trans "Welcome %}
```

Do:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Template tags inside an attribute value emit the whitespace and newlines around them into the rendered attribute, so an href or src built with plain `{% if %}`/`{% for %}` tags can contain stray spaces and produce broken URLs. Jinja/Nunjucks whitespace-control tags (`{%- ... -%}`) strip that surrounding whitespace so the attribute renders as one clean value. The class attribute is exempt, since extra whitespace between class names is harmless.

Not applied to the django profile: Django template tags do not support `{%- -%}` whitespace control.

Don't:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Do:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

The HTML spec defines the form method keywords as lowercase (get, post); browsers only accept uppercase variants through case-insensitive fallback matching. Keeping the canonical lowercase form makes templates consistent and greppable and avoids complaints from strict validators and XHTML-based toolchains.

Don't:

```html
<form method="POST"></form>
```

Do:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Search engines use the meta description as the snippet under your page title in results; without one they synthesize a snippet from arbitrary page text, which hurts click-through rates and produces poor link previews when the page is shared.

Only fires on files containing a complete `<html>`...`</html>` document. The snippet argument applies to publicly indexed pages; for auth-gated or intranet apps this rule is commonly disabled.

Don't:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Do:

```html
<html lang="en">
  <head>
    <title>Home</title>
    <meta name="description" content="A short summary of this page.">
  </head>
  <body>Welcome</body>
</html>
```

#### H031

`Consider adding meta keywords.`

Off by default; enable with `--include=H031`.

Keyword metadata is still consumed by some site-search tools, intranet indexers, and older crawlers, so a page that never declares `<meta name="keywords">` can be invisible to those systems. Major public search engines ignore it, though, so teams that don't rely on such tooling commonly disable this rule.

Only fires on files containing a complete `<html>...</html>` document.

Don't:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<title>Home</title>
<meta name="description" content="A short summary.">
</head>
</html>
```

Do:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<title>Home</title>
<meta name="description" content="A short summary.">
<meta name="keywords" content="django, templates">
</head>
</html>
```

#### T032

`Extra whitespace found in template tags.`

Runs of spaces or tabs between the arguments of a template tag are invisible noise: they hide real differences in diffs, can make it hard to spot a missing argument, and drift from the single-space style djLint's formatter produces, causing needless reformat churn. Whitespace inside quoted strings is preserved and not flagged.

Don't:

```html
{% static  'css/style.css' %}
```

Do:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Leading or trailing whitespace inside a form's action value becomes part of the rendered URL. Browsers strip it when parsing, but non-browser clients and tests hitting the literal value may not, and around a `{% url %}` tag the stray space almost always signals a typo that renders a submission URL which fails server-side route matching.

Don't:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Do:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% is almost always a typo for %}. The template engine does not recognize }% as a tag delimiter, so the tag is never parsed: the raw {% ... }% text leaks into the rendered HTML, or the engine raises a syntax error when it hits the unclosed tag.

Don't:

```html
{% include "footer.html" }%
```

Do:

```html
{% include "footer.html" %}
```

#### H035

`Meta tags should be self closing.`

In plain HTML5 the trailing slash on `<meta>` is optional, but templates that are also fed through XML/XHTML tooling (XML validators, email pipelines, XSLT) fail to parse when void elements are not self-closed. Enabling this rule keeps `<meta>` tags in the XHTML-compatible `<meta ... />` form so the same markup survives both parsers.

Off by default; enable with `--include=H035`. A subset of H017 (which enforces the trailing slash on all void tags, meta included); enable H035 alone only if you want the XHTML form just for meta. Mutually exclusive with H018; do not enable both.

Don't:

```html
<meta name="viewport" content="width=device-width">
```

Do:

```html
<meta name="viewport" content="width=device-width" />
```

#### H036

`Avoid use of <br> tags.`

`<br>` encodes presentation in markup: using it for spacing or to fake paragraphs breaks text reflow at narrow widths and degrades accessibility, since screen readers announce forced breaks instead of a natural pause between blocks. Separate thoughts belong in separate block elements, and vertical spacing belongs to CSS margins. Note that `<br>` is legitimate where the line break is part of the content itself (postal addresses, poems, lyrics), and this rule cannot tell those apart from presentational use: it flags every `<br>`. Leave it disabled if your templates render such content.

Off by default; enable with `--include=H036`.

Don't:

```html
<p>Shipping is free.<br>Delivery takes 3 days.</p>
```

Do:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Duplicate attributes are invalid HTML, and browsers keep only the first occurrence and silently drop the rest, so the second class or style value never takes effect, which hides real bugs. The check is template-aware: an attribute repeated in mutually exclusive branches (`{% if %}`/`{% else %}`) is not flagged, since only one copy can render.

Don't:

```html
<div class="card" id="profile" class="active">...</div>
```

Do:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

A block tag such as `{% if %}`, `{% for %}` or `{% macro %}` without its matching end tag is a hard TemplateSyntaxError in Django and Jinja: the page fails to render at request time, which this rule catches before deploy. It also flags orphan end tags with no opening tag and incorrectly interleaved blocks (e.g. `{% if %}``{% for %}``{% endif %}`).

`{% block %}`/`{% endblock %}` pairing and endblock-name mismatches are checked by this rule; T003 (off by default) additionally demands a name on every multi-line `{% endblock %}`. Custom block tags registered via custom_blocks are also checked, including their self-closing / %} form.

Don't:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Do:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

A template tag opened with `{{` or `{%` but never closed with the matching `}}` or `%}` is not parsed as a tag: Django/Jinja either raise a TemplateSyntaxError or render the raw brace characters into the page, and everything up to the next delimiter can be silently swallowed. These typos (a single missing brace, a mismatched delimiter) are easy to miss in review because the template may still partially render.

Don't:

```html
<p>{{ user.name }</p>
```

Do:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

An `{% extends %}` or `{% include %}` tag with a missing, empty, or whitespace-only template name has nothing to load: Django raises TemplateSyntaxError when the name is missing entirely, and TemplateDoesNotExist at render time when it is empty, so the page 500s in production even though the template file itself looks syntactically plausible.

Don't:

```html
{% extends "" %}
```

Do:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

When an HTML tag is opened in one `{% block %}` but closed in another, a child template that overrides only one of those blocks inherits half of the element, producing unbalanced markup in the rendered page; browsers then auto-close or re-nest elements unpredictably, breaking layout and CSS selectors far from the template that was actually edited. Keeping each element opened and closed within the same block makes every block safe to override independently.

Don't:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Do:

```html
{% block content %}
<div class="wrapper">
</div>
{% endblock content %}
{% block footer %}
{% endblock footer %}
```

#### H042

`Label for attribute has no matching element id in this file.`

Off by default; enable with --include=H042.

The check runs only on files it can analyze soundly: if the file contains anything that could render an id this file never shows (a `{{ ... }}` output such as a form widget, an `{% include %}` or `{% extends %}`, or an unrecognized template tag), the rule stays silent for that file. Where it does run, a report is a real broken association.

Don't:

```html
<label for="email">Email</label>
<input id="username">
```

Do:

```html
<label for="email">Email</label>
<input id="email">
```

{% endraw %}

<!-- prettier-ignore-end -->

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

## Custom Rules

You can add custom rules just for your project by creating a `.djlint_rules.yaml` alongside
your `pyproject.toml`. Rules can be added to this files and djLint will pick them up.
A rules file in another location can be given with the `--rules` CLI option.

### Pattern Rules

You can add rules that fails if one of the regex pattern has a match:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Python module Rules

You can add rules that import and execute a custom python function:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

The specified `python_module` must contain a `run()` function that will be executed on
every checked file. It must accept the following arguments:

::: content

- `rule`: The dict that represent your rule in `.djlint_rules.yaml`. You will typically
  use this variable to access the rule name and message.
- `config`: The DJLint configuration object.
- `html`: The full html content of the file.
- `filepath`: Path to the file that we are currently checking.
- `line_ends`: List of line `start` and `end` character position that you can use with
  `djlint.lint.get_line()` to get line numbers from a character position. See the example.
- `*args, **kwargs`: We might add other arguments in the future, so you should include
  those two arguments to reduce the risk of failure on djLint upgrade.
  :::

It must return a list of dict, one for each errors, with the following keys:

::: content

- `code`: Code name of the rule that report the error (typically `rule['name']`)
- `line`: Line number and character number on this line, separated by a ':' as a string.
  For example `"2:3"` means that the error has been found on line 2, character 3
- `match`: The part of the content that contains the error
- `message`: The message that will be printed to signal the error (typically `rule['message']`)
  :::

```python
from typing import Any, Dict, List
from djlint.settings import Config
from djlint.lint import get_line
import re


def run(
    rule: Dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: List[Dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> List[Dict[str, str]]:
    """
    Rule that fails if if the html file contains 'bad'. This is just an example, in
    reality it's much simpler to do that with "pattern rule".
    """
    errors: List[Dict[str, str]] = []
    for match in re.finditer(r"bad", html):
        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })
    return errors
```
