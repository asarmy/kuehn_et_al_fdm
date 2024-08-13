# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import toml
import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

# project = 'kuehn-et-al-fdm: Implementation of the Kuehn et al. (2024) Fault Displacement Model'
# copyright = '2024, Alex Sarmiento'
# author = 'Alex Sarmiento'

# The full version, including alpha/beta/rc tags
# release = '0.0.1'

with open(os.path.join(os.path.dirname(__file__), "../pyproject.toml"), "r") as f:
    pyproject_data = toml.load(f)

project = pyproject_data["project"]["name"]
author = pyproject_data["project"]["authors"][0]["name"]
copyright = f"2024, {author}"
release = pyproject_data["project"]["version"]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinxcontrib.bibtex",
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Additional configurations -------------------------------------------------

# Specify the location of your BibTeX files
bibtex_bibfiles = ["references.bib"]

# Hidden doesn't seem to work in index, exclude here
exclude_patterns = ["modules.rst"]

# Hide private files
autodoc_default_options = {"private-members": False}

# Needed to get docstrings to show on RTD
autodoc_mock_imports = ["numpy", "pandas", "scipy", "kuehn_et_al_fdm"]
