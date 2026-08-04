---
name: generate-frontend-spec
description: Collect required inputs, confirm the frontend-spec output directory, generate or resume an isolated frontend specification, and when requested implement a node-specific Figma design in Neo Cloud dashboard-ui with visual validation. Use whenever a user asks to add, create, build, design, plan, continue, implement, restore, or update a frontend feature—including “增加功能”, “新增页面”, “继续这个需求”, “开发前端功能”, or “像素级还原”—even when required inputs are still missing. Never scan the surrounding project for background.
---

# Generate Frontend Spec

Produce a reviewable specification through explicit intermediate artifacts and approval gates, then either stop at the specification or continue into an approved dashboard UI implementation and visual-validation loop.

Resolve resource paths in this file from the directory containing this `SKILL.md`. Use the resolved absolute path when invoking a bundled script from another working directory.

## Mandatory input preflight

Run this gate before reading any user workspace file, invoking a workspace tool, listing existing specifications, initializing artifacts, proposing an implementation, or analyzing the feature.

Classify each required input independently:

1. **Requirement** — a PRD, product document, issue, or pasted requirement with enough behavior to identify the user or actor, action or trigger, and expected outcome. A feature title or one-line command such as “增加微信绑定和解绑功能” is not a provided requirement.
2. **Prototype** — Figma, Axure, screenshot, HTML prototype, wireframe, or an explicit written UI description containing actual page structure, controls, or interaction. A project or page name alone is not a provided prototype.
3. **API** — OpenAPI, Swagger, protobuf, endpoint documentation, a typed frontend client selected by the user, or an explicit statement that no API exists yet. A vague statement that backend support exists is not a provided API contract.
4. **Output location** — the exact directory in which `frontend-spec/` will live. The current workspace, repository root, terminal directory, or a prior run is not implicit authorization.

Use exactly one state for each source category:

- `provided`: the current conversation contains or points to usable evidence.
- `explicitly_unavailable`: the user has explicitly said the input does not exist or is not available. Preserve this as a gap or blocker.
- `missing`: neither evidence nor an explicit unavailable statement exists.

For output location, use exactly one state:

- `confirmed`: the user explicitly requested creation at an exact absolute `frontend-spec` path, or explicitly confirmed an exact absolute path that the assistant displayed.
- `proposed`: the user named a relative path, a parent directory, “项目根目录”, or “当前目录”, but the assistant has not yet displayed and received confirmation of the resolved absolute `frontend-spec` path.
- `missing`: no location preference exists.

If any source category is `missing`, or output location is not `confirmed`:

- Stop before all other workflow steps.
- Ask for every missing category together in one concise response, using the user's language.
- Resolve a proposed parent directory by appending `frontend-spec`; preserve an exact path whose basename is already `frontend-spec`. Display the resolved absolute path and ask the user to confirm it.
- When location is missing, propose `<current-workspace>/frontend-spec` as a suggestion only and ask the user to confirm it or provide another parent directory. Never treat the suggestion as approval.
- State that the plugin first generates a frontend specification and, for a Figma implementation request, continues only after a restoration-brief approval; it will not browse the project for missing information.
- Tell the user they may reply that an item is unavailable; do not assume unavailability from silence.
- Do not create files, inspect the named project or directory, initialize the pipeline, analyze requirements, propose flows, or produce a specification in the same response.

Use this response pattern and omit categories already provided:

```text
我会先为这个功能生成前端开发规格，不会扫描项目代码；如果这是基于节点级 Figma 的开发请求，规格就绪后我会先提交还原说明，经你确认后再实现并进行设计与回归视觉测试。开始前还需要：
1. 需求/PRD：…
2. 原型：…
3. 接口：…
4. 输出位置：请确认在哪个目录下创建 `frontend-spec`。建议路径：`<当前工作区绝对路径>/frontend-spec`。请回复“确认此路径”或提供其他父目录/完整路径。
如果需求、原型或接口暂时没有，请直接说明“暂无”，我会把它记录为缺口；输出位置必须确认。
```

Re-run the preflight after every user reply. Continue only when all three source categories are either `provided` or `explicitly_unavailable` and the exact absolute output location is `confirmed`. Store that path as `<spec-root>`. Location confirmation authorizes only plugin artifacts under `<spec-root>`; it does not authorize scanning the parent directory.

## Select the delivery mode

After the mandatory input preflight passes, select exactly one delivery mode and preserve it for the feature run:

