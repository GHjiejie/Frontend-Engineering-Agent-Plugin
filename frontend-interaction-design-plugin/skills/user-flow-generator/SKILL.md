---
name: user-flow-generator
description: Generate a reviewable Markdown user-flow artifact with Mermaid flowcharts, actors, pages, interactive elements, actions, and evidence-backed branches from a product PRD, frontend prototype, and a passed clarification gate. Use when Codex is asked to map an end-user journey or write frontend-design/{feature-name}/user-flow.md after clarification.md is Cleared or Resolved.
---

# User Flow Generator

Create only `frontend-design/<feature-name>/user-flow.md`. Do not generate code or write any downstream artifact.

## Require inputs

Require the product PRD, readable prototype evidence, and `clarification.md`. Accept Figma, Axure, screenshots, or written UI descriptions. Verify `Gate: PASS` and `Status: Cleared` or `Resolved` before writing. If the gate is blocked or an input is missing, return to `requirement-clarification-generator` and pause without creating or updating `user-flow.md`.

Use an explicit feature name when supplied. Otherwise derive a concise lowercase kebab-case name from the PRD and state the derivation. Use a user-specified output root when present; otherwise use `frontend-design/<feature-name>/`.

## Build the flow

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Inventory source evidence: actors, entry conditions, pages, dialogs, controls, fields, and visible prototype states.
3. Identify user actions such as click, input, submit, confirm, cancel, retry, navigate, and return.
4. Model each meaningful goal as a stable `UF-xx` flow. Include success, cancellation, validation, empty, permission, and recoverable failure branches only when supported by evidence or a confirmed `CL-xx` decision.
5. If a new conflict, gap, or multiple-choice behavior appears, append or reopen a clarification item, block the gate, and stop. Never leave an unresolved decision inside a completed user-flow artifact.
6. Write the Markdown artifact with Mermaid `flowchart TD` diagrams and a decision trace to relevant `CL-xx` IDs.

## Preserve evidence

- Cite input filenames, URLs, page/frame names, or PRD sections in the evidence inventory.
- Treat only source evidence and confirmed `CL-xx` decisions as authoritative; do not add assumptions.
- Do not invent controls, navigation, permissions, API calls, or hidden system behavior.
- If `user-flow.md` already exists, preserve reviewer notes and manual decisions while applying the requested update.

## Validate and hand off

Verify that every Mermaid node is reachable, every branch rejoins or terminates, every referenced UI element exists in the inventory, every flow has an entry and terminal outcome, and every non-obvious decision traces to a source or `CL-xx`. End with a handoff confirming the clarification gate still passes and listing what `state-machine-generator` may consume.
