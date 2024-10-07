# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT

"""Jinja2 environment fixtures."""

import pytest
from jinja2 import Environment


@pytest.fixture(scope="class")
def environment() -> Environment:
    """Fixture for creating a Jinja2 environment.

    This fixture sets up a Jinja2 environment with automatic HTML escaping
    enabled, which is suitable for rendering templates securely. The
    environment can be used for rendering templates with context data, ensuring
    that variables are properly escaped to prevent injection vulnerabilities.

    Returns:
        A Jinja2 environment instance with `autoescape` set to `True`.
    """
    return Environment(autoescape=True)
