---
name: requirement-analyzer
description: Convert product requirements into traceable frontend pages, actors, features, rules, acceptance criteria, assumptions, and open questions. Use when Codex receives a PRD, Markdown or Word product document, issue description, feature brief, or pasted requirement text that must be structured before frontend design or implementation planning.
---

# Requirement Analyzer

Write `<feature-root>/requirement/requirement-analysis.json` from product evidence.

## Analyze

1. Read `../../references/artifact-contract.md` and `../../schemas/requirement-analysis.schema.json`.
2. Separate source facts, derived implications, assumptions, and missing decisions.
3. Assign stable IDs: `PAGE-###`, `RQ-###`, `RULE-###`, and `Q-###`.
4. For each feature, capture actor, trigger, action, target, preconditions, outcome, business rules, acceptance criteria, priority when stated, and evidence locators.
5. Extract page hierarchy and cross-page navigation without inventing routes.
6. Record non-functional requirements that affect frontend behavior, including permission, accessibility, localization, performance, observability, and compatibility.

## Quality rules

- Make acceptance criteria observable and testable.
- Preserve source terminology and flag inconsistent terms.
- Split compound requirements into atomic features.
- Do not turn an implementation guess into a requirement.
- Add ambiguous deletion, validation, failure, empty-state, permission, refresh, concurrency, and recovery behavior to `open_questions`.

Update the `requirement-analysis` stage only after every feature has an evidence reference or is labeled as an assumption.
