# Architecture

Frontend Spec Generator is an artifact-driven pipeline. One orchestration skill runs seven bounded analysis stages plus change tracking; each stage reads approved upstream artifacts and writes a versioned output. Stable IDs provide traceability from requirements through UI, API, interactions, diagrams, and the final handoff.

```text
PRD + prototype + API
          │
          ▼
requirements → clarification gate
                         │
                         ▼
                 UI tree + API map
                         │
                         ▼
             interaction specification
                         │
                         ▼
            flows → development spec
                         │
                         ▼
              overrides + change history
```

The plugin intentionally stops before code generation and never scans the surrounding project for background. Its default evidence boundary is product requirements, UI prototypes, and API contracts. Explicitly supplied frontend code may be inspected only within the user-selected scope. `pipeline-state.json` is the resumable control plane; the artifact tree is the durable data plane.

Manual decisions have higher authority than generated text. Regeneration uses the change tracker to preserve overrides and surface conflicts rather than silently replacing them.
