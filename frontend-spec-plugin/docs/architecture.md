# Architecture

Frontend Spec Generator is an artifact-driven pipeline. One orchestration skill runs nine bounded stage skills; each stage reads approved upstream artifacts and writes a versioned output. Stable IDs provide traceability from source requirements through UI, API, interactions, diagrams, and the final handoff.

```text
PRD + project + API + UI
            │
            ▼
context → requirements → clarification gate
                               │
                               ▼
                       API map + UI tree
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

The plugin intentionally stops before code generation. This prevents an unconfirmed product assumption from becoming implementation. `pipeline-state.json` is the resumable control plane; the artifact tree is the durable data plane.

Manual decisions have higher authority than generated text. Regeneration uses the change tracker to preserve overrides and surface conflicts rather than silently replacing them.
