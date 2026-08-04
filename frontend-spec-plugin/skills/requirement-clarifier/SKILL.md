---
name: requirement-clarifier
description: Detect consequential gaps in analyzed frontend requirements, ask focused product questions, and preserve approved answers as durable decisions. Use when a PRD is incomplete, ambiguous, contradictory, or lacks behavior for validation, permissions, confirmations, failures, loading, empty states, refreshes, concurrency, or navigation.
---

# Requirement Clarifier

Produce `frontend-spec/requirement/question-list.md` and maintain `frontend-spec/requirement/decision-log.md`.

## Classify gaps

1. Read `../../references/artifact-contract.md` and the current requirement analysis.
2. Classify each gap as `blocking`, `important`, or `non_blocking` based on whether different answers materially change user behavior, API usage, data integrity, permission, or architecture.
3. Merge duplicates and group related questions by user flow.
4. For every question, include the affected requirement IDs, why the answer matters, options when genuinely known, and a recommended default only when evidence supports it.

## Ask and record

- Ask blocking questions before downstream binding.
- Do not force confirmation for harmless implementation details; record a reversible assumption instead.
- Append confirmed answers to `decision-log.md` with decision ID, date, owner, status, rationale, affected IDs, and superseded decision when applicable.
- Propagate confirmed decisions back into the requirement analysis. Keep the original question traceable.

Mark the stage `blocked` while blocking questions are unanswered. Mark it `complete` only when none remain; important unresolved items must stay visible in the final specification.
