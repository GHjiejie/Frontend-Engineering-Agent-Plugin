---
name: frontend-design
description: Convert a ready frontend Feature Contract into an evidence-backed implementation design covering pages, components, API adapters, state ownership, interactions, tests, rollout, rollback, and file-level changes while honoring project memory and architecture decisions. Use after frontend analysis, when planning a frontend feature, evaluating implementation approaches, or updating a technical design before code changes.
---

# Frontend Design

Produce an executable design without modifying product code.

## Preconditions

1. Read repository instructions and inspect the worktree.
2. Load the target `feature.yaml`, `contract.yaml`, project memory, domain memory, and relevant ADRs.
3. Require `contract.yaml` to have `status: READY` and `feature.yaml` to have `contractReady: true`.
4. If the contract is incomplete or contradicts repository facts, stop the design, record `BLOCKED` or `CONFLICT`, and return to `frontend-analysis`.

## Workflow

1. Trace each requirement and acceptance criterion to current routes, components, APIs, stores, composables, styles, and tests.
2. Compare viable approaches. Prefer existing project patterns and the smallest coherent change surface.
3. Define page boundaries, component responsibilities, data flow, state ownership, API adaptation, validation, error handling, accessibility, responsive behavior, and observability.
4. Decide which state is local, composable-owned, store-owned, URL-derived, or server-derived. Avoid persistent global state for short-lived page state unless project decisions require it.
5. Specify file-level operations as create, modify, move, or delete. Identify user-owned or high-conflict files.
6. Map each acceptance criterion to automated or manual verification and include failure-path tests.
7. Define rollout, rollback, compatibility, data migration, and documentation or memory updates.
8. Write `implementation.yaml` according to [references/implementation-plan.md](references/implementation-plan.md).
9. Update `feature.yaml` to `status: DESIGNED`, `orchestratorState: DESIGN_READY`, and `implementationReady: true` only after the design gate passes.
10. Run `python3 <plugin-root>/scripts/frontend_ai.py validate --root <repository-root> --feature <feature-id> --phase design`.

## Design gate

- Every contract requirement and acceptance criterion has traceability.
- Every planned file change has a reason and ownership boundary.
- API, state, component, interaction, accessibility, responsive, error, and test designs are explicit.
- Decisions align with project memory and ADRs, or a new decision is proposed with consequences.
- Risks, dependencies, rollout, and rollback are actionable.
- No unresolved issue could materially change the implementation approach.

## Safety and handoff

Do not edit application code, install dependencies, or mutate external systems. Report the chosen approach, rejected alternatives, impacted files, risks, verification strategy, and any human approvals needed. Recommend `frontend-implementation` only after the design gate passes.
