---
name: frontend-implementation
description: Safely implement an approved frontend feature design in an existing repository, preserving user changes while modifying Vue, React, TypeScript, JavaScript, routing, components, API adapters, state, styles, and tests; verify the implementation, record a change log, and update durable project memory. Use when a Feature Contract and implementation plan are ready and the user asks to build, change, or fix the planned frontend feature.
---

# Frontend Implementation

Execute the approved plan and keep code, feature artifacts, and memory synchronized.

## Preconditions

1. Read repository instructions and `git status` before editing.
2. Load `feature.yaml`, `contract.yaml`, `implementation.yaml`, project memory, domain memory, and relevant ADRs.
3. Require `contract.status: READY`, `implementation.status: READY`, `contractReady: true`, and `implementationReady: true`.
4. Compare planned files with current code. If the plan is stale or overlaps unexplained user changes, record `CONFLICT` and stop or redesign the affected step.
5. Do not start from a dirty file by assuming its changes are disposable.

## Workflow

1. Set the feature lifecycle to `IMPLEMENTING` and orchestrator state to `IMPLEMENTING` while preserving history.
2. Implement steps in dependency order, using existing project abstractions, tokens, naming, linting, test, and accessibility conventions.
3. Keep API transport in the established API layer and keep state at the narrowest correct lifetime.
4. Add or update tests alongside behavior. Cover success, failure, loading, empty, permission, validation, and boundary paths that the contract requires.
5. Run focused checks after each coherent step, then the repository's relevant typecheck, lint, unit, component, integration, end-to-end, and build commands.
6. Review the actual diff against `implementation.yaml` and the contract. Explain any deviation and update the plan if the deviation is accepted.
7. Write `docs/frontend-ai/reports/<feature-id>-change-log.md` according to [references/implementation-records.md](references/implementation-records.md).
8. Update durable memory only with verified facts: project index, architecture map, feature registry, ADRs, domain memory, and memory index. Do not mark the feature `RELEASED` or append a release evolution event before review passes.
9. Set the orchestrator state to `VERIFYING` and keep feature status `IMPLEMENTING` for review.
10. Run `python3 <plugin-root>/scripts/frontend_ai.py validate --root <repository-root> --feature <feature-id> --phase implementation`.

## Safety

- Never discard, reset, or overwrite unrelated changes.
- Do not widen scope merely because nearby cleanup is attractive.
- Do not change architecture decisions silently; create or propose an ADR.
- Do not commit, push, deploy, or communicate externally unless the user explicitly requests that action.
- If required verification cannot run, report the exact command, failure, and residual risk.

## Handoff

Report implemented acceptance criteria, changed files, deviations, checks run with results, memory updates, and residual risks. Hand the feature to `frontend-review`; do not claim release before that review passes.
