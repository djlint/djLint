"""Test jazzband sorl-thumbnail tag.

https://github.com/jazzband/sorl-thumbnail

poetry run pytest tests/test_django/test_thumbnail.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            '{% thumbnail person.profile_photo "200x200" crop="center" as im %}\n'
            '   <img src="{{ im.url }}"\n'
            '        width="{{ im.width }}"\n'
            '          height="{{ im.height }}"\n'
            '         class="img-thumbnail"\n'
            '         alt="{{ person.name }}">\n'
            "{% endthumbnail %}\n"
        ),
        (
            '{% thumbnail person.profile_photo "200x200" crop="center" as im %}\n'
            '    <img src="{{ im.url }}"\n'
            '         width="{{ im.width }}"\n'
            '         height="{{ im.height }}"\n'
            '         class="img-thumbnail"\n'
            '         alt="{{ person.name }}">\n'
            "{% endthumbnail %}\n"
        ),
        id="thumbnail",
    ),
]


@pytest.mark.parametrize(("source", "expected"), test_data)
def test_base(source, expected, django_config):
    output = formatter(django_config, source)

    printer(expected, source, output)
    assert expected == output
