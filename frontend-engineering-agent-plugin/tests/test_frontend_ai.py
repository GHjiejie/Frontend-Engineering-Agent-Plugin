from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "frontend_ai.py"
SPEC = importlib.util.spec_from_file_location("frontend_ai", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
frontend_ai = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(frontend_ai)


USER_FACING_CONTRACT = """schemaVersion: 2
taskId: TASK-001
type: feature
status: READY
designEvidence:
  uiImpact: USER_FACING
  prototypeRequired: true
  prototypeStatus: PROVIDED
  prototypeProvidedBy: human
  prototypes:
    - id: PROTO-001
      type: figma
      locator: https://figma.example/frame
  interactionStatus: COMPLETE
  interactionProvidedBy: human
  interactionFlows:
    - id: INT-001
      prototypeRef: PROTO-001
      trigger: retry-button
      action: click
      result: loading-then-success-or-error
  uiStates:
    - id: UI-STATE-001
      name: loading
  unresolvedDesignGaps: []
  prototypeNotRequiredReason: ""
  uiInvariantEvidence: []
"""


NO_UI_IMPACT_CONTRACT = """schemaVersion: 2
taskId: TASK-002
type: refactor
status: READY
designEvidence:
  uiImpact: NONE
  prototypeRequired: false
  prototypeStatus: NOT_REQUIRED
  prototypeProvidedBy: not-required
  prototypes: []
  interactionStatus: NOT_REQUIRED
  interactionProvidedBy: not-required
  interactionFlows: []
  uiStates: []
  unresolvedDesignGaps: []
  prototypeNotRequiredReason: "Only internal type extraction; rendered output and handlers are unchanged."
  uiInvariantEvidence:
    - src/components/RetryButton.tsx snapshot and event-handler tests remain unchanged
"""


class DesignEvidenceTests(unittest.TestCase):
    def write_contract(self, root: Path, content: str) -> Path:
        path = root / "docs" / "frontend-ai" / "runtime" / "change-contract.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_user_facing_contract_accepts_human_prototype_and_interactions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_contract(Path(directory), USER_FACING_CONTRACT)
            self.assertEqual(frontend_ai.contract_design_evidence_errors(path), [])

    def test_user_facing_contract_rejects_missing_prototype(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            content = USER_FACING_CONTRACT.replace("prototypeStatus: PROVIDED", "prototypeStatus: MISSING").replace(
                "  prototypes:\n    - id: PROTO-001\n      type: figma\n      locator: https://figma.example/frame",
                "  prototypes: []",
            )
            path = self.write_contract(Path(directory), content)
            errors = frontend_ai.contract_design_evidence_errors(path)
            self.assertTrue(any("prototypeStatus: PROVIDED" in error for error in errors))
            self.assertTrue(any("non-empty prototypes" in error for error in errors))

    def test_user_facing_contract_rejects_incomplete_interactions_and_open_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            content = USER_FACING_CONTRACT.replace("interactionStatus: COMPLETE", "interactionStatus: INCOMPLETE").replace(
                "  interactionFlows:\n    - id: INT-001\n      prototypeRef: PROTO-001\n      trigger: retry-button\n      action: click\n      result: loading-then-success-or-error",
                "  interactionFlows: []",
            ).replace("  unresolvedDesignGaps: []", "  unresolvedDesignGaps: [missing-error-state]")
            path = self.write_contract(Path(directory), content)
            errors = frontend_ai.contract_design_evidence_errors(path)
            self.assertTrue(any("interactionStatus: COMPLETE" in error for error in errors))
            self.assertTrue(any("non-empty interactionFlows" in error for error in errors))
            self.assertTrue(any("unresolvedDesignGaps must be empty" in error for error in errors))

    def test_no_ui_impact_accepts_reason_and_invariant_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_contract(Path(directory), NO_UI_IMPACT_CONTRACT)
            self.assertEqual(frontend_ai.contract_design_evidence_errors(path), [])

    def test_no_ui_impact_rejects_missing_exception_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            content = NO_UI_IMPACT_CONTRACT.replace(
                '  prototypeNotRequiredReason: "Only internal type extraction; rendered output and handlers are unchanged."',
                '  prototypeNotRequiredReason: ""',
            ).replace(
                "  uiInvariantEvidence:\n    - src/components/RetryButton.tsx snapshot and event-handler tests remain unchanged",
                "  uiInvariantEvidence: []",
            )
            path = self.write_contract(Path(directory), content)
            errors = frontend_ai.contract_design_evidence_errors(path)
            self.assertTrue(any("prototypeNotRequiredReason" in error for error in errors))
            self.assertTrue(any("non-empty uiInvariantEvidence" in error for error in errors))

    def test_analysis_approval_transition_is_blocked_without_design_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(frontend_ai.initialize(root), 0)
            self.assertEqual(frontend_ai.transition_state(root, "MEMORY_SYNC", "TASK-003", "", "test"), 0)
            self.assertEqual(frontend_ai.transition_state(root, "CONTEXT_BUILD", "TASK-003", "", "test"), 0)
            self.assertEqual(frontend_ai.transition_state(root, "ANALYSIS", "TASK-003", "", "test"), 0)
            contract = USER_FACING_CONTRACT.replace("  prototypes:\n    - id: PROTO-001\n      type: figma\n      locator: https://figma.example/frame", "  prototypes: []")
            self.write_contract(root, contract)
            result = frontend_ai.transition_state(root, "APPROVAL_REQUIRED", "TASK-003", "", "test")
            self.assertEqual(result, 2)
            state = root / "docs" / "frontend-ai" / "runtime" / "state.yaml"
            self.assertEqual(frontend_ai.yaml_scalar(state, "state"), "ANALYSIS")


if __name__ == "__main__":
    unittest.main()
