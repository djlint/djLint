"""Test for preserve blank lines.

--preserve-blank-lines

poetry run pytest tests/test_config/test_preserve_blank_lines.py
"""
import pytest

from src.djlint.reformat import formatter
from tests.conftest import config_builder, printer

test_data = [
    pytest.param(
        (
            "---\n"
            "my:yaml\n"
            "---\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "{% if   abc == 101 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "{% endif %}\n"
            "\n"
            "\n"
            "{% if abc == 102 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "{% endif %}\n"
            "\n"
            "{% if abc == 103 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "{% endif %}\n"
        ),
        (
            "---\n"
            "my:yaml\n"
            "---\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "{% if   abc == 101 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "{% endif %}\n"
            "\n"
            "\n"
            "{% if abc == 102 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "{% endif %}\n"
            "\n"
            "{% if abc == 103 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "{% endif %}\n"
        ),
        ({"preserve_blank_lines": True, "preserve_leading_space": True}),
        id="network stuff",
    ),
    pytest.param(
        ("{% block someblock %}{% endblock %}\n" "<br />\n" "<br />\n"),
        ("{% block someblock %}{% endblock %}\n" "<br />\n" "<br />\n"),
        ({"preserve_blank_lines": True}),
        id="whitespace test",
    ),
    pytest.param(
        ("<div>"),
        ("<div>\n"),
        ({"preserve_blank_lines": True}),
        id="whitespace test",
    ),
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source, expected, args):
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
