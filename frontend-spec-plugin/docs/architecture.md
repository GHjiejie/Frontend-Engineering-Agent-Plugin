# Architecture

Frontend Spec Generator is an artifact-driven pipeline. A catalog selects one isolated feature root before the orchestration skill runs seven bounded analysis stages plus change tracking. Stable IDs provide traceability within a feature from requirements through UI, API, interactions, diagrams, and the final handoff.

```text
PRD + prototype + API
          │
          ▼
feature catalog → create / resume gate
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

The plugin intentionally stops before code generation and never scans the surrounding project for background. Its default evidence boundary is product requirements, UI prototypes, API contracts, and its own catalog. Explicitly supplied frontend code may be inspected only within the user-selected scope. `catalog.json` selects the feature data plane; each feature's `pipeline-state.json` is its resumable control plane.

Manual decisions have higher authority than generated text. Regeneration uses the change tracker to preserve overrides and surface conflicts rather than silently replacing them.

Independent requirements never share a feature root. An adopted legacy feature may remain at the catalog root, while every newly created feature uses `features/<feature-id>/`.
