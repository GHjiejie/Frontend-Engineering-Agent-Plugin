---
name: state-machine-generator
description: Convert approved UF-xx flows, durable PT-xx prototype evidence, and resolved CL-xx decisions into explicit frontend page and component state models for one confirmed feature version. Use to define relevant loading, empty, data, error, dialog, submitting, success, failed, disabled, cancellation, retry, and recovery behavior after source and clarification gates pass.
---

# State Machine Generator

Create only `<confirmed-output-directory>/state-machine.md`. Do not generate code or write source, flow, sequence, plan, or publishing artifacts.

## Require inputs

Require same-version `source-manifest.md` with `Source Gate: PASS`, `clarification.md` with `Clarification Gate: PASS`, approved `user-flow.md`, and readable `PT-xx` evidence. Route missing evidence to `source-evidence-manager` and semantic ambiguity to `requirement-clarification` before writing.

## Model states

1. Read `prompt.md` and the example when useful.
2. Map each `UF-xx` step to the page or component that renders visible feedback.
3. Assign stable `SM-xx` and event names such as `LOAD`, `SUBMIT`, `RESOLVE`, `REJECT`, and `CANCEL`.
4. Define every transition as current state + event + optional guard + next state + visible effect + evidence.
5. Model only states required by `PT-xx`, `UF-xx`, API evidence, or resolved `CL-xx`; do not add states for formal completeness.
6. Separate persistent domain data from transient UI state and record reset/preservation behavior.
7. Reopen clarification if a guard, transition, feedback, retry, cancellation, or preservation rule remains undecided.

## Validate and hand off

Verify all states are reachable, every async path has confirmed success/failure outcomes, cancellation has a confirmed target or is explicitly unavailable, visible effects match evidence, and each transition traces to `UF-xx`, `PT-xx`, or `CL-xx`. Hand off stable `SM-xx` IDs to `sequence-diagram-generator`.
