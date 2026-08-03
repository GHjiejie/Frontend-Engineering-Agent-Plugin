---
name: frontend-analysis
description: Understand an existing frontend repository, refresh its persistent project and domain memory, analyze a new or changed requirement, reconcile API/UI/interaction inputs, identify reusable capabilities and risks, and create or update a durable Feature Entity and Feature Contract. Use when onboarding a frontend codebase, receiving a feature request, clarifying requirements, assessing change impact, or preparing work for frontend technical design.
---

# Frontend Analysis

Create an evidence-backed Feature Contract before design or implementation. Treat repository facts and user-provided requirements as authoritative; treat memory files as a cache that may be stale.

## Workflow

1. Read repository instructions, especially `AGENTS.md`, then inspect the worktree without changing it.
2. Load `docs/frontend-ai/project-memory/`, `domain-memory/`, `decisions/`, and the feature registry when present.
3. If memory is absent, initialize it non-destructively with `python3 <plugin-root>/scripts/frontend_ai.py init --root <repository-root>`. Never overwrite existing memory merely to normalize it.
4. Verify memory against `package.json`, lockfiles, TypeScript config, build config, routing, state, API, component, test, README, and recent Git history. Mark contradictions explicitly and update only facts supported by the repository.
5. Parse the request into goals, actors, in-scope and out-of-scope behavior, UI states, API behavior, interactions, acceptance criteria, constraints, and open questions.
6. Inspect provided API documents, designs, screenshots, or links when available. Distinguish observed facts from inference.
7. Search the project index and source for reusable routes, components, composables, stores, services, patterns, and tests.
8. Create the feature with `python3 <plugin-root>/scripts/frontend_ai.py new-feature <feature-id> --root <repository-root> --domain <domain> --title <title>` when it does not already exist.
9. Write `feature.yaml`, `contract.yaml`, and `risk-report.md` according to [references/analysis-artifacts.md](references/analysis-artifacts.md). Preserve feature history when updating an existing feature.
10. Refresh `project-context.yaml`, `project-index.json`, `architecture-map.yaml`, domain memory, and `memory-index.json` only where the analysis discovered durable facts.
11. Run `python3 <plugin-root>/scripts/frontend_ai.py validate --root <repository-root> --feature <feature-id> --phase analysis`.

## Contract gate

Do not hand off to design until all of the following are true:

- Every requirement is mapped to at least one acceptance criterion.
- UI, API, interaction, error, loading, empty, permission, and boundary behavior are either specified or explicitly not applicable.
- Reuse candidates and affected areas cite repository evidence.
- Assumptions and open questions are separated.
- Blocking ambiguity is resolved or the orchestrator state is recorded as `BLOCKED` or `NEED_HUMAN_REVIEW`.
- `contract.yaml` has `status: READY`, and `feature.yaml` records `contractReady: true` while the lifecycle remains `ANALYZING`.

## Safety

- Do not implement product code in this skill.
- Do not invent endpoints, design details, business rules, or architectural conventions.
- Preserve unrelated user changes and never use destructive Git commands.
- Do not commit, push, or open a pull request unless the user separately requests it.

## Handoff

Report the feature id, contract path, material risks, unresolved decisions, and the evidence used to refresh memory. Recommend `frontend-design` only after the contract gate passes.
