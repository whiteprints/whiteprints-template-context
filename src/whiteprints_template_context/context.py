# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT
"""Update Copier context."""

import re
import sys
import unicodedata
from functools import lru_cache
from typing import Any

from copier_templates_extensions import ContextHook
from license_expression import get_spdx_licensing


if sys.version_info < (3, 12):
    from typing_extensions import override
else:
    from typing import override


# SPDX-SnippetBegin
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-SnippetCopyrightText: Copyright (c) Django Software Foundation and individual contributors.
# SPDX-FileCopyrightText: © 2024 The Whiteprints Authors <whiteprints@pm.me>


def slugify(value: str, *, allow_unicode: bool = False) -> str:
    """Slugify.

    Convert to ASCII if "allow_unicode" is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren"t alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.

    Returns:
        a slug of `value`.
    """
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


# SPDX-SnippetEnd


@lru_cache
def spdx_symbols(expression: str) -> set[str]:
    """Returns the set of SPDX symbols in an expression."""
    licensing = get_spdx_licensing()
    return {
        license_symbol.obj
        for license_symbol in licensing.license_symbols(expression)
    }


class ContextUpdater(ContextHook):
    """Context updater hook."""

    @override
    def hook(self, context: dict[str, Any]) -> dict[str, Any]:
        latest_python = 13
        target_python_minor = context["target_python_version"][3:]

        context["latest_python"] = latest_python
        context["project_slug"] = slugify(context["project_name"])
        context["package_name"] = context["project_slug"].replace("-", "_")
        context["target_python"] = f"3.{target_python_minor}"
        context["tox_python_list"] = (
            "py{"
            + ",".join(
                f"3{python_minor}"
                for python_minor in range(
                    int(target_python_minor),
                    latest_python + 1,
                )
            )
            + "}"
        )
        code_license_symbols = list(spdx_symbols(context["code_license_id"]))
        context["code_license_symbols"] = list(code_license_symbols)
        context["resources_license_symbols"] = list(
            spdx_symbols(context["resources_license_id"])
        )
        context["code_license_text_ext"] = context["code_license_id"]
        for symbol in code_license_symbols:
            context["code_license_text_ext"] = context[
                "code_license_text_ext"
            ].replace(
                symbol, f"[{symbol}](https://spdx.org/licenses/{symbol})"
            )

        context["code_license_text"] = context["code_license_id"]
        for symbol in code_license_symbols:
            context["code_license_text"] = context[
                "code_license_text"
            ].replace(symbol, f"[{symbol}](../LICENSES/{symbol}.txt)")

        return context
