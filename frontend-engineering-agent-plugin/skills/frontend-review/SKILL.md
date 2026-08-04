---
name: frontend-review
description: Review an applied frontend patch against its Change Contract, task context, bug or feature history, implementation plan, project Constitution, regression surface, tests, and actual diff; produce a severity-ranked report and a governed Memory Update Proposal that is persisted only after explicit human confirmation. Use for final validation, pre-merge review, bug-fix verification, regression assessment, architecture compliance, or memory synchronization after a frontend change.
---

# Frontend Review

Establish release readiness and propose knowledge changes. Review first; do not silently fix defects unless the user separately requests implementation.

## Preconditions

1. Require an applied, human-approved patch and load all runtime artifacts, current diff, repository rules, Constitution, entities, tests, and source inputs.
2. Require orchestrator state `REVIEW`. If the applied diff no longer matches the approved proposal, enter `CONFLICT`.

## Review

1. Verify each feature requirement, bug reproduction/root cause, or refactor invariant against evidence.
2. Check UI, API, interaction, loading, error, empty, permission, accessibility, responsive, security, performance, and compatibility behavior where applicable.
3. Assess regression risk using related Feature, Bug, Change, Decision, file, route, and symbol knowledge.
4. Check dependency direction, component reuse, API layer, state lifetime, tokens, and every Constitution rule.
5. Run or inspect relevant typecheck, lint, tests, build, and targeted UI verification. Distinguish pass, fail, and not run.
6. Write `reports/<task-id>-review.md` using [references/review-and-memory-sync.md](references/review-and-memory-sync.md). Rank findings `P0` through `P3` with exact evidence.

## Memory governance

1. Convert engineering meaning—not raw file churn—into `runtime/memory-update-proposal.yaml`.
2. Include the proposed Change Entity and any Feature, Bug, Decision, Project, Domain, index, confidence, or verification changes.
3. Move to `MEMORY_UPDATE`, record pending memory approval, then move to `WAITING_HUMAN` with gate `memory`.
4. Validate phase `review`, stop, and ask the human to approve or reject the memory proposal.
5. After explicit approval, move back to `MEMORY_UPDATE`, persist only approved items, update the knowledge index, mark the proposal `APPLIED`, validate phase `memory-update`, and move to `COMPLETED`.

## Outcome rules

- `PASS`: no open P0-P2 finding and every required criterion has evidence.
- `FAIL`: confirmed defects block completion; route code fixes to implementation and require a new patch proposal.
- `BLOCKED`: required evidence or environment is unavailable.
- `WAITING_HUMAN`: intent or governance requires human judgment.

Lead the handoff with findings, then outcome, verification, regressions, Constitution compliance, and the exact memory decision requested.
