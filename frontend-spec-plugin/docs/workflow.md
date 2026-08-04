# Workflow

Use `$generate-frontend-spec` for a complete run. Provide a feature name plus the PRD or requirement, UI prototype, and API contract. Missing inputs become explicit gaps; blocking product decisions pause the pipeline after clarification.

Typical request:

> Use `$generate-frontend-spec` for customer group management. The PRD is `customer-groups.md`, the API is `openapi.yaml`, and the UI source is the supplied Figma frame.

The plugin does not inspect the project for general background. If existing frontend code matters, explicitly name the exact frontend file or directory that may be read.

Use an individual stage skill when the user only needs one artifact, such as `$api-analyzer` for a contract map or `$requirement-clarifier` for a question and decision pass.

The run writes `frontend-spec/` in the selected workspace. Resume by invoking the orchestrator again with the same directory. When upstream evidence changes, the orchestrator invokes `$change-tracker` before regeneration.

Validate structure during iteration:

```bash
python3 scripts/validate_frontend_spec.py <workspace>/frontend-spec
```

Require implementation readiness at handoff:

```bash
python3 scripts/validate_frontend_spec.py <workspace>/frontend-spec --require-complete
```
