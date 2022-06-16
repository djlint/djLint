"""Djlint tests specific to --preserve-leading-space option.

run::

   pytest tests/test_config/test_preserve_leading_space/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   pytest tests/test_config/test_preserve_leading_space/test_config.py::test_config

"""
# pylint: disable=C0116
from click.testing import CliRunner

from src.djlint import main as djlint


def test_config(runner: CliRunner) -> None:

    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_preserve_leading_space/html.html",
            "--check",
            "--preserve-leading-space",
        ],
    )

    assert result.exit_code == 1
    assert (
        """-     {% if   abc == 101 %}
+{% if   abc == 101 %}
  interface Ethernet1/2
    description // Connected to leaf-2
    no switchport
@@ -6,8 +6,6 @@

    ip router ospf 1 area 0.0.0.0
    no shutdown
 {% endif %}
-
-
 {% if abc == 102 %}
  interface Ethernet1/2
    description // Connected to leaf-2
@@ -15,8 +13,7 @@

    ip address 10.1.2.1/30
    ip router ospf 1 area 0.0.0.0
    no shutdown
-  {% endif %}
-
+{% endif %}
 {% if abc == 103 %}
  interface Ethernet1/2
    description // Connected to leaf-2
@@ -24,4 +21,4 @@

    ip address 10.1.2.1/30
    ip router ospf 1 area 0.0.0.0
    no shutdown
-            {% endif %}
+{% endif %}
"""
        in result.output
    )
