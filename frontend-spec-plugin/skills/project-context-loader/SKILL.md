---
name: project-context-loader
description: Capture evidence-backed frontend project constraints and structure. Use when Codex must inspect a target frontend repository before specifying a feature, including framework, language, package manager, UI system, state management, styling, routing, build tools, API conventions, reusable components, tests, and repository instructions.
---

# Project Context Loader

Create `frontend-spec/context/project-context.json` as the implementation constraint baseline.

## Collect evidence

1. Read `../../references/artifact-contract.md` and `../../schemas/project-context.schema.json`.
2. Inspect only the target project placed in scope by the user.
3. Prefer authoritative sources: repository instructions, package manifest and lockfile, build configuration, TypeScript configuration, source entry points, router and state setup, API layer, component directories, and test configuration.
4. Exclude dependencies, build output, generated code, caches, and unrelated packages.
5. Record each conclusion with its source path. Use `unknown` when evidence is absent or conflicting.

## Capture

- Framework, language, package manager, runtime and build tool
- UI component system, styling system, state management and router
- API client, error-handling and authentication conventions
- Relevant reusable components and feature-local structure
- Test tools, commands, formatting and lint constraints
- Repository instructions and feature-relevant architectural rules

Do not read the entire repository indiscriminately. Search for the minimum evidence needed for the current feature.

## Complete the stage

Validate the JSON shape, add conflicts or unknowns to `gaps`, and update the `project-context` stage in `pipeline-state.json`. Do not recommend a stack that contradicts repository evidence.
