---
name: dashboard-ui-figma-restore
description: Restore Neo Cloud dashboard-ui pages from node-specific Figma designs with scoped Vue implementation, token-aware styling, and mandatory design and regression visual validation. Use when a user asks to implement, refactor, visually align, pixel-match, or restore a page under dashboard/dashboard-ui after requirements, prototype, API, and interaction decisions are approved.
---

# Dashboard UI Figma Restore

Turn a developer-approved frontend specification and Figma frame into a scoped `dashboard/dashboard-ui` implementation. Preserve dashboard tokens, existing frontend architecture, accessibility, and visual-test integrity. In this skill, **developer** means the requesting user who controls the implementation scope and approvals.

Resolve artifact paths from the active feature root selected by `$generate-frontend-spec` when this skill is used as part of that workflow.

## Required inputs

Before changing code, require all of the following:

- A node-specific Figma design URL.
- The exact dashboard page, module, route, or visual scenario to change.
- The selected `dashboard-ui` frontend root or another exact frontend target path explicitly approved by the user.
- Approved product and interaction decisions. Prefer the active feature's `document/frontend-development-spec.md`, `requirement/decision-log.md`, `ui/ui-tree.json`, `api/api-map.json`, and `interaction/interaction-spec.json` when available.

If the Figma node, target, or frontend root is missing or ambiguous, ask one concise grouped question and stop. Do not discover the answer by scanning the project.

## Enforce the frontend boundary

- Stay inside the user-approved frontend root and selected page.
- Read only the target page/components, their minimum direct frontend imports, and the exact style, token, test, and visual-reference files needed for this restoration.
- Read applicable `AGENTS.md` or `CLAUDE.md` instructions only along the approved frontend path and its necessary ancestors. Do not use them as a reason to inspect general project background.
- Do not browse backend code, infrastructure, unrelated pages, package workspaces, or repository history for context.
- Do not revert, overwrite, or incorporate unrelated user changes. Check changes only inside the authorized frontend root before editing, for example `git -C <authorized-frontend-root> status --short -- .`, and report pre-existing in-scope changes separately.

## Preflight

1. Verify that Figma capabilities are callable before Figma-dependent work.
   - Before calling `get_design_context`, load and follow the `figma:figma-design-to-code` skill.
   - Prefer `get_design_context` for design-to-code evidence. Use Figma metadata and screenshots only to fill specific gaps.
   - Before calling `use_figma`, load and follow the `figma:figma-use` skill.
   - If no callable Figma capability is available, tell the user to install or configure the Figma plugin and retry with the same URL and target. Stop without editing.
2. Read the approved feature artifacts listed under **Required inputs**. Treat confirmed decisions as authoritative; record any conflict with the Figma source rather than silently choosing.
3. Within the approved frontend scope, inspect only:
   - the named target page and minimum direct components;
   - relevant page styles and `src/styles/tokens.css`, `src/styles/dashboard-semantic-tokens.css`, or exact generated token definitions referenced by those styles;
   - the authorized frontend root's exact `package.json` and directly relevant test/build configuration solely to identify and run the required checks;
   - the visual config, scenario spec, and reference registry required for the named scenario;
   - focused tests directly covering the target.
4. Capture path-scoped status for the authorized frontend root without changing it. Do not enumerate changes elsewhere in the repository.

## Restoration brief gate

Do not modify application code, test code, configuration, visual references, or any other workspace artifact until the developer has approved a restoration brief. Before approval, the only permitted write is `<feature-root>/implementation/restoration-brief.md` when an active feature root exists.

The brief must include:

- Figma file, node/frame identity, viewport size, and key layout measurements.
- Requirement, interaction, and API decisions that constrain the UI.
- Exact frontend files/components likely to change.
- Token strategy: values mapped to `--dashboard-*`, `--wylon-*`, or stable page/component tokens.
- Expected unavoidable deviations caused by data, existing components, responsive behavior, or accessibility.
- Validation plan: targeted tests, type checking, build, token/style audits, design comparison, and regression comparison.

