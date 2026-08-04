# Workflow

Use `$generate-frontend-spec` for a complete run. Provide a feature name plus any available PRD, target project, API contract, and UI reference. Missing optional inputs become explicit gaps; blocking product decisions pause the pipeline after clarification.

Typical request:

> Use `$generate-frontend-spec` for customer group management. The PRD is `customer-groups.md`, the target project is `console-ui`, the API is `openapi.yaml`, and the UI source is the supplied Figma frame.

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
