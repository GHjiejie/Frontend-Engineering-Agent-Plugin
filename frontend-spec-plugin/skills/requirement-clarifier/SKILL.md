---
name: requirement-clarifier
description: Detect consequential gaps in analyzed frontend requirements, ask focused product questions, and preserve approved answers as durable decisions. Use when a PRD is incomplete, ambiguous, contradictory, or lacks behavior for validation, permissions, confirmations, failures, loading, empty states, refreshes, concurrency, or navigation.
---

# Requirement Clarifier

Produce `frontend-spec/requirement/question-list.md` and maintain `frontend-spec/requirement/decision-log.md`.

## Classify gaps

1. Read `../../references/artifact-contract.md` and the current requirement analysis.
2. Classify every gap that changes visible UI, user action, validation, confirmation, loading, success, failure, empty state, navigation, refresh, permission, retry, cancellation, or recovery as `blocking`.
3. Merge duplicates and group related questions by user flow.
4. For every question, include the affected requirement IDs, why the answer matters, options when genuinely known, and a recommended default only when evidence supports it.

## Ask and record

- Ask blocking questions before downstream binding.
- Stop the turn after asking blocking questions. Do not continue into UI/API binding or interaction design in the same turn.
- Never choose a user-visible behavior on the developer's behalf. A recommendation is an option, not an approved decision.
- Record an assumption only for implementation-internal details that cannot change anything a user sees, does, or recovers from.
- Append confirmed answers to `decision-log.md` with decision ID, date, owner, status, rationale, affected IDs, and superseded decision when applicable.
- Propagate confirmed decisions back into the requirement analysis. Keep the original question traceable.

Mark the stage `blocked` while any user-visible question is unanswered. Mark it `complete` only when every user-visible behavior is sourced or explicitly decided by the developer. Important implementation-internal items may stay visible in the final specification.
