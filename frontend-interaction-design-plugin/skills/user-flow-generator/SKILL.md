---
name: user-flow-generator
description: Generate a reviewable Markdown user flow from a passed source manifest, durable PT-xx prototype evidence, and resolved CL-xx decisions for one confirmed frontend feature version. Use to map end-user goals, pages, controls, actions, cancellation, validation, and supported alternative outcomes after Source Gate #3 and Clarification Gate #4 pass.
---

# User Flow Generator

Create only `<confirmed-output-directory>/user-flow.md`. Do not generate code or write source, state, sequence, plan, or publishing artifacts.

## Require inputs

Require `source-manifest.md` with `Source Gate: PASS` and `clarification.md` with `Clarification Gate: PASS` from the same confirmed project/feature/version. Require readable PRD scope and durable `PT-xx` evidence. If paths disagree or a gate is blocked, return to the owning skill and pause without updating the flow.

Reuse confirmed context exactly. Never rediscover the project, derive a new feature/version, or use a chat-only image.

## Build the flow

1. Read `prompt.md` and the example when useful.
2. Inventory actors, entry conditions, pages, dialogs, controls, fields, and visible states using `PRD-xx` and `PT-xx`.
3. Model each meaningful user goal as a stable `UF-xx`.
4. Include success, validation, cancellation, empty, permission, and recoverable failure branches only when evidenced or resolved by `CL-xx`.
5. Cite the exact prototype page/state at relevant steps.
6. If a new consequential choice appears, reopen clarification in the same version and stop.
7. Write Mermaid `flowchart TD` diagrams, numbered steps, visible outcomes, and evidence traces.

## Preserve evidence

- Treat developer-confirmed decisions as highest priority, followed by non-conflicting source evidence.
- Do not invent controls, navigation, permissions, API calls, or hidden behavior.
- Preserve reviewer notes and approved manual decisions on same-version updates.

## Validate and hand off

Verify every node is reachable, every branch rejoins or terminates, every UI element exists in the evidence inventory, every flow has entry and terminal outcomes, and every non-obvious behavior cites `PRD-xx`, `PT-xx`, or `CL-xx`. Hand off stable `UF-xx` IDs to `state-machine-generator`.
