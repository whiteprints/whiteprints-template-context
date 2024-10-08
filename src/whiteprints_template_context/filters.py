# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT
"""Define custom Jinja2 filters."""

from __future__ import annotations

from jinja2 import Environment
from jinja2.ext import Extension
from license_expression import (  # type: ignore [reportMissingTypeStubs]
    ExpressionInfo,
    get_spdx_licensing,
)


class LicenseExpressionError(ValueError):
    """Errors in the validation of SPDX license expressions.

    This error is typically raised when a provided license expression is
    determined to be invalid according to the SPDX standard. It optionally
    includes details of the validation errors encountered.

    Args:
        expression_info: Optional details of the validation errors related to
            the SPDX license expression.
    """

    def __init__(self, expression_info: ExpressionInfo | None = None) -> None:
        """Instantiate a LicenseExpressionError."""
        error_message = (
            "Invalid license expression. See https://spdx.org/licenses."
        )
        if expression_info:
            errors = (  # type: ignore [reportGeneralTypeIssues]
                expression_info.errors
            )
            error_message += f" Details: {errors}."

        super().__init__(error_message)


def is_spdx_expression(value: str) -> bool:
    """Check if a given string is a valid SPDX license expression.

    This function validates a provided license expression string against
    the SPDX license standard. If the expression is valid, it returns True.
    If the expression is invalid, it raises a LicenseExpressionError.

    Args:
        value: The license expression string to validate.

    Returns:
        True if the provided string is a valid SPDX license expression.

    Raises:
        LicenseExpressionError: If the expression is invalid or if there is an
            error during the parsing process.
    """
    licensing = get_spdx_licensing()
    try:
        info = licensing.validate(  # type: ignore [reportGeneralTypeIssues]
            value
        )
    except AttributeError as expression_parse_error:
        raise LicenseExpressionError from expression_parse_error

    if info.errors:  # type: ignore [reportGeneralTypeIssues]
        raise LicenseExpressionError(info)

    return True


class WhiteprintsFilters(Extension):  # pylint: disable=abstract-method
    # Pylint tells that parse method need to be overriden, but is our case
    # it is not necessary.
    """Jinja2 extension for adding custom filters.

    Args:
        environment (Environment): The Jinja2 environment to which the filter
            is added.
    """

    def __init__(self, environment: Environment) -> None:
        """Instantiate a WhiteprintsFilters."""
        super().__init__(environment)
        environment.tests["spdx_expression"] = is_spdx_expression