Write or update the brief at `<feature-root>/implementation/restoration-brief.md` when an active feature root exists. Present the concise brief to the developer and ask for explicit approval. A direct instruction such as “按这个方案立即实现” counts only when it follows a brief containing the items above; a general request to build the feature does not bypass this gate.

## Implementation rules

- Keep changes scoped to the approved page. Do not change unrelated pages, backend logic, API contracts, generated token files, or unrelated test baselines.
- Follow existing Vue 3, TypeScript, and CSS patterns visible inside the approved scope. Prefer focused component edits over broad rewrites.
- Use CSS custom properties:
  - Prefer semantic `--dashboard-*` tokens in component CSS.
  - Add stable page/component tokens to `src/styles/tokens.css` when Figma-specific dimensions require names.
  - Use generated `--wylon-*` tokens through semantic aliases unless the approved scope already uses a direct token for that exact role.
  - Avoid hardcoded colors, type sizes, spacing, radii, shadows, and borders unless they are accepted local exceptions such as responsive breakpoints or accessibility utilities.
- If Figma evidence is missing or inconsistent, infer conservatively, label the inference, and do not contradict an approved decision.
- Preserve semantic headings, accessible labels, visible focus, and keyboard operation.
- Add or update focused structure tests when the visual contract or token use changes.

## Visual reference handling

- If the user provides a PNG reference, use the project's existing visual-reference convention. For the standard dashboard layout this is `tests/visual/design-references/figma/<scenario-id>/<viewport>.png`.
- If using Figma API synchronization, update only the intended entry in `tests/visual/design-references/figma.references.json` when that registry exists.
- Reuse the existing scenario ID. Common mappings are `models`, `model-detail`, and `playground`; do not invent a new ID when the target already has one.
- If the route has no visual scenario, propose a deterministic scenario ID and the exact Figma screenshot/reference acquisition path in the restoration brief. Create the scoped scenario and registry entry only after brief approval. A new regression baseline remains a candidate until separately approved.
- Never overwrite or promote an approved regression baseline without explicit user approval.

## Validation loop

Use the commands and scripts actually defined by the approved dashboard frontend. Do not scan other workspaces to find alternatives. Run the narrowest checks first and then broaden when available:

1. Targeted structure, service, and display tests for the changed page.
2. Type checking.
3. Production build.
4. Theme/token audit.
5. Style-metric audit.
6. Design visual comparison for the selected scenario.
7. Regression visual comparison for the selected scenario.

In the standard dashboard project these are commonly:

```bash
npm run type-check
npm run build
npm run theme-audit
npm run style-metric-audit
npm run test:visual:design -- --grep <scenario-or-title>
npm run test:visual:regression -- --grep <scenario-or-title>
```

If a visual check fails:

- Inspect only the selected scenario's diff and artifacts.
- Correct the implementation and rerun the affected checks when it diverges from Figma.
- If the approved design intentionally supersedes the regression baseline, generate a candidate with the project's existing capture workflow and ask the user to review it.
- Promote a candidate only after explicit approval.
- Continue until both visual comparisons pass or an external blocker is proven, such as unavailable Figma access, a local server failure, or pending baseline approval.

Write the executed commands, results, diff locations, deviations, and pending approvals to `<feature-root>/implementation/visual-validation.md` when an active feature root exists.

## Final report

Report:

- Files changed.
- Figma node and design reference used.
- Requirement/API decisions honored.
- Token strategy and deviations.
- Exact checks run with pass, fail, or blocker status.
- Any candidate baseline awaiting approval.
- Unrelated pre-existing changes observed inside the authorized frontend scope, separately. Do not inspect or report repository changes outside that scope.

Do not claim implementation, visual validation, or feature delivery complete if either the design comparison or regression comparison was skipped, failed, or blocked.
