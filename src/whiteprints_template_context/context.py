# SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>
#
# SPDX-License-Identifier: MIT
"""Update Copier context."""

from __future__ import annotations

import re
import sys
import unicodedata
import warnings
from abc import abstractmethod
from collections.abc import Iterator
from functools import lru_cache
from typing import Any, Callable, Final, cast

from jinja2 import Environment
from jinja2.ext import Extension
from jinja2.runtime import Context
from license_expression import (  # type: ignore [reportMissingTypeStubs]
    BaseSymbol,
    get_spdx_licensing,
)


if sys.version_info < (3, 12):
    from typing_extensions import override
else:
    from typing import override


LATEST_PYTHON: Final = 13

# SPDX-SnippetBegin
# SPDX-License-Identifier: ISC
# SPDX-FileCopyrightText: Copyright (c) 2021, Timothée Mazzucotelli
# SPDX-FileCopyrightText: © 2024 The Whiteprints Authors <whiteprints@pm.me>

# This snippet is adapted from
# https://github.com/copier-org/copier-templates-extensions/blob/main/src/copier_templates_extensions/extensions/context.py

_SENTINEL = object()


class ContextHook(Extension):
    """Extension allowing to modify the Copier context."""

    update = _SENTINEL

    def __init__(self, environment: Environment) -> None:
        """Initialize the object.

        Arguments:
            environment: The Jinja environment.
        """
        extension_self = self
        super().__init__(environment)

        # we ignore coverage for this class for now as it is difficult to test
        # with little benefits. PR Welcome though!
        class ContextClass(environment.context_class):  # pragma: no cover
            """Modify jinja2 environment.

            This extension allows subclasses to customize or update the context
            dictionary used during template rendering. It is useful for
            injecting additional data into the context or adjusting values
            based on project configurations before rendering.

            Attributes:
                update: A placeholder used internally to track if deprecated
                    update behavior is present.
            """

            # pylint: disable=too-few-public-methods
            # pylint tells us that the class has too few public methods but
            # this is a false positive as the class we need subclass the
            # context_class.

            def __init__(
                self,
                env: Environment,
                parent: dict[str, Any],
                name: str | None,
                blocks: dict[str, Callable[[Context], Iterator[str]]],
                *_args: object,
                **_kwargs: object,
            ) -> None:
                """Create a ContextClass instance."""
                if extension_self.update is not _SENTINEL:
                    warnings.warn(
                        "The `update` attribute of `ContextHook` subclasses is"
                        " deprecated. The `hook` method should now always"
                        "modify the `context` in place.",
                        DeprecationWarning,
                        stacklevel=1,
                    )

                context = extension_self.hook(parent)
                if context is not None and "_copier_conf" in parent:
                    parent.update(context)
                    warnings.warn(
                        "Returning a dict from the `hook` method is"
                        " deprecated. It should now always modify the"
                        " `context` in place.",
                        DeprecationWarning,
                        stacklevel=1,
                    )

                super().__init__(env, parent, name, blocks)

        environment.context_class = ContextClass

    @abstractmethod
    def hook(self, context: dict[str, Any]) -> dict[str, Any] | None:
        """Abstract hook for modifying the context.

        Subclasses should override this method to modify the provided context.
        The method can either directly modify the input `context` in-place
        or return a new dictionary that will be used to update the original
        context.

        Arguments:
            context: The context to be modified, containing various
                project-related settings and values.

        Returns:
            A modified context dictionary, or None if the context is updated
            in-place.

        Raises:
            NotImplementedError: This method must be overridden in a subclass.
        """


# SPDX-SnippetEnd


# SPDX-SnippetBegin
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Copyright (c) Django Software Foundation and individual contributors.
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
    """Extract SPDX symbols from a license expression.

    This function parses a given SPDX license expression and returns a set
    containing the symbols (licenses or exceptions) used in that expression.

    Arguments:
        expression: An SPDX license expression string, such as "MIT AND
           Apache-2.0".

    Returns:
        A set of SPDX symbols (e.g., {"MIT", "Apache-2.0"}) extracted from the
           input expression.
    """
    licensing = get_spdx_licensing()
    license_symbols = cast(
        list[BaseSymbol],
        licensing.license_symbols(  # type: ignore [reportGeneralTypeIssues]
            expression
        ),
    )
    return {symbol.obj for symbol in license_symbols}


class ContextUpdater(ContextHook):  # pylint: disable=abstract-method
    # Pylint tells that parse method need to be overriden, but is our case
    # it is not necessary.
    """Modify the Copier context with additional computed values.

    This method updates the context with various derived attributes based on
    the provided input context. It includes attributes like `latest_python`,
    `project_slug`, `package_name`, `target_python`, `tox_python_list`, and
    license-related information.

    Arguments:
        context: A dictionary representing the current context of the project,
            containing values like `project_name`, `target_python_version`,
            `code_license_id`, and `resources_license_id`.

    Returns:
        A dictionary containing the updated context values, including modified
        project settings and license information.
    """

    @override
    def hook(self, context: dict[str, Any]) -> dict[str, Any]:
        latest_python = LATEST_PYTHON
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
