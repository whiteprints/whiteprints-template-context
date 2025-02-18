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
    def test_slugify_empty_string() -> None:
        """Test that an empty string returns an empty slug."""
        assert not slugify(""), "Empty string should return an empty slug."

    @staticmethod
    @given(TEXT_STRATEGY)
    def test_slugify_unicode(value: str) -> None:
        """Test the slugify function with Unicode characters."""
        result_unicode = slugify(value, allow_unicode=True)
        if value:
            assert re.match(r"^[\w\s-]*$", result_unicode), (
                "Unicode slug not valid"
            )

    @staticmethod
    @given(TEXT_STRATEGY)
    def test_slugify_ascii(value: str) -> None:
        """Test the slugify function with ASCII characters."""
        result_ascii = slugify(value, allow_unicode=False)
        if value:
            assert re.match(r"^[a-z0-9-_]*$", result_ascii), (
                "ASCII slug not valid"
            )


class TestSpdxSymbols:
    """Test suite for the spdx_symbols function."""

    SPDX_IDENTIFIERS = st.sampled_from([
        "MIT",
        "GPL-2.0-only",
        "GPL-3.0-or-later WITH LGPL-3.0-linking-exception",
        "MIT OR Apache-2.0",
        "BSD-3-Clause",
        "CC-BY-4.0",
        "MPL-2.0",
        "ISC",
        "Zlib",
        "EPL-1.0",
    ])
    MIXED_SPDX_AND_RANDOM = st.one_of(SPDX_IDENTIFIERS)

    @staticmethod
    @given(MIXED_SPDX_AND_RANDOM)
    def test_spdx_symbols_type(expression: str) -> None:
        """Test that spdx_symbols returns a set."""
        result = spdx_symbols(expression)
        assert isinstance(result, set), "Result should be a set"

    @staticmethod
    @given(MIXED_SPDX_AND_RANDOM)
    def test_spdx_symbols_elements(expression: str) -> None:
        """Test that each element in the result of spdx_symbols is a string."""
        result = spdx_symbols(expression)
        for symbol in result:
            assert isinstance(symbol, str), "Each symbol should be a string"


class TestContextUpdater:
    """Test suite for the ContextUpdater class."""

    ENVIRONMENT_EXAMPLES = st.sampled_from([
        {
            "target_python_version": "py310",
            "project_name": "Test Project",
            "code_license_id": "MIT",
            "resources_license_id": "Apache-2.0",
        },
    ])

    @staticmethod
    @given(ENVIRONMENT_EXAMPLES)
    def test_latest_python(
        environment: Environment,
        context: dict[str, str],
    ) -> None:
        """Test that the latest Python version is set correctly."""
        updater = ContextUpdater(environment)
        updated_context = updater.hook(context)
        assert updated_context["latest_python"] == LATEST_PYTHON, (
            "Latest Python version mismatch"
        )

    @staticmethod
    @given(ENVIRONMENT_EXAMPLES)
    def test_project_slug(
        environment: Environment,
        context: dict[str, str],
    ) -> None:
        """Test that the project name is slugified correctly."""
        updater = ContextUpdater(environment)
        updated_context = updater.hook(context)
        assert updated_context["project_slug"] == "test-project", (
            "Slugify failed"
        )

    @staticmethod
    @given(ENVIRONMENT_EXAMPLES)
    def test_package_name(
        environment: Environment,
        context: dict[str, str],
    ) -> None:
        """Test that the package name is derived correctly."""
        updater = ContextUpdater(environment)
        updated_context = updater.hook(context)
        assert updated_context["package_name"] == "test_project", (
            "Package name mismatch"
        )

    @staticmethod
    @given(ENVIRONMENT_EXAMPLES)
    def test_target_python_version(
        environment: Environment,
        context: dict[str, str],
    ) -> None:
        """Test that the target Python version is set correctly."""
        updater = ContextUpdater(environment)
        updated_context = updater.hook(context)
        assert updated_context["target_python"] == "3.10", (
            "Target Python version mismatch"
        )

    @staticmethod
    @given(ENVIRONMENT_EXAMPLES)
    def test_code_license_symbols(
        environment: Environment,
        context: dict[str, str],
    ) -> None:
        """Test that the code license symbols are updated correctly."""
        updater = ContextUpdater(environment)
        updated_context = updater.hook(context)
        assert "MIT" in updated_context["code_license_symbols"], (
            "License symbol mismatch"
        )

    @staticmethod
    @given(ENVIRONMENT_EXAMPLES)
    def test_code_license_text_ext(
        environment: Environment,
        context: dict[str, str],
    ) -> None:
        """Test that the extended license text."""
        updater = ContextUpdater(environment)
        updated_context = updater.hook(context)
        assert updated_context["code_license_text_ext"].startswith("[MIT]"), (
            "SPDX link not replaced"
        )

    @staticmethod
    @given(ENVIRONMENT_EXAMPLES)
    def test_code_license_text(
        environment: Environment,
        context: dict[str, str],
    ) -> None:
        """Test that the code license text is correctly replaced."""
        updater = ContextUpdater(environment)
        updated_context = updater.hook(context)
        assert updated_context["code_license_text"].startswith("[MIT]"), (
            "License text replacement failed"
        )

    @staticmethod
    def test_empty_environment(
        context: dict[str, str],
    ) -> None:
        """Test that the code do not fail if the environment is empty.

        This was introduced to solve
        https://github.com/copier-org/copier-templates-extensions/issues/7
        """
        updater = ContextUpdater({})
        updated_context = updater.hook(context)
        assert updated_context
