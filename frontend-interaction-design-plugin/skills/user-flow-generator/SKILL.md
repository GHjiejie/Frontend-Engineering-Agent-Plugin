---
name: user-flow-generator
description: Analyze a product PRD and frontend prototype to generate a reviewable Markdown user-flow artifact with Mermaid flowcharts, actors, pages, interactive elements, actions, branches, and unresolved gaps. Use when Codex is asked to map a feature's end-user journey, start the frontend interaction design pipeline, or write frontend-design/{feature-name}/user-flow.md from PRD, Figma, Axure, screenshots, or written prototype evidence.
---

# User Flow Generator

Create only `frontend-design/<feature-name>/user-flow.md`. Do not generate code or write any downstream artifact.

## Require inputs

Require both a product PRD and readable prototype evidence. Accept Figma, Axure, screenshots, or written UI descriptions. If either input is missing or inaccessible, identify the exact gap and pause before writing the artifact.

Use an explicit feature name when supplied. Otherwise derive a concise lowercase kebab-case name from the PRD and state the derivation. Use a user-specified output root when present; otherwise use `frontend-design/<feature-name>/`.

## Build the flow

1. Read `prompt.md` for the output contract and `examples/customer-management.md` when a concrete shape is helpful.
2. Inventory source evidence: actors, entry conditions, pages, dialogs, controls, fields, and visible prototype states.
3. Identify user actions such as click, input, submit, confirm, cancel, retry, navigate, and return.
4. Model each meaningful goal as a stable `UF-xx` flow. Include success, cancellation, validation, empty, permission, and recoverable failure branches only when supported by evidence.
5. Record contradictions and missing behavior under `待确认项`; never silently choose between conflicting sources.
6. Write the Markdown artifact with Mermaid `flowchart TD` diagrams and the required tables.

## Preserve evidence

- Cite input filenames, URLs, page/frame names, or PRD sections in the evidence inventory.
- Distinguish confirmed behavior from assumptions and open questions.
- Do not invent controls, navigation, permissions, API calls, or hidden system behavior.
- If `user-flow.md` already exists, preserve reviewer notes and manual decisions while applying the requested update.

## Validate and hand off

Verify that every Mermaid node is reachable, every branch rejoins or terminates, every referenced UI element exists in the inventory, and every flow has an entry and terminal outcome. End with a handoff listing what `state-machine-generator` may consume and which gaps still block state modeling.
