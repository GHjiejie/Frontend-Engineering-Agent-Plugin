---
name: source-evidence-manager
description: Persist PRD, prototype, and backend API evidence for a confirmed frontend feature version, including downloadable source-file attachments, Figma node screenshots, and prototype images supplied in the conversation, then create source-manifest.md and a Feishu evidence document with lark-cli by default. Use before requirement clarification whenever an end-to-end frontend design request starts, source documents change, evidence exists only locally or in chat, or reviewers need durable context outside the current session.
---

# Source Evidence Manager

Create or update only the confirmed version's `source-manifest.md`, its Feishu Review document, and optional offline-export assets. Do not clarify business behavior, create interaction models, generate application code, or choose a project/version for the developer.

## Require confirmed scope

Require the developer-confirmed absolute frontend project root, feature name, version, output directory, and planned Feishu document title. If Gate #1 or Gate #2 has not passed, return to `frontend-plan-generator` preflight and pause before any local or Feishu write.

Read these references before acting:

- `references/source-manifest-contract.md` for the local artifact.
- `references/source-attachment-contract.md` when any PRD, API contract, matrix, or other non-image source is supplied as a local or conversation-uploaded file.
- `references/prototype-evidence-contract.md` when any prototype is supplied.
- `references/lark-publishing-workflow.md` before using Feishu or `lark-cli`.

## Collect sources

1. Inventory the Product PRD, prototype, and API contract.
2. Assign stable IDs: `PRD-xx`, `PT-xx`, and `API-xx`. Preserve existing IDs across updates.
3. Record title, locator, version/revision, capture time with timezone, confirmed scope, access status, and evidence location.
4. Treat missing consequential sources, unreadable content, mutable links without a snapshot, and inaccessible evidence as blockers.
5. Never persist secrets, credentials, session cookies, or confidential fields that are outside the confirmed feature scope.

## Persist source-file attachments

For every user-uploaded or local PRD, API contract, permission matrix, data dictionary, or equivalent review source:

1. Inspect the exact file, compute its SHA-256 digest, and confirm it contains no out-of-scope secrets.
2. Insert the original file into the Feishu Review document as a visible file card under `原始来源附件`; do not substitute a filename, local path, repository path, or summary.
3. Preserve the original filename and record the returned file token, file-card block ID, byte size, digest, and stable block link.
4. Make the Source ID, title, and `查看/下载原文件` action navigate to that exact file card. Keep any original canonical URL or repository locator in a separate field.
5. Fetch and preview or download the uploaded file to verify reviewer retrieval. A static source row or inaccessible file card blocks Source Gate.

For an accessible cloud-native source, retain its canonical URL and revision. Add a file snapshot when it is mutable, access is uncertain, or the uploaded file is the reviewed version. Do not upload an entire directory or repository without explicit scope.

## Persist prototype evidence

### Conversation or local images

1. Inspect the supplied image; never guess a local file path for an unavailable attachment.
2. Give each page or visible state a `PT-xx`, concise name, and caption.
3. Insert it into the confirmed Feishu document with `lark-cli` by default.
4. Record a stable, copyable Feishu image-block link (or its uniquely paired caption-block link when the image block cannot be linked directly), the block ID, and what the image does and does not prove. A document-home URL is not an adequate block locator when an exact block can be resolved.
5. If a static image omits transitions, validation, failure, permission, or async behavior, leave those facts unresolved for `requirement-clarification`.

### Figma and other prototype URLs

1. Resolve the exact file/page/frame/node in scope; do not use only a file home URL when a precise node can be identified.
2. Capture the relevant pages and key visible states with available Figma or browser capabilities.
3. Upload each capture to the Feishu document, assign `PT-xx`, retain the original node URL, node ID, and capture time, and record the exact Feishu image/caption block link used by downstream references.
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
- Every user-uploaded or local PRD/API source has a verified Feishu file card, stable block link, file token, digest, and download check.
- Every relevant prototype page/state has a durable `PT-xx` evidence entry.
- The API contract and its version are locatable.
- No consequential source exists only in chat.
- Reviewers can access the evidence, or the review document contains an adequate durable summary.

Otherwise set `Source Gate: BLOCKED`, list focused remediation items, and stop before `requirement-clarification`.

## Validate and hand off

Verify all locators, unique IDs, source attachments, prototype captions, access states, confirmed paths, and Gate status. Resolve every recorded source-file and prototype block locator inside the expected Review document, and verify source-file retrieval. Hand off the exact `source-manifest.md` path, Feishu URL/token, source IDs, attachment/file tokens, block links, digests, and source-gate result. Permit `requirement-clarification` only when Gate #3 passes.
