"""Djlint setup."""

from pathlib import Path

from setuptools import find_packages, setup

project_path = Path(__file__).parent

__version__ = "0.2.4"


def long_description():
    """Build long description from readme and changelog."""
    return (
        (project_path / "README.md").read_text(encoding="utf8")
        + "\n\n"
        + (project_path / "CHANGELOG.md").read_text(encoding="utf8")
    )


test_deps = ["coverage", "pytest", "pytest-xdist", "pytest-cov"]

extras = {
    "test": test_deps,
}

setup(
    name="djlint",
    version=__version__,
    author="Christopher Pickering",
    author_email="cpickering@rhc.net",
    description="Django Template Linter",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "https://djlint.readthedocs.io",
        "Source": "https://github.com/Riverside-Healthcare/djlint",
    },
    url="",
    include_package_data=True,
    package_data={"djlint": ["rules.yaml"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "click>=7.1.2",
        "pyyaml>=5.4.1",
        "colorama>=0.4.3",
        "regex>=2020.11.13",
        "tqdm>=4.61.2",
    ],
    test_suite="tests.test_djlint",
    entry_points={
        "console_scripts": [
            "djlint=djlint:main",
        ]
    },
    tests_require=test_deps,
    extras_require=extras,
)
