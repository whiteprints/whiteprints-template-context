# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT

"""Sphinx configuration."""

# pylint: disable=invalid-name

from importlib import metadata
from pathlib import Path


project = "Whiteprints template context"
author = "Romain Brault"
project_copyright = "2024 {} {} - {}"
project_copyright = project_copyright.format(
    'The "Whiteprints template context" contributors',
    "<whiteprints@pm.me>",
    "Distributed under license CC-BY-NC-SA-4.0",
)
release = metadata.version("whiteprints_template_context")
version = ".".join(release.split(".")[:3])
language = "en"
myst_heading_anchors = 3
extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "autoapi.extension",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]
autoapi_type = "python"
autoapi_dirs = ["../src"]
autoapi_template_dir = "_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",
    "special-members",
    "show-module-summary",
    "imported-members",
]
autodoc_typehints = "both"
autosectionlabel_prefix_document = True
napoleon_use_param = True
napoleon_numpy_docstring = False
napoleon_google_docstring = True
python_maximum_signature_line_length = 72
html_favicon = "_static/logo.svg"
html_logo = "_static/logo.svg"
html_static_path = ["_static"]
html_extra_path = []
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/whiteprints/whiteprints-template-context",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/whiteprints-template-context",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
    ],
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pip": ("https://pip.pypa.io/en/stable", None),
    "tox": ("https://tox.wiki/en/stable/", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "click": ("https://click.palletsprojects.com/en/8.1.x/", None),
    "beartype": ("https://beartype.readthedocs.io/en/stable/", None),
    "pytest": ("https://docs.pytest.org/en/stable/", None),
}
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]
myst_substitutions = {
    "licenses": "\n".join(
        f" - [{license_path.stem}](path:{license_path})"
        for license_path in Path("../LICENSES").glob("*.txt")
    )
}
exclude_patterns = [
    "_autoapi_templates/**",
]
linkcheck_ignore = [
    r"https://pypi\.org/project/.*",
    r"https://.*\.readthedocs\.io/en/stable/",
]
