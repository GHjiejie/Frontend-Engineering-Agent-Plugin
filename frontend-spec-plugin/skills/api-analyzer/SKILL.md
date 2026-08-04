---
name: api-analyzer
description: Analyze OpenAPI, Swagger, protobuf, typed clients, or backend contract documentation and map backend operations to frontend requirements. Use when Codex must identify request and response models, errors, authentication, pagination, filtering, idempotency, cancellation, and backend capability gaps for a frontend feature.
---

# API Analyzer

Write `frontend-spec/api/api-map.json` and `frontend-spec/api/request-response.md`.

## Build the contract map

1. Read `../../references/artifact-contract.md` and `../../schemas/api-map.schema.json`.
2. Prefer machine-readable contracts over examples or prose when they conflict. Record the conflict.
3. Read only the supplied API contract or explicitly named frontend client files. Do not search the repository for endpoints, backend implementations, or additional project context.
4. Assign stable IDs `API-###` and map each operation to requirement IDs.
5. Capture method, path, operation identifier, authentication, path/query/header/body fields, response variants, error codes, pagination, sorting, filtering, rate limits, idempotency, and cancellation behavior when specified.
6. Derive frontend models from declared schemas while preserving nullability, optionality, enums, formats, and discriminators.

## Identify gaps

- Required feature with no backend operation
- Contract fields that cannot render or submit the required UI
- Ambiguous success or error envelopes
- Mismatched identifiers, pagination, permission, or lifecycle semantics
- UI behavior that would require unsupported polling, streaming, upload, or bulk behavior

Never invent an endpoint. Label example-only behavior as unverified. Complete the stage only when every API-dependent requirement is mapped or explicitly listed in `gaps` with impact and owner.
