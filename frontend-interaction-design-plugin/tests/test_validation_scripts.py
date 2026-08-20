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
        "## 4. 输入资料与版本\n\n| Source ID | Type | Title / Scope | Version | Open / Download | Original Locator |\n| --- | --- | --- | --- | --- | --- |\n| [PRD-01](https://example.feishu.cn/docx/abc#prd01-file) | PRD | [Customer PRD](https://example.feishu.cn/docx/abc#prd01-file) | v1 | [Download file](https://example.feishu.cn/docx/abc#prd01-file) | `requirements.md` |\n| [API-01](https://example.feishu.cn/docx/abc#api01-file) | API | [Customer API](https://example.feishu.cn/docx/abc#api01-file) | v1 | [Download file](https://example.feishu.cn/docx/abc#api01-file) | `openapi.yaml` |",
        "## 5. 原型页面与状态总览\n\n[PT-01](https://example.feishu.cn/docx/abc?block_id=pt01-image)",
        "## 6. 本次开发范围与非目标",
        "## 7. 页面与组件职责",
        "## 8. User Flow\n\n### UF-01 Create customer\n\nCreate a customer and show a visible result.\n\n```mermaid\nflowchart TD\n  A --> B\n```",
        "## 9. 前端状态设计\n\n### SM-01 Customer page\n\nOwn loading and recovery states.\n\n```mermaid\nstateDiagram-v2\n  [*] --> Ready\n```",
        "## 10. API 使用方案\n\n[API-01](https://example.feishu.cn/docx/abc#api01-file)",
        "## 11. API 与交互 Mapping\n\n### SQ-01 Create request\n\nMap the request to visible UI states.\n\n```mermaid\nsequenceDiagram\n  User->>Frontend: Submit\n```",
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
            "user-flow.md": "UF-01 PRD-01 PT-01 CL-01\n```mermaid\nflowchart TD\n  A --> B\n```\n",
            "state-machine.md": "SM-01 UF-01 PT-01 CL-01\n```mermaid\nstateDiagram-v2\n  [*] --> Ready\n```\n",
            "sequence-diagram.md": "SQ-01 API-01 UF-01 SM-01 CL-01\n```mermaid\nsequenceDiagram\n  User->>Frontend: Submit\n```\n",
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

    def test_local_diagram_reference_is_not_reviewable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_package(root)
            plan = root / "frontend-development-plan.md"
            content = plan.read_text(encoding="utf-8")
            content = content.replace(
                "Create a customer and show a visible result.\n\n```mermaid\nflowchart TD\n  A --> B\n```",
                "详见 user-flow.md。",
            )
            plan.write_text(content, encoding="utf-8")
            errors = validate_design_package.validate_package(root)
            self.assertTrue(
                any("UF-01 must include an inline flowchart" in error for error in errors)
            )

    def test_exported_diagram_image_is_reviewable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_package(root)
            plan = root / "frontend-development-plan.md"
            content = plan.read_text(encoding="utf-8")
            content = content.replace(
                "```mermaid\nflowchart TD\n  A --> B\n```",
                "![UF-01 Create customer](https://example.feishu.cn/media/uf-01)",
                1,
            )
            plan.write_text(content, encoding="utf-8")
            manifest_path = root / "sync-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["fileDigests"]["frontend-development-plan.md"] = hashlib.sha256(
                content.encode("utf-8")
            ).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual([], validate_design_package.validate_package(root))

    def test_unlinked_visual_id_in_plan_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_package(root)
            plan = root / "frontend-development-plan.md"
            plan.write_text(plan.read_text(encoding="utf-8") + "See PT-01.\n", encoding="utf-8")
            errors = validate_design_package.validate_package(root)
            self.assertTrue(any("PT-01 must link" in error for error in errors))

    def test_grouped_visual_ids_in_one_link_are_rejected(self) -> None:
        plan = "[PT-01、PT-02](https://example.feishu.cn/docx/abc?block_id=prototype)\n"
        errors = validate_design_package._validate_visual_id_links(plan)
        self.assertTrue(any("linked individually" in error for error in errors))

    def test_document_home_visual_link_is_rejected(self) -> None:
        plan = "[UF-01](https://example.feishu.cn/docx/abc)\n"
        errors = validate_design_package._validate_visual_id_links(plan)
        self.assertTrue(any("document home" in error for error in errors))

    def test_heading_and_diagram_contents_are_exempt(self) -> None:
        plan = "## UF-01 新增客户\n\n```mermaid\nA[PT-01] --> B[SM-01]\n```\n"
        self.assertEqual([], validate_design_package._validate_visual_id_links(plan))

    def test_unlinked_source_id_in_plan_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_valid_package(root)
            plan = root / "frontend-development-plan.md"
            plan.write_text(plan.read_text(encoding="utf-8") + "See PRD-01.\n", encoding="utf-8")
            errors = validate_design_package.validate_package(root)
            self.assertTrue(any("PRD-01 must link" in error for error in errors))

    def test_grouped_source_ids_in_one_link_are_rejected(self) -> None:
        plan = "[API-01、API-02](https://example.feishu.cn/docx/abc#api-file)\n"
        errors = validate_design_package._validate_source_id_links(plan)
        self.assertTrue(any("source IDs must be linked individually" in error for error in errors))

    def test_review_document_home_source_link_is_rejected(self) -> None:
        plan = (
            "## Review Source\n\n"
            "- Feishu Document: https://example.feishu.cn/docx/abc\n\n"
            "[PRD-01](https://example.feishu.cn/docx/abc)\n"
        )
        errors = validate_design_package._validate_source_id_links(plan)
        self.assertTrue(any("source attachment block" in error for error in errors))

    def test_external_canonical_source_document_is_allowed(self) -> None:
        plan = (
            "## Review Source\n\n"
            "- Feishu Document: https://example.feishu.cn/docx/abc\n\n"
            "[PRD-01](https://product.feishu.cn/docx/prd)\n"
        )
        self.assertEqual([], validate_design_package._validate_source_id_links(plan))

    def test_static_source_inventory_title_and_action_are_rejected(self) -> None:
        plan = (
            "## 4. 输入资料与版本\n\n"
            "| Source ID | Type | Title / Scope | Version | Open / Download | Original Locator |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| [PRD-01](https://example.feishu.cn/docx/abc#prd-file) | PRD | Static title | v1 | Static filename.md | `/tmp/file.md` |\n"
            "## 5. 原型页面与状态总览\n"
        )
        errors = validate_design_package._validate_source_inventory(plan)
        self.assertTrue(any("title must be linked" in error for error in errors))
        self.assertTrue(any("open/download action" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
