"""Djlint html parser tests.

run::

   pytest tests/test_parser.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

   # for a single test

   pytest tests/test_parser.py::test_T028 --cov=src/djlint --cov-branch \
         --cov-report xml:coverage.xml --cov-report term-missing

"""

from src.djlint.formatter.parser import HTMLParser


def test_test():
    p = HTMLParser()
    a = p.feed("<div></div>")
    p.close()

    assert a == 1
