# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT

"""Test Copier context update."""

import re

from hypothesis import given
from hypothesis import strategies as st
from jinja2 import Environment

from whiteprints_template_context.context import (
    LATEST_PYTHON,
    ContextUpdater,
    slugify,
    spdx_symbols,
)


class TestSlugify:
    """Test suite for the slugify function."""

    UNICODE_EXAMPLES = st.sampled_from([
        "Café Münsterländer",
        "naïve café",
        " résumé",
        "jalapeño",
        "façade",
    ])
    TEXT_STRATEGY = st.one_of(st.text(), UNICODE_EXAMPLES)

    @staticmethod
    @given(TEXT_STRATEGY)
    def test_slugify(value: str) -> None:
        """Test the slugify function for both Unicode and ASCII slugs."""
        assert not slugify(""), "Empty string should return an empty slug."

        result_unicode = slugify(value, allow_unicode=True)
        if value:
            assert re.match(r"^[\w\s-]*$", result_unicode), (
                "Unicode slug not valid"
            )

        result_ascii = slugify(value, allow_unicode=False)
        if value:
            assert re.match(r"^[a-z0-9-_]*$", result_ascii), (
                "ASCII slug not valid"
            )


class TestSpdxSymbols:
    """Test suite for the spdx_symbols function."""

    # Define a basic strategy for SPDX expressions as a class variable
    SPDX_IDENTIFIERS = st.sampled_from([
        "MIT",
        "GPL-2.0-only",
        "GPL-3.0-or-later",
        "Apache-2.0",
        "BSD-3-Clause",
        "CC-BY-4.0",
        "MPL-2.0",
        "ISC",
        "Zlib",
        "EPL-1.0",
    ])

    # Create a strategy that mixes random text with SPDX expressions
    MIXED_SPDX_AND_RANDOM = st.one_of(
        SPDX_IDENTIFIERS,
    )

    @staticmethod
    @given(MIXED_SPDX_AND_RANDOM)
    def test_spdx_symbols(expression: str) -> None:
        """Test that spdx_symbols returns a set of strings.

        Args:
            expression: a be random text or a valid SPDX identifier.
        """
        result = spdx_symbols(expression)
        assert isinstance(result, set), "Result should be a set"
        for symbol in result:
            assert isinstance(symbol, str), "Each symbol should be a string"


def test_context_updater() -> None:
    """Test the context updater."""
    updater = ContextUpdater(environment=Environment())
    context = {
        "target_python_version": "py310",
        "project_name": "Test Project",
        "code_license_id": "MIT",
        "resources_license_id": "Apache-2.0",
    }

    updated_context = updater.hook(context)

    assert (
        updated_context["latest_python"] == LATEST_PYTHON
    ), "Latest Python version mismatch"
    assert updated_context["project_slug"] == "test-project", "Slugify failed"
    assert (
        updated_context["package_name"] == "test_project"
    ), "Package name mismatch"
    assert (
        updated_context["target_python"] == "3.10"
    ), "Target Python version mismatch"

    # Verify SPDX symbols and replacements
    assert (
        "MIT" in updated_context["code_license_symbols"]
    ), "License symbol mismatch"
    assert updated_context["code_license_text_ext"].startswith(
        "[MIT]"
    ), "SPDX link not replaced"
    assert updated_context["code_license_text"].startswith(
        "[MIT]"
    ), "License text replacement failed"
