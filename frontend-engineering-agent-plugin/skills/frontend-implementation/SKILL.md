---
name: frontend-implementation
description: Execute a ready frontend Implementation Plan through a proposal-first patch workflow that preserves manual user changes, produces a reviewable patch and diff before mutation, waits for explicit human patch approval, applies only the approved change, runs relevant verification, and generates a Change Entity proposal. Use when an approved Change Contract and ready plan exist and the user asks to implement the frontend feature, bug fix, or refactor.
---

# Frontend Implementation

Follow `Plan -> Patch Proposal -> Human Diff Review -> Apply -> Test -> Change Entity Proposal`. Never edit product files before the Patch Approval Gate.

## Preconditions

1. Load task context, approved Change Contract, Implementation Plan, Constitution, relevant entities, repository instructions, and current Git status.
2. Require analysis approval `APPROVED` and plan status `READY`.
3. Reconcile unexplained manual changes. Preserve them or enter `CONFLICT`; never assume they are disposable.
4. Move the orchestrator to `IMPLEMENTATION`.

## Proposal phase

1. Derive the exact patch from the plan without applying it.
2. Write `runtime/patch-proposal.yaml` and `runtime/patch-proposal.diff` using [references/patch-and-change.md](references/patch-and-change.md).
3. Review the proposed diff against contract, plan, user edits, Constitution, and scope. Mark the proposal `PENDING_APPROVAL`.
4. Record pending patch approval, move to `WAITING_HUMAN` with gate `patch`, validate phase `patch-proposal`, and stop.
5. Ask the human to approve or reject the exact patch. Do not infer approval from the original implementation request.

## Apply phase

Continue only after an explicit human approval has been recorded through the runtime CLI.

1. Move back to `IMPLEMENTATION`, re-check that the worktree still matches the patch base, and regenerate the proposal if it drifted.
2. Apply only the approved patch. Use patch-aware editing and never overwrite whole user-owned files unnecessarily.
3. Inspect the actual diff. If it differs materially from the approved patch, stop and request approval again.
4. Run focused tests, then relevant typecheck, lint, unit/component/integration/e2e checks and build.
5. Set patch status `APPLIED`; write `runtime/change-entity-proposal.yaml` and `reports/<task-id>-change-log.md`.
6. Do not persist the proposed Change Entity or other memory updates yet. Move to `REVIEW` and validate phase `implementation`.

## Safety and handoff

Do not commit, push, deploy, or update durable memory unless separately authorized. Report the approved patch, actual diff, checks, deviations, user changes preserved, and the Change Entity proposal.
