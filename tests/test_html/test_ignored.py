"""Djlint tests specific to html.

run::

   pytest tests/test_html.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_html.py::test_front_matter --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing


"""
# pylint: disable=C0116

from typing import TextIO

from click.testing import CliRunner

from tests.conftest import reformat


def test_ignored_block(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<!-- <span> -->
    <div><p><span></span></p></div>
    <!-- <div> -->
    """,
    )

    assert output.exit_code == 1

    assert (
        output.text
        == """<!-- <span> -->
<div>
    <p>
        <span></span>
    </p>
</div>
<!-- <div> -->
"""
    )

    # check custom ignore tag {# djlint:off #} {# djlint:on #}
    output = reformat(
        tmp_file,
        runner,
        b"""<!-- djlint:off -->
<div><p><span></span></p></div>
<!-- djlint:on -->
{# djlint:off #}
<div><p><span></span></p></div>
{# djlint:on #}
{% comment %} djlint:off {% endcomment %}
<div><p><span></span></p></div>
{% comment %} djlint:on {% endcomment %}
{{ /* djlint:off */ }}
<div><p><span></span></p></div>
{{ /* djlint:on */ }}
{{!-- djlint:off --}}
<div><p><span></span></p></div>
{{!-- djlint:on --}}
""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""{# djlint: off #}<meta name="description" content="{% block meta_content %}Alle vogelkijkhutten van Nederland{% endblock %}">{# djlint:on #}
""",
    )

    assert output.exit_code == 0

    # check script tag
    output = reformat(
        tmp_file,
        runner,
        b"""<script>
    <div><p><span></span></p></div>
</script>
""",
    )

    assert output.exit_code == 0

    assert (
        """<script>
    <div><p><span></span></p></div>
</script>
"""
        in output.text
    )

    # check inline script includes
    output = reformat(
        tmp_file,
        runner,
        b"""<html>
    <head>
        <link href="{% static  'foo/bar.css' %}" rel="stylesheet"/>
        <!--JS-->
        <script src="{% static  'foo/bar.js' %}"></script>
    </head>
</html>
""",
    )
    print(output.text)
    assert output.exit_code == 0


def test_style_tag(runner: CliRunner, tmp_file: TextIO) -> None:
    output = reformat(
        tmp_file,
        runner,
        b"""<style>
    {# override to fix text all over the place in media upload box #}
    .k-dropzone .k-upload-status {
        color: #a1a1a1;
    }
</style>
""",
    )

    assert output.exit_code == 0

    output = reformat(
        tmp_file,
        runner,
        b"""<style>
 .k-dropzone .k-upload-status {
       color: #a1a1a1;
           }
</style>
""",
    )

    assert output.exit_code == 0

    # check style includes
    output = reformat(
        tmp_file,
        runner,
        b"""<link href="{% static 'common/js/foo.min.js' %}"/>""",
    )

    assert output.exit_code == 0
