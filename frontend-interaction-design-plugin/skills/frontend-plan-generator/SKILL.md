---
name: frontend-plan-generator
description: Orchestrate an end-to-end, Feishu-first frontend design workflow from project/version confirmation through durable source evidence, requirement clarification, user flows, state machines, API sequences, a self-explanatory frontend plan, and review-package publication. Use for frontend design plans, task breakdowns, page/component responsibilities, state/API strategies, Figma or pasted-prototype inputs, technical-review packages, or frontend-development-plan.md; never use it to generate application code.
---

# Frontend Plan Generator

Orchestrate the complete V5 pipeline and create a Draft `<confirmed-output-directory>/frontend-development-plan.md`. Delegate final Feishu publication, fixed-revision export, `sync-manifest.json`, and Reviewability Gate #5 to `review-package-publisher`. Never generate or modify application code, commit changes, or open a pull request.

## Run preflight Gates #1 and #2 before writing

1. Inspect likely frontend roots read-only using `package.json`, `src/`, framework/build configs, routes, dependencies, and system names in supplied sources.
2. Present the most likely frontend project, absolute root, evidence, confidence, and viable alternatives. Wait for developer confirmation; never choose on their behalf.
3. Resolve a concise lowercase kebab-case feature name.
4. Inspect `<confirmed-root>/docs/frontend-design/<feature-name>/` read-only.
5. Recommend continuing the current `YYYY-MM-DD[-vN]` or creating a new version. Create a new version only for an independent PRD iteration, behavior-changing source revision, completed-plan successor, or explicit request.
6. Present the exact output directory and planned Feishu title `[Frontend Design] <Feature> / <Version>`. Wait for confirmation before local or Feishu writes.
7. Lock project, feature, version, output directory, and planned document title for all downstream skills.

Same-version clarification answers, review comments, evidence additions, diagram corrections, and wording changes must not create a new version.

## Enforce the V5 pipeline

For an end-to-end request, run these responsibilities in order:

1. `source-evidence-manager`: persist PRD, prototype, and API evidence; upload conversation images or captured Figma states to Feishu with `lark-cli` by default; require Source Gate #3 PASS.
2. `requirement-clarification`: compare sources and pause on Clarification Gate #4 until all consequential `CL-xx` decisions are confirmed.
3. `user-flow-generator`.
4. `state-machine-generator`.
5. `sequence-diagram-generator`.
6. Return here to assemble the Plan Draft.
7. `review-package-publisher`: update the Feishu document, pin its Revision, explicitly export the local plan, create sync metadata, and run Reviewability Gate #5.

If any input is missing, paths disagree, a gate blocks, or new ambiguity appears, return to the owning artifact in the same version and pause. Do not collapse the pipeline into an untraceable single pass.

## Assemble a self-explanatory plan

Read `prompt.md` for the exact contract and the example when helpful.

1. Start with a Review guide that identifies audience, status, Feishu evidence location, and requested review outcome.
2. Explain the business problem, target users, scenarios, terms, goals, scope, non-goals, and acceptance outcomes without relying on the source chat.
3. Include a source inventory and Prototype Catalog with individually linked `PT-xx`, page/state names, preview/block links, original locators, and what each image proves.
4. Define a semantic page/component responsibility tree without prescribing framework source files.
5. Inline every review-relevant `UF-xx`, `SM-xx`, and `SQ-xx` into the Plan. For each ID include its title, Mermaid source, a plain-language summary, and evidence/decision IDs; do not replace content with a path or “see `*.md`”.
6. Describe validation, visible feedback, recovery, permissions, concurrency, cancellation, refresh behavior, and confirmed contract gaps.
7. Split work into dependency-ordered `FE-xx` tasks with inputs, deliverables, dependencies, and testable acceptance checks.
8. Include confirmed decisions, unresolved issues, and a traceability matrix linking `PRD`, `PT`, `API`, `CL`, `UF`, `SM`, `SQ`, and `FE` IDs.

Treat visual-artifact IDs as navigation, not plain labels. In prose, lists, and table cells, link every `PT-xx`, `UF-xx`, `SM-xx`, and `SQ-xx` occurrence to its exact image, diagram, or canonical section block. When a cell mentions several IDs, link each ID separately. Canonical destination headings and IDs rendered inside a diagram are exempt. Preserve the original Figma/source URL separately from the Feishu Review target.

## Preserve evidence and review work

- Developer-confirmed decisions have highest priority.
- Never replace durable evidence with “see the screenshot above” or a chat reference.
- Treat `user-flow.md`, `state-machine.md`, and `sequence-diagram.md` as composition sources, not reviewer-facing substitutes. A reviewer reading only the Plan must see the actual diagrams and their explanations.
- Do not infer components, endpoints, permissions, states, or error behavior without evidence.
- Preserve reviewer notes, approved decisions, and manual overrides during same-version regeneration.
- Plan generation may write a Draft locally; only the publisher may replace it with an exported fixed Feishu Revision after drift checks.

## Validate and publish

Before publisher handoff, verify prerequisites share the same confirmed context, both upstream gates pass, every in-scope goal has a flow, every async interaction has states, every API appears in a sequence, every failure has visible handling, and every task has an acceptance condition. Also verify every `UF-xx`, `SM-xx`, and `SQ-xx` defined by the source artifacts appears in its Plan section with an inline Mermaid diagram. Missing or file-reference-only diagram content blocks publication.

Set Draft status to `Ready for Publication` only when no source or clarification blocker remains. Final status becomes `Ready for Technical Review` after publication/export and `Ready for Development` only after approved Technical Review against the synchronized Revision.
