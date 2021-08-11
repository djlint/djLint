# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------


# -- Project information -----------------------------------------------------

project = "djlint"
copyright = "2021, Riverside Healthcare"
author = "Christopher Pickering"
release = "0.2.4"
version = release

# -- General configuration ---------------------------------------------------

extensions = ["myst_parser", "sphinx_copybutton"]

templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"

html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
    ]
}

html_theme_options = {
    "show_related": False,
    "description": "Html Template Lint",
    "github_button": True,
    "github_user": "Riverside-Healthcare",
    "github_repo": "djlint",
    "github_type": "star",
    "show_powered_by": False,
    "fixed_sidebar": True,
    "logo": "icon.png",
}

html_static_path = ["_static"]

source_suffix = [".rst", ".md"]

pygments_style = "sphinx"
