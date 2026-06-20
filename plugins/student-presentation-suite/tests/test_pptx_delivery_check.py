from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "student-presentation-ppt" / "scripts" / "pptx_delivery_check.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pptx_delivery_check", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PptxDeliveryCheckTests(unittest.TestCase):
    def write_minimal_pptx(self, path: Path, *, embedded_notes: bool = False) -> None:
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("[Content_Types].xml", "<Types/>")
            zf.writestr("_rels/.rels", "<Relationships/>")
            zf.writestr(
                "ppt/presentation.xml",
                """<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>""",
            )
            zf.writestr("ppt/_rels/presentation.xml.rels", "<Relationships/>")
            zf.writestr(
                "ppt/slides/slide1.xml",
                """<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>""",
            )
            if embedded_notes:
                zf.writestr(
                    "ppt/notesSlides/notesSlide1.xml",
                    """<p:notes xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>""",
                )

    def write_png(self, path: Path) -> None:
        path.write_bytes(
            b"\x89PNG\r\n\x1a\n"
            + b"\x00\x00\x00\rIHDR"
            + (320).to_bytes(4, "big")
            + (180).to_bytes(4, "big")
        )

    def test_derives_and_requires_notes_and_preview_by_default(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "demo-presentation.pptx"
            self.write_minimal_pptx(pptx)

            result = module.inspect_delivery(pptx, None, [])

        self.assertEqual(["notes", "preview"], result["missing_expected_files"])
        self.assertTrue(result["requirements"]["notes_required"])
        self.assertTrue(result["requirements"]["preview_required"])

    def test_embedded_notes_satisfy_notes_requirement(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "demo-presentation.pptx"
            preview = Path(tmp) / "demo-preview.png"
            self.write_minimal_pptx(pptx, embedded_notes=True)
            self.write_png(preview)
            result = module.inspect_delivery(pptx, None, [preview])
        self.assertEqual([], result["missing_expected_files"])
        self.assertEqual(1, result["embedded_notes_count"])

    def test_invalid_preview_is_fatal_in_strict_mode(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "demo-presentation.pptx"
            notes = Path(tmp) / "demo-speaker-notes.md"
            preview = Path(tmp) / "demo-preview.png"
            self.write_minimal_pptx(pptx)
            notes.write_text("notes", encoding="utf-8")
            preview.write_text("not an image", encoding="utf-8")
            result = module.inspect_delivery(pptx, notes, [preview])
        self.assertIn("preview-invalid", result["fatal_issues"])
        self.assertEqual(
            2,
            module.determine_exit_code(result, strict=True, fail_on_blockers=False),
        )

    def test_corrupt_pptx_is_fatal_in_strict_mode(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "broken.pptx"
            pptx.write_bytes(b"not-a-zip")
            result = module.inspect_delivery(
                pptx,
                None,
                [],
                require_notes=False,
                require_preview=False,
            )
        self.assertIn("pptx-invalid", result["fatal_issues"])
        self.assertEqual(
            2,
            module.determine_exit_code(result, strict=True, fail_on_blockers=False),
        )

    def test_explicit_exceptions_do_not_report_optional_files_missing(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "demo-presentation.pptx"
            self.write_minimal_pptx(pptx)

            result = module.inspect_delivery(
                pptx,
                None,
                [],
                require_notes=False,
                require_preview=False,
            )

        self.assertEqual([], result["missing_expected_files"])

    def test_font_inheritance_uncertainty_is_not_blocker_like(self) -> None:
        module = load_module()
        result = module.summarize_static_risks(
            {
                "findings": [
                    {
                        "slide": 1,
                        "shape": 1,
                        "text_preview": "Inherited text",
                        "char_count": 14,
                        "min_font_pt": None,
                        "risk": ["font-size-not-explicit"],
                    }
                ]
            }
        )

        self.assertEqual(0, result["blocker_like_count"])

    def test_fail_on_blockers_uses_exit_code_three(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            pptx = Path(tmp) / "demo-presentation.pptx"
            self.write_minimal_pptx(pptx)
            static_result = {
                "findings": [
                    {
                        "slide": 1,
                        "shape": 1,
                        "text_preview": "Dense body text",
                        "char_count": 300,
                        "min_font_pt": 18,
                        "risk": ["paragraph-heavy-slide-text"],
                    }
                ]
            }
            with mock.patch.object(module, "_load_inspect_pptx", return_value=lambda _: static_result):
                result = module.inspect_delivery(
                    pptx,
                    None,
                    [],
                    require_notes=False,
                    require_preview=False,
                )
        self.assertEqual(
            3,
            module.determine_exit_code(result, strict=True, fail_on_blockers=True),
        )

    def test_cli_can_import_shared_package_without_pythonpath(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
