from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PLUGIN_ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


verify_sync_manifest = load_module(
    "verify_sync_manifest", SCRIPTS / "verify_sync_manifest.py"
)

import sys

sys.modules["verify_sync_manifest"] = verify_sync_manifest
validate_design_package = load_module(
    "validate_design_package", SCRIPTS / "validate_design_package.py"
)


PLAN_SECTIONS = "\n\n".join(
    [
        "# Customer Frontend Development Plan\n\nStatus: Ready for Technical Review",
        "## Review Source\n\n- Feishu Document: https://example.feishu.cn/docx/abc\n- Feishu Revision: `42`\n- Synced At: `2026-08-10T16:20:00+08:00`\n- Export Mode: cloud-media",
        "## 1. Review 导读",
        "## 2. 功能背景与问题",
        "## 3. 目标用户与使用场景",
        "## 4. 输入资料与版本\n\nPRD-01 PT-01 API-01",
        "## 5. 原型页面与状态总览\n\nPT-01",
        "## 6. 本次开发范围与非目标",
        "## 7. 页面与组件职责",
        "## 8. User Flow\n\nUF-01",
        "## 9. 前端状态设计\n\nSM-01",
        "## 10. API 使用方案\n\nAPI-01",
        "## 11. API 与交互 Mapping\n\nSQ-01",
        "## 12. 异常与边界状态",
        "## 13. 关键开发决策\n\nCL-01",
        "## 14. 开发任务拆分\n\nFE-01",
        "## 15. 验收标准",
        "## 16. 已确认事项",
        "## 17. 未解决问题",
        "## 18. 追踪矩阵",
        "## 19. Technical Review 清单",
        "## 20. Revision 与同步信息",
    ]
) + "\n"


class ValidationScriptsTest(unittest.TestCase):
    def create_valid_package(self, root: Path) -> None:
        files = {
            "source-manifest.md": "Status: Ready\nSource Gate: PASS\nPRD-01 PT-01 API-01\n",
            "clarification.md": "Status: Resolved\nClarification Gate: PASS\nCL-01\nPRD-01 PT-01 API-01\n",
            "user-flow.md": "UF-01 PRD-01 PT-01 CL-01\n",
            "state-machine.md": "SM-01 UF-01 PT-01 CL-01\n",
            "sequence-diagram.md": "SQ-01 API-01 UF-01 SM-01 CL-01\n",
            "frontend-development-plan.md": PLAN_SECTIONS,
        }
        for name, content in files.items():
            (root / name).write_text(content, encoding="utf-8")

        plan_digest = hashlib.sha256(PLAN_SECTIONS.encode("utf-8")).hexdigest()
        manifest = {
            "feature": "customer-management",
            "version": "2026-08-10",
            "feishuDocumentUrl": "https://example.feishu.cn/docx/abc",
            "feishuDocumentToken": "doxcnabc",
            "feishuRevisionId": 42,
            "syncedAt": "2026-08-10T16:20:00+08:00",
            "exportMode": "cloud-media",
            "syncedFiles": ["frontend-development-plan.md"],
            "prototypeIds": ["PT-01"],
            "fileDigests": {"frontend-development-plan.md": plan_digest},
            "status": "in-sync",
        }
        (root / "sync-manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    def test_valid_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_package(root)
            self.assertEqual([], validate_design_package.validate_package(root))

    def test_digest_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_package(root)
            plan = root / "frontend-development-plan.md"
            plan.write_text(plan.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
            errors = verify_sync_manifest.validate_manifest(
                root / "sync-manifest.json", strict=True
            )
            self.assertTrue(any("digest mismatch" in error for error in errors))

    def test_undefined_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_package(root)
            flow = root / "user-flow.md"
            flow.write_text(flow.read_text(encoding="utf-8") + "PT-99\n", encoding="utf-8")
            errors = validate_design_package.validate_package(root)
            self.assertTrue(any("PT-99 is referenced" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
