# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT

"""Test Copier Whiteprints custom filters."""

import pytest
from hypothesis import given
from hypothesis import strategies as st
from jinja2 import Environment

from whiteprints_template_context.filters import (
    LicenseExpressionError,
    WhiteprintsFilters,
    is_spdx_expression,
)


class TestIsSpdxExpression:
    """Test suite for the is_spdx_expression function."""

    VALID_SPDX_STRATEGY = st.sampled_from([
        "MIT",
        "Apache-2.0",
        "GPL-3.0-or-later WITH Autoconf-exception-3.0",
        "LGPL-2.1-only",
        "CC-BY-4.0 OR MIT",
    ])
    INVALID_SPDX_STRATEGY = st.sampled_from([
        "INVALID",
        "GPL 3.0",
        "Apache2.0",
        "MIT OR GPL-2.0 AND",  # Trailing operator
        "GPL-2.0 only",  # Missing dash
    ])

    @staticmethod
    @given(VALID_SPDX_STRATEGY)
    def test_valid_spdx_expression(value: str) -> None:
        """Test that valid SPDX expressions are recognized as valid."""
        assert is_spdx_expression(
            value
        ), f"Valid SPDX expression '{value}' should pass validation"

    @staticmethod
    @given(INVALID_SPDX_STRATEGY)
    def test_invalid_spdx_expression(value: str) -> None:
        """Test that invalid SPDX expressions raise LicenseExpressionError."""
        with pytest.raises(LicenseExpressionError):
            is_spdx_expression(value)


def test_spdx_expression_filter_added() -> None:
    """Test that 'spdx_expression' test is added to the environment."""
    env = Environment(autoescape=True)
    WhiteprintsFilters(env)
    assert (
        "spdx_expression" in env.tests
    ), "'spdx_expression' should be available in Jinja2 tests"