- **`spec_only`** — use only when the user explicitly asks for a specification, plan, analysis, or documentation without application-code changes, or explicitly says not to implement.
- **`implement_and_validate`** — use when the user asks to add, create, build, develop, implement, refactor, restore, visually align, or pixel-match a dashboard UI feature and supplies a node-specific Figma prototype. This is the default for action requests such as “新增这个功能” after a usable Figma node is supplied; do not silently reinterpret them as documentation-only work.

If the request remains genuinely ambiguous between documentation and implementation, ask one concise question naming the two modes and stop.

If the user requests implementation but the prototype is explicitly unavailable, is not Figma, or does not identify a Figma node, report that `implement_and_validate` is blocked. Ask for a node-specific Figma URL or explicit permission to continue as `spec_only`; do not silently downgrade the request.

For `implement_and_validate`, also require:

1. The exact dashboard page, module, route, or visual scenario to change.
2. The exact `dashboard-ui` frontend root or another exact frontend code path the user authorizes.

If either is missing or ambiguous, ask for both missing values together and stop. Do not list or scan the repository to discover them. The confirmed `<spec-root>` controls specification artifacts only and does not authorize application-code access.

## Select the feature run

1. Read `../../references/artifact-contract.md`.
2. Confirm that the mandatory input preflight passed. Identify the feature scope and every user-supplied source without widening the scope.
3. Run `python3 ../../scripts/manage_frontend_specs.py --output <spec-root> list`. This reads only plugin-owned artifacts; do not enumerate the parent directory.
4. Select exactly one mode:
   - **Resume** only when the user explicitly names an existing feature or the current conversation unambiguously continues it. Run `... resume --feature-id <feature-id>`.
   - **Create** only when the user explicitly says this is a new feature and its normalized lowercase hyphen-case ID is not registered. Action phrases such as “新增”, “增加”, “新建”, and “add a new” explicitly indicate a new feature. Run `... create --feature-id <feature-id> --title <title>`.
   - **Adopt legacy** when `list` reports `LEGACY`. Explain that the existing root-level artifacts belong to the reported feature. Ask whether to continue that feature or register it before creating another one. After explicit confirmation, run `... adopt-legacy --feature-id <reported-feature-id> --title <title>`.
5. If intent is ambiguous, show the known feature IDs and titles, ask whether to resume one or create a new feature, and stop. Never infer that a new request updates an existing feature merely because it uses the same workspace.
6. Store the command's `Feature root` output as `<feature-root>`. Every downstream stage must read and write only inside that directory.

Do not initialize, modify, or reuse any feature artifacts before this selection is resolved. Never merge independent features into one feature root.

## Enforce the input boundary

- Use only the preflight-approved product requirements, UI prototypes, and API contracts by default.
- Do not enumerate or scan the project root for background. Do not read package manifests, build configuration, README files, directory trees, backend code, infrastructure, or unrelated source files merely because they exist. After `implement_and_validate` is selected, the restoration skill may read the authorized frontend root's exact package manifest and directly relevant test/build configuration solely to identify and run required frontend checks.
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

## Validate the specification

1. Run `python3 ../../scripts/validate_frontend_spec.py <feature-root> --require-complete`.
2. If validation fails, repair deterministic issues and report genuine product or contract blockers.
3. If the selected mode is `spec_only`, return the final document path, readiness status, unresolved items, and the next required human action. Stop without editing application code.

## Implement and validate the dashboard UI

Run this section only when the selected mode is `implement_and_validate` and the specification is `ready_for_implementation`.

1. Present the final specification's pages, interactions, API mappings, assumptions, and non-blocking gaps. Ask the developer to approve it for implementation and stop; validator success alone is not human approval.
2. After approval, invoke `../change-tracker/SKILL.md`, record the approval in `requirement/decision-log.md`, and rerun specification validation before implementation.
3. Read and follow `../dashboard-ui-figma-restore/SKILL.md`.
4. Pass it the active `<feature-root>`, node-specific Figma URL, exact target page/route/scenario, and developer-approved frontend root.
5. Complete its Figma and scoped-code preflight.
6. Generate `<feature-root>/implementation/restoration-brief.md`, present the brief, and stop until the developer explicitly approves it. A general request to build the feature is not approval of an unseen brief.
7. After approval, implement only inside the authorized frontend scope and run the skill's full design plus regression visual-validation loop.
8. Record results in `<feature-root>/implementation/visual-validation.md` and report implementation files, design evidence, tests, visual results, deviations, blockers, and any baseline candidate awaiting approval.

Never claim the feature is delivered merely because the specification is complete. In `implement_and_validate` mode, completion requires the approved implementation plus successful design and regression visual checks. Report an external blocker as an incomplete, blocked delivery.
