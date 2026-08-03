---
name: frontend-review
description: Review an implemented frontend feature against its Feature Contract, implementation plan, UI and API inputs, interaction paths, repository rules, architecture memory, decisions, tests, accessibility, and actual diff; produce a severity-ranked review report and finalize feature and memory state only when evidence supports release. Use for pre-merge quality review, acceptance validation, regression assessment, or release readiness of a frontend feature.
---

# Frontend Review

Determine release readiness from evidence. Review first; do not silently repair implementation defects in the same pass unless the user explicitly asks for fixes.

## Preconditions

1. Read repository instructions and inspect the actual worktree and diff.
2. Load the feature contract, implementation plan, change log, project memory, domain memory, relevant ADRs, and source inputs such as designs or API documentation.
3. Require the feature to be in lifecycle `IMPLEMENTING` with orchestrator state `VERIFYING`. If artifacts are stale, record `CONFLICT`.

## Review dimensions

1. **Feature coverage:** Trace every requirement and acceptance criterion to implemented code and evidence.
2. **UI coverage:** Compare layout, content, states, responsiveness, accessibility, and token usage to the specified design or contract.
3. **API coverage:** Verify endpoint, method, parameters, types, mapping, cancellation, loading, retry, success, and failure behavior.
4. **Interaction coverage:** Follow each trigger through request, pending state, success, failure, recovery, duplicate action, and permission path.
5. **Architecture:** Check repository rules, dependency direction, component boundaries, API layer, state lifetime, duplication, and ADR compliance.
6. **Code quality:** Check correctness, typing, maintainability, security, performance, compatibility, and unintended scope.
7. **Verification:** Inspect tests and run the most relevant typecheck, lint, test, build, and targeted UI checks. Distinguish passing, failing, and not run.
8. **Memory integrity:** Verify memory changes describe durable facts and do not claim unreviewed or nonexistent capabilities.

## Findings and outcome

Write `docs/frontend-ai/reports/<feature-id>-review-report.md` using [references/review-report.md](references/review-report.md). Rank actionable findings as `P0`, `P1`, `P2`, or `P3`, cite exact file and line evidence, and avoid speculative findings.

- `PASS`: no open P0-P2 findings, required checks pass, and every acceptance criterion is supported by evidence.
- `NEED_HUMAN_REVIEW`: product, design, API, or business intent requires a human decision.
- `BLOCKED`: required evidence or environment is unavailable.
- `FAIL`: confirmed defects prevent release.

On `PASS`, set feature status to `RELEASED`, orchestrator state to `MEMORY_UPDATING`, update the feature registry, append one capability-oriented JSON object to `evolution-log.jsonl`, update `history.yaml` and `memory-index.json`, then set orchestrator state to `COMPLETED`.

On any other outcome, keep the lifecycle at `IMPLEMENTING`, set `reviewStatus` to the outcome, set orchestrator state to `FAILED`, `BLOCKED`, or `NEED_HUMAN_REVIEW` as applicable, and route code fixes back to `frontend-implementation` or contract issues to `frontend-analysis`.

Run `python3 <plugin-root>/scripts/frontend_ai.py validate --root <repository-root> --feature <feature-id> --phase review` after writing the report and final state.

## Handoff

Lead with findings ordered by severity. Then report the outcome, acceptance coverage, checks run, residual risks, and exact next owner. If there are no findings, say so explicitly and still disclose verification gaps.
