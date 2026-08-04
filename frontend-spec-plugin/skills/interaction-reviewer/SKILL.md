---
name: interaction-reviewer
description: Present a frontend interaction draft to the developer, collect requested changes, and record explicit approval for the current revision. Use after interaction design and whenever user-visible interaction behavior changes. Block flow diagrams and final specification generation until the developer clearly approves the current interaction revision.
---

# Interaction Reviewer

Maintain `frontend-spec/interaction/interaction-review.md` and the review fields in `interaction-spec.json`.

## Publish the review

1. Read `../../references/artifact-contract.md`, the interaction draft, requirement decisions, UI tree, and API map.
2. Build a concise review matrix for every `IX-###`: trigger, visible states, validation, API call, success feedback, failure feedback, recovery, refresh/navigation, and evidence or decision IDs.
3. Separate sourced behavior from developer-approved decisions and unresolved proposals. Never present a generated recommendation as approved.
4. Write the reviewed revision and set `interaction-review` to `blocked` with `Awaiting explicit developer approval`.
5. Ask the developer to reply with either requested changes or an unambiguous approval that names the current revision, such as `确认交互方案 revision 3`.
6. Stop the turn. Do not invoke flow-generator or frontend-spec-generator in the review turn.

## Handle the developer response

- Treat silence, a new unrelated request, or an assistant-authored statement as no approval.
- If the developer requests changes, append the decisions, return to interaction design, increment `revision`, set `review_status: changes_requested` and then `pending_review`, clear `approval`, publish a new review, and remain blocked.
- If the developer unambiguously approves the current revision, append a `DEC-###` entry to `decision-log.md` and set:
  - `review_status: approved`
  - `approval.decision_id` to that decision ID
  - `approval.revision` to the current interaction revision
  - `approval.approved_by` and `approval.approved_at`
- Mark `interaction-review` complete only when the approval revision exactly equals the current interaction revision.

## Invalidate stale approval

Any later change to requirements, prototype, API mapping, or interactions that affects user-visible behavior must increment the interaction revision, clear `approval`, set `review_status: pending_review`, and return this stage to blocked. Never carry an approval across revisions.
