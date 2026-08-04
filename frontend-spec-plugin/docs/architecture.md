# Architecture

Frontend Spec Generator is an artifact-driven frontend delivery pipeline. An explicit location gate selects the absolute `frontend-spec` root, then a catalog selects one isolated feature root before the orchestration skill runs seven bounded analysis stages plus change tracking. A delivery-mode gate either stops at the implementation-ready specification or continues through an approved Figma restoration and mandatory visual validation. Stable IDs provide traceability from requirements through UI, API, interactions, implementation, and final verification.

```text
PRD + prototype + API + confirmed output path
          │
          ▼
         location gate
          │
          ▼
 delivery mode + authorized frontend scope
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
                         ├─────────────── spec_only ──→ handoff
                         │
                         ▼ implement_and_validate
                  restoration brief
                         │
                  developer approval
                         │
                         ▼
             scoped Vue/CSS implementation
                         │
                         ▼
       design comparison + regression comparison
```

The plugin never scans the surrounding project for background. Its default evidence boundary is product requirements, UI prototypes, API contracts, and its own catalog at the confirmed path. In `implement_and_validate` mode, the developer must also name the target page and exact frontend root. Only the target page, minimum direct frontend dependencies, required token files, and relevant visual-test support files may be read. `catalog.json` selects the feature data plane; each feature's `pipeline-state.json` is its resumable specification control plane.

Manual decisions have higher authority than generated text. Regeneration uses the change tracker to preserve overrides and surface conflicts rather than silently replacing them.

Independent requirements never share a feature root. An adopted legacy feature may remain at the catalog root, while every newly created feature uses `features/<feature-id>/`.

Implementation remains separately gated from specification readiness. The plugin writes a restoration brief, waits for approval, then records visual commands and results under the selected feature's optional `implementation/` directory. An implementation is not complete while design or regression comparison is skipped, failing, or blocked.
