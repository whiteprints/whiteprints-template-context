# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT

"""Shared test configuration file."""

import pkgutil
from pathlib import Path
from typing import Final


FIXTURE_DIRECTORY_NAME: Final = "fixtures"
FIXTURES_ROOT: Final = Path(__file__).parent / FIXTURE_DIRECTORY_NAME


pytest_plugins = [
    ".".join((__package__ or "", FIXTURE_DIRECTORY_NAME, name))
    for _module_finder, name, _ispkg in pkgutil.walk_packages(
        path=map(str, [FIXTURES_ROOT])
    )
]
