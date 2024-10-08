<!--
SPDX-FileCopyrightText: © 2024 The "Whiteprints template context" contributors <whiteprints@pm.me>

SPDX-License-Identifier: CC-BY-NC-SA-4.0
-->

# ⚡ Quickstart

To activate the template just add the following to copier.yml:

```yaml
_jinja_extensions:
  - whiteprints_template_context.context.ContextUpdater
  - whiteprints_template_context.filters.WhiteprintsFilters
```

This will enhance copier's context with additional variables and filters that
are required by Whiteprints templates.
