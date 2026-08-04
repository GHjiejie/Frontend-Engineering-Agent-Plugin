---
name: generate-frontend-spec
description: Run an end-to-end frontend specification pipeline from product requirements, project context, API contracts, and UI references. Use when Codex must turn a PRD, feature request, Figma design, screenshot, HTML prototype, OpenAPI or Swagger definition, or a combination of these inputs into a traceable frontend development specification without writing application code.
---

# Generate Frontend Spec

Produce a reviewable specification through explicit intermediate artifacts and approval gates.

Resolve resource paths in this file from the directory containing this `SKILL.md`. Use the resolved absolute path when invoking a bundled script from another working directory.

## Start the run

1. Read `../../references/artifact-contract.md`.
2. Identify the feature scope and every user-supplied source. Do not silently widen the scope.
3. Run `python3 ../../scripts/init_frontend_spec.py --output <workspace>/frontend-spec --feature-id <feature-id>` when the artifact tree does not exist.
4. Reuse an existing artifact tree. Never overwrite manual decisions or history during initialization.

## Execute the pipeline

Run these stages in order. Before each stage, read and follow the referenced sibling skill:

1. `../project-context-loader/SKILL.md`
2. `../requirement-analyzer/SKILL.md`
3. `../requirement-clarifier/SKILL.md`
4. `../api-analyzer/SKILL.md`
5. `../ui-parser/SKILL.md`
6. `../interaction-designer/SKILL.md`
7. `../flow-generator/SKILL.md`
8. `../frontend-spec-generator/SKILL.md`

Invoke `../change-tracker/SKILL.md` before changing any previously generated or manually overridden section.

Update `frontend-spec/pipeline-state.json` after each stage with `pending`, `in_progress`, `blocked`, or `complete`. Include artifact paths and blockers.

## Enforce quality gates

- Continue through missing optional evidence by recording an explicit gap and its impact.
- Pause after requirement clarification when a blocking product decision remains. Ask only the minimum grouped questions needed to proceed.
- Treat a developer answer as approved only when it is recorded in `requirement/decision-log.md`.
- Do not mark API or UI mappings complete when an essential operation or control is inferred without evidence.
- Do not mark the final document `ready_for_implementation` while blocking questions, unmapped required interactions, or unresolved contract conflicts remain.
- Label supported inferences as assumptions with owner and validation status. Never present guesses as source facts.

## Finish

1. Run `python3 ../../scripts/validate_frontend_spec.py <workspace>/frontend-spec --require-complete`.
2. If validation fails, repair deterministic issues and report genuine product or contract blockers.
3. Return the final document path, readiness status, unresolved items, and the next required human action.

Do not generate Vue, React, API service, store, or test implementation code. Those are deliberate future pipeline stages.
