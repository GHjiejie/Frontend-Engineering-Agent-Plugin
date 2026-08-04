---
name: frontend-design
description: Convert a human-approved frontend Change Contract for a feature, bug, or refactor into a traceable Implementation Plan that honors task context, project constitution, historical decisions, user edits, architecture, component reuse, API and state boundaries, tests, rollout, and rollback. Use only after the analysis approval gate is explicitly approved and before producing or applying any code patch.
---

# Frontend Design

Design the smallest coherent implementation that satisfies the approved contract. Do not modify product code.

## Preconditions

1. Read repository instructions, `runtime/task-context.yaml`, `runtime/change-contract.yaml`, and `runtime/approvals/analysis.yaml`.
2. Require approval `APPROVED`. Never treat silence, a ready contract, or a prior implementation request as approval.
3. Re-check the current worktree against the approved evidence. If code or requirements changed materially, enter `CONFLICT` and return to analysis.
4. Move the orchestrator from `APPROVAL_REQUIRED` to `DESIGN` through the runtime CLI.

## Workflow

1. Trace every contract item to files, symbols, entities, steps, and verification.
2. Read `memory/project/constitution.yaml`, relevant ADRs, Feature/Bug/Change history, project index relations, and current implementation patterns.
3. Compare viable approaches. Prefer reuse, narrow state lifetime, established API layers, design tokens, compatibility, and reversible change.
4. Define routes/pages, components, API mapping, state ownership, UI states, interactions, validation, error handling, accessibility, performance, security, and observability.
5. Identify user-modified or high-conflict files and prescribe preservation or reconciliation.
6. Specify file operations, dependency order, test coverage, rollout, rollback, and proposed knowledge updates.
7. Write `runtime/implementation-plan.yaml` according to [references/implementation-plan.md](references/implementation-plan.md).
8. Set the plan to `READY` only when traceability and risk handling are complete, then validate phase `design`.

## Design gate

- Every requirement or bug condition maps to implementation steps and verification.
- Every file operation has a reason and an ownership boundary.
- The plan obeys Constitution and Decisions or proposes an explicit new Decision.
- No unresolved issue could materially change the approach.
- Patch scope, diff review method, and rollback are executable.

## Handoff

Report the selected approach, rejected alternatives, files, risks, tests, rollback, and any required Decision proposal. Hand off to `frontend-implementation`; approval of the design does not waive the later Patch Approval Gate.
