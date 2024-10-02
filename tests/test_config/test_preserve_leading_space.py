"""Test for preserve leading space.

--preserve-leading-space

uv run pytest tests/test_config/test_preserve_leading_space.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from djlint.reformat import formatter
from tests.conftest import config_builder, printer

if TYPE_CHECKING:
    from typing_extensions import Any

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
            "     ip address 10.1.2.1/30\n"
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
            "     ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "{% endif %}\n"
        ),
        ({"preserve_blank_lines": True, "preserve_leading_space": True}),
        id="network stuff",
    ),
    pytest.param(
        (
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
            " {% if abc == 102 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "  {% endif %}\n"
            "\n"
            "{% if abc == 103 %}\n"
            " interface Ethernet1/2\n"
            "   description // Connected to leaf-2\n"
            "   no switchport\n"
            "   ip address 10.1.2.1/30\n"
            "   ip router ospf 1 area 0.0.0.0\n"
            "   no shutdown\n"
            "            {% endif %}\n"
        ),
        (
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
]


@pytest.mark.parametrize(("source", "expected", "args"), test_data)
def test_base(source: str, expected: str, args: dict[str, Any]) -> None:
    output = formatter(config_builder(args), source)

    printer(expected, source, output)
    assert expected == output
