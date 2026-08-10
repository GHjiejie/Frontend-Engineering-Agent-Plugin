---
name: source-evidence-manager
description: Persist PRD, prototype, and backend API evidence for a confirmed frontend feature version, including Figma node screenshots and prototype images pasted into the conversation, then create source-manifest.md and a Feishu evidence document using lark-cli by default. Use before requirement clarification whenever an end-to-end frontend design request starts, source documents change, prototype evidence exists only in chat, or reviewers need durable context outside the current session.
---

# Source Evidence Manager

Create or update only the confirmed version's `source-manifest.md`, its Feishu Review document, and optional `assets/prototype/` files in offline export mode. Do not clarify business behavior, create interaction models, generate application code, or choose a project/version for the developer.

## Require confirmed scope

Require the developer-confirmed absolute frontend project root, feature name, version, output directory, and planned Feishu document title. If Gate #1 or Gate #2 has not passed, return to `frontend-plan-generator` preflight and pause before any local or Feishu write.

Read these references before acting:

- `references/source-manifest-contract.md` for the local artifact.
- `references/prototype-evidence-contract.md` when any prototype is supplied.
- `references/lark-publishing-workflow.md` before using Feishu or `lark-cli`.

## Collect sources

1. Inventory the Product PRD, prototype, and API contract.
2. Assign stable IDs: `PRD-xx`, `PT-xx`, and `API-xx`. Preserve existing IDs across updates.
3. Record title, locator, version/revision, capture time with timezone, confirmed scope, access status, and evidence location.
4. Treat missing consequential sources, unreadable content, mutable links without a snapshot, and inaccessible evidence as blockers.
5. Never persist secrets, credentials, session cookies, or confidential fields that are outside the confirmed feature scope.

## Persist prototype evidence

### Conversation or local images

1. Inspect the supplied image; never guess a local file path for an unavailable attachment.
2. Give each page or visible state a `PT-xx`, concise name, and caption.
3. Insert it into the confirmed Feishu document with `lark-cli` by default.
4. Record the Feishu block locator and what the image does and does not prove.
5. If a static image omits transitions, validation, failure, permission, or async behavior, leave those facts unresolved for `requirement-clarification`.

### Figma and other prototype URLs

1. Resolve the exact file/page/frame/node in scope; do not use only a file home URL when a precise node can be identified.
2. Capture the relevant pages and key visible states with available Figma or browser capabilities.
3. Upload each capture to the Feishu document, assign `PT-xx`, and retain the original node URL, node ID, and capture time.
4. Block the source gate if the URL is inaccessible, the relevant node range is unclear, or essential states cannot be captured.

## Use Feishu safely

- Confirm `lark-cli` is available before starting the write workflow. If it is unavailable, block Gate #3 instead of pretending the evidence was persisted; use another Feishu path only when the user explicitly authorizes that fallback.
- Prefer `lark-cli` for Feishu document creation, updates, media insertion, reads, and downloads.
- Before a Feishu operation, read the installed CLI's matching embedded skill and required references; do not infer flags from memory.
- Use the user identity by default and preserve existing permissions.
- Do not expand public access, add collaborators, or publish externally unless the user explicitly asks.
- Reuse the current feature/version document instead of creating duplicates during the same iteration.

## Manage Source Gate #3

Set `Source Gate: PASS` only when:

- PRD scope is readable or durably summarized.
- Every relevant prototype page/state has a durable `PT-xx` evidence entry.
- The API contract and its version are locatable.
- No consequential source exists only in chat.
- Reviewers can access the evidence, or the review document contains an adequate durable summary.

Otherwise set `Source Gate: BLOCKED`, list focused remediation items, and stop before `requirement-clarification`.

## Validate and hand off

Verify all locators, unique IDs, prototype captions, access states, confirmed paths, and Gate status. Hand off the exact `source-manifest.md` path, Feishu URL/token when available, source IDs, and source-gate result. Permit `requirement-clarification` only when Gate #3 passes.
