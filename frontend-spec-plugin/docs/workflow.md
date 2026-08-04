# Workflow

Use `$generate-frontend-spec` for a complete run. Provide a feature name plus the PRD or requirement, UI prototype, and API contract. Inputs the user explicitly marks unavailable become visible gaps; blocking product decisions pause the pipeline after clarification.

The first turn always performs an input preflight. If the requirement, prototype, or API is missing, the plugin asks for all missing categories together and stops. It does not inspect files or initialize the artifact tree until the user supplies each category or explicitly says it is unavailable.

After preflight, the plugin lists only its own feature catalog. It resumes a feature only when the developer explicitly names it or the conversation clearly continues it. A new requirement receives a new `frontend-spec/features/<feature-id>/` tree. When the old root-level layout is detected, the plugin asks before registering it as a legacy feature; no files are moved.

Typical request:

> Use `$generate-frontend-spec` for customer group management. The PRD is `customer-groups.md`, the API is `openapi.yaml`, and the UI source is the supplied Figma frame.

The plugin does not inspect the project for general background. If existing frontend code matters, explicitly name the exact frontend file or directory that may be read.

Use an individual stage skill when the user only needs one artifact, such as `$api-analyzer` for a contract map or `$requirement-clarifier` for a question and decision pass.

The run writes `frontend-spec/catalog.json` plus one isolated tree per feature. Resume by invoking the orchestrator again and naming the existing feature. When upstream evidence changes, the orchestrator invokes `$change-tracker` within that feature root before regeneration.

Validate structure during iteration:

```bash
python3 scripts/validate_frontend_spec.py <workspace>/frontend-spec/features/<feature-id>
```

Require implementation readiness at handoff:

```bash
python3 scripts/validate_frontend_spec.py <workspace>/frontend-spec/features/<feature-id> --require-complete
```
