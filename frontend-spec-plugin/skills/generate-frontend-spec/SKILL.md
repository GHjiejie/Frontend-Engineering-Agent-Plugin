---
name: generate-frontend-spec
description: Collect required inputs and generate or resume an isolated end-to-end frontend development specification. Use whenever a user asks to add, create, build, design, plan, continue, or update a frontend feature—including phrases such as “增加功能”, “新增页面”, “继续这个需求”, “开发前端功能”, or “现在要做”—even when no PRD, prototype, or API has been provided yet. First ask for every missing requirement or PRD, UI prototype, and API contract; then explicitly select an existing feature run or create a separate one. Do not use this skill to implement application code or scan the surrounding project.
---

# Generate Frontend Spec

Produce a reviewable specification through explicit intermediate artifacts and approval gates.

Resolve resource paths in this file from the directory containing this `SKILL.md`. Use the resolved absolute path when invoking a bundled script from another working directory.

## Mandatory input preflight

Run this gate before reading any user workspace file, invoking a workspace tool, initializing artifacts, proposing an implementation, or analyzing the feature.

Classify each required input independently:

1. **Requirement** — a PRD, product document, issue, or pasted requirement with enough behavior to identify the user or actor, action or trigger, and expected outcome. A feature title or one-line command such as “增加微信绑定和解绑功能” is not a provided requirement.
2. **Prototype** — Figma, Axure, screenshot, HTML prototype, wireframe, or an explicit written UI description containing actual page structure, controls, or interaction. A project or page name alone is not a provided prototype.
3. **API** — OpenAPI, Swagger, protobuf, endpoint documentation, a typed frontend client selected by the user, or an explicit statement that no API exists yet. A vague statement that backend support exists is not a provided API contract.

Use exactly one state for each category:

- `provided`: the current conversation contains or points to usable evidence.
- `explicitly_unavailable`: the user has explicitly said the input does not exist or is not available. Preserve this as a gap or blocker.
- `missing`: neither evidence nor an explicit unavailable statement exists.

If any category is `missing`:

- Stop before all other workflow steps.
- Ask for every missing category together in one concise response, using the user's language.
- State that the plugin generates a frontend specification and will not browse the project for the missing information.
- Tell the user they may reply that an item is unavailable; do not assume unavailability from silence.
- Do not create files, inspect the named project or directory, initialize the pipeline, analyze requirements, propose flows, or produce a specification in the same response.

Use this response pattern and omit categories already provided:

```text
我会为这个功能生成前端开发规格，不会扫描项目代码。开始前还需要：
1. 需求/PRD：…
2. 原型：…
3. 接口：…
如果某项暂时没有，请直接说明“暂无”，我会把它记录为缺口。
```

Re-run the preflight after every user reply. Continue only when all three categories are either `provided` or `explicitly_unavailable`.

## Select the feature run

1. Read `../../references/artifact-contract.md`.
2. Confirm that the mandatory input preflight passed. Identify the feature scope and every user-supplied source without widening the scope.
3. Run `python3 ../../scripts/manage_frontend_specs.py --output <workspace>/frontend-spec list`. This reads only plugin-owned artifacts; do not enumerate the workspace.
4. Select exactly one mode:
   - **Resume** only when the user explicitly names an existing feature or the current conversation unambiguously continues it. Run `... resume --feature-id <feature-id>`.
   - **Create** only when the user explicitly says this is a new feature and its normalized lowercase hyphen-case ID is not registered. Run `... create --feature-id <feature-id> --title <title>`.
   - **Adopt legacy** when `list` reports `LEGACY`. Explain that the existing root-level artifacts belong to the reported feature. Ask whether to continue that feature or register it before creating another one. After explicit confirmation, run `... adopt-legacy --feature-id <reported-feature-id> --title <title>`.
5. If intent is ambiguous, show the known feature IDs and titles, ask whether to resume one or create a new feature, and stop. Never infer that a new request updates an existing feature merely because it uses the same workspace.
6. Store the command's `Feature root` output as `<feature-root>`. Every downstream stage must read and write only inside that directory.

Do not initialize, modify, or reuse any feature artifacts before this selection is resolved. Never merge independent features into one feature root.

## Enforce the input boundary

- Use only the preflight-approved product requirements, UI prototypes, and API contracts by default.
- Do not enumerate or scan the project root for background. Do not read package manifests, build configuration, README files, directory trees, backend code, infrastructure, or unrelated source files merely because they exist.
- Treat the existence of a repository as no permission to browse it.
- Inspect code only when the user explicitly supplies or names a path. The path must be frontend code or another exact path selected by the user.
- Within an allowed frontend path, read only the named files and the minimum direct frontend dependencies needed to understand the requested behavior. Do not expand into unrelated modules.
- If required information is absent from the three primary inputs, record a gap or ask a focused question instead of searching the project for an answer.

## Execute the pipeline

Run these stages in order. Before each stage, read and follow the referenced sibling skill:

1. `../requirement-analyzer/SKILL.md`
2. `../requirement-clarifier/SKILL.md`
3. `../ui-parser/SKILL.md`
4. `../api-analyzer/SKILL.md`
5. `../interaction-designer/SKILL.md`
6. `../flow-generator/SKILL.md`
7. `../frontend-spec-generator/SKILL.md`

Invoke `../change-tracker/SKILL.md` before changing any previously generated or manually overridden section.

Update `<feature-root>/pipeline-state.json` after each stage with `pending`, `in_progress`, `blocked`, or `complete`. Include artifact paths and blockers.

## Enforce quality gates

- After preflight passes, record inputs explicitly marked unavailable as gaps or blockers with their impact.
- Pause after requirement clarification when a blocking product decision remains. Ask only the minimum grouped questions needed to proceed.
- Treat a developer answer as approved only when it is recorded in `requirement/decision-log.md`.
- Do not mark API or UI mappings complete when an essential operation or control is inferred without evidence.
- Do not mark the final document `ready_for_implementation` while blocking questions, unmapped required interactions, or unresolved contract conflicts remain.
- Label supported inferences as assumptions with owner and validation status. Never present guesses as source facts.

## Finish

1. Run `python3 ../../scripts/validate_frontend_spec.py <feature-root> --require-complete`.
2. If validation fails, repair deterministic issues and report genuine product or contract blockers.
3. Return the final document path, readiness status, unresolved items, and the next required human action.

Do not generate Vue, React, API service, store, or test implementation code. Those are deliberate future pipeline stages.
