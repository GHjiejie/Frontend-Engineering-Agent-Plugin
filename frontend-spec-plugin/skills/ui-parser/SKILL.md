---
name: ui-parser
description: Convert Figma designs, screenshots, Axure exports, HTML prototypes, or written UI descriptions into a semantic frontend UI tree. Use when Codex must inventory pages, components, controls, fields, tables, dialogs, tabs, navigation, responsive variants, visible states, and uncertain visual details before interaction design.
---

# UI Parser

Write `frontend-spec/ui/ui-tree.json` from the supplied visual evidence.

## Parse the design

1. Read `../../references/artifact-contract.md` and `../../schemas/ui-tree.schema.json`.
2. Inspect the highest-fidelity source available and record its source locator, frame, screenshot, or node identifier.
3. Assign stable IDs `UI-###` and preserve page/component hierarchy.
4. Capture semantic role, visible label, data binding, enabled/disabled conditions, validation hints, actions, parent, children, and linked requirement IDs.
5. Record loading, empty, error, success, permission-denied, responsive, hover, focus, selected, and disabled variants only when visible or required.
6. Treat component reuse as proposed unless the user explicitly supplied frontend component code that proves an existing reusable component.

## Handle uncertainty

Do not infer hidden behavior from appearance alone. Do not browse the project for missing design details. Add unclear controls, missing states, inconsistent labels, or non-accessible affordances to `unresolved` with evidence and impact. Complete the stage when every visible interactive element has an ID and every required page has a known design mapping or explicit design gap.
