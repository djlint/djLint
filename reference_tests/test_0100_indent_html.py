"""
Porting original test 'test_html/test_tag_hr' to directly use 'indent_html' formatter
instead passing through the CLI.
"""
import pytest

from src.djlint.formatter.indent import indent_html

@pytest.mark.xfail(reason="Awaiting full spec for expected result")
def test_indent_html_tag_html5(basic_config) -> None:
    """
    Test a hr element parsing in its HTML5 form
    """
    source = (
        '<div>'
        '    <div>'
        '        <hr>'
        '    </div>'
        '</div>'
        ''
    )
    expected = ('')

    result = indent_html(source, basic_config)

    print()
    print(("."*60), "Expected", ("."*60))
    print(expected)
    print()
    print(("."*60), "Result", ("."*60))
    print(result)
    print()

    assert result == expected
    assert 1 == 42


@pytest.mark.xfail(reason="Awaiting full spec for expected result")
def test_indent_html_tag_autoclose(basic_config) -> None:
    """
    Test a hr element parsing in its auto-close form
    """
    source = (
        '<div>'
        '    <div>'
        '        <hr />'
        '    </div>'
        '</div>'
        ''
    )
    expected = ('')

    result = indent_html(source, basic_config)

    print()
    print(("."*60), "Expected", ("."*60))
    print(expected)
    print()
    print(("."*60), "Result", ("."*60))
    print(result)
    print()

    assert result == expected
    assert 1 == 42
