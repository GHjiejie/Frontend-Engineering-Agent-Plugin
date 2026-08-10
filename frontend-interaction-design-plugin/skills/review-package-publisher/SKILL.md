---
name: review-package-publisher
description: Publish a complete frontend development plan and prototype evidence to a Feishu review document with lark-cli, pin the reviewed document revision, explicitly export it to frontend-development-plan.md, write sync-manifest.json, and validate reviewability and sync drift. Use after all source, clarification, user-flow, state-machine, sequence-diagram, and plan-draft prerequisites exist, or when republishing review changes, exporting offline media, or reconciling Feishu/local snapshot drift.
---

# Review Package Publisher

Publish only the confirmed feature/version design package. Do not generate application code, modify product or API behavior, create a new feature version, or silently overwrite manual local edits.

Read before acting:

- `references/feishu-review-document-contract.md` for the human review surface.
- `references/local-export-contract.md` for revision-pinned export and drift handling.
- `references/reviewability-checklist.md` before assigning a ready status.

## Require a complete draft package

Require from one confirmed output directory:

- `source-manifest.md` with `Source Gate: PASS`.
- `clarification.md` with `Clarification Gate: PASS`.
- `user-flow.md`.
- `state-machine.md`.
- `sequence-diagram.md`.
- `frontend-development-plan.md` with a Draft or review-ready status.
- The Feishu URL/token established by `source-evidence-manager`.

If paths, feature/version values, source IDs, or gates disagree, block publication and return to the owning skill.

## Publish with lark-cli

1. Confirm `lark-cli` is available; otherwise block publication unless the user explicitly authorizes another Feishu path.
2. Read the installed `lark-doc` and `lark-shared` guidance plus every referenced create/update/fetch/media instruction required for this operation.
3. Use `lark-cli` by default; do not silently replace it with browser automation or a different API.
4. Reuse the current feature/version document and preserve prototype blocks.
5. Update the document into the contract order without deleting reviewer comments or unrelated approved notes.
6. Verify the final content by fetching the document.
7. Record the exact final Revision ID. Do not continue editing that revision after it is selected for export.

The Feishu document is the main human Review surface. Include enough context for a product manager or developer who did not join the source conversation.

## Export a fixed revision

1. Check whether the local `frontend-development-plan.md` changed since the last recorded sync. If so, mark `Sync Drift` and stop before overwrite.
2. Fetch the exact Revision ID as Markdown using the installed CLI's supported fixed-revision option.
3. Normalize media references. Keep stable Feishu document/block references in `cloud-media`; download media to `assets/prototype/` only in `offline-media`.
4. Replace the local plan with the exported content only after the drift check passes.
5. Write `sync-manifest.json` using `references/local-export-contract.md`.
6. Resolve the plugin root from this `SKILL.md`, then run `../../scripts/verify_sync_manifest.py` and `../../scripts/validate_design_package.py`.

Do not use ordinary Drive folder sync for the online document; it skips online documents and cannot establish the required document Revision contract.

## Run Reviewability Gate #5

Validate the checklist in `references/reviewability-checklist.md`.

Allowed package states:

- `Ready for Technical Review` when Gates #1–#5 pass but human technical approval is pending.
- `Ready for Development` only after Technical Review approval is recorded and the local snapshot still matches the approved Revision.
- `Sync Drift` when local and Feishu content require reconciliation.
- `Blocked` when sources, decisions, access, publication, or validation remain incomplete.

## Handle review changes

- Keep the same feature/version for comments, evidence additions, clarification answers, diagram corrections, and plan wording changes.
- Route evidence gaps to `source-evidence-manager` and semantic decisions to `requirement-clarification`.
- Regenerate only affected downstream artifacts, update the same Feishu document, select a new Revision, and export again.
- Preserve reviewer notes and manual decisions; never erase them as a side effect of regeneration.

## Hand off

Return the Feishu document link and Revision, local output directory, export mode, validator results, Reviewability Gate result, and next allowed action. Do not claim `Ready for Development` unless approval and sync checks both pass.
