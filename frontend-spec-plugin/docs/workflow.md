# Workflow

Use `$generate-frontend-spec` for a complete run. Provide a feature name, PRD or requirement, UI prototype, API contract, and the parent directory where `frontend-spec` should be created. Inputs the user explicitly marks unavailable become visible gaps; blocking product decisions pause the pipeline after clarification.

The first turn always performs an input preflight. If the requirement, prototype, API, or confirmed output location is missing, the plugin asks for all missing items together and stops. It displays the exact absolute `frontend-spec` path and waits for explicit confirmation. The current workspace root is a suggestion, not automatic authorization.

After preflight, the plugin lists only its own feature catalog. It resumes a feature only when the developer explicitly names it or the conversation clearly continues it. A new requirement receives a new `frontend-spec/features/<feature-id>/` tree. When the old root-level layout is detected, the plugin asks before registering it as a legacy feature; no files are moved.

The run then selects one delivery mode:

- `spec_only` is used only when the developer explicitly asks for analysis, documentation, or no code changes.
- `implement_and_validate` is the default when the developer asks to add, build, implement, refactor, restore, or pixel-match a dashboard feature and supplies a node-specific Figma frame.

Implementation mode additionally requires the exact target page/route/scenario and the exact authorized `dashboard-ui` frontend root. The plugin asks for those values rather than inspecting the repository to infer them.

Typical request:

> Use `$generate-frontend-spec` to implement customer group management. The PRD is `customer-groups.md`, the API is `openapi.yaml`, the UI source is this node-specific Figma frame, create `frontend-spec` under `/workspace/dashboard-ui`, and limit code access to `/workspace/dashboard-ui/dashboard/dashboard-ui/src/views/customer-groups` plus its required frontend support files.

The plugin does not inspect the project for general background. If existing frontend code matters, explicitly name the exact frontend file or directory that may be read.

After the specification becomes implementation-ready, the plugin presents its pages, interactions, API mappings, assumptions, and gaps and waits for developer approval. Validator success is not human approval. It then invokes `$dashboard-ui-figma-restore`, obtains Figma design evidence, and writes `implementation/restoration-brief.md`. No application or test code is changed until the developer separately approves that brief.

After approval, the plugin implements only the selected page and runs targeted tests, type checking, build, token/style audits, design visual comparison, and regression visual comparison when those commands exist in the authorized frontend. Results and diff paths are written to `implementation/visual-validation.md`. Approved baselines are never replaced without explicit approval.

Use an individual stage skill when the user only needs one artifact, such as `$api-analyzer` for a contract map or `$requirement-clarifier` for a question and decision pass.

After the exact location is confirmed, the run writes `<confirmed-parent>/frontend-spec/catalog.json` plus one isolated tree per feature. Resume by invoking the orchestrator again, confirming the output location, and naming the existing feature. When upstream evidence changes, the orchestrator invokes `$change-tracker` within that feature root before regeneration.

Validate structure during iteration:

```bash
python3 scripts/validate_frontend_spec.py <confirmed-parent>/frontend-spec/features/<feature-id>
```

Require implementation readiness at handoff:

```bash
python3 scripts/validate_frontend_spec.py <confirmed-parent>/frontend-spec/features/<feature-id> --require-complete
```
