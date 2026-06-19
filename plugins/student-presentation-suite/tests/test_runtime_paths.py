from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.runtime_paths import document_skills_compatibility, output_root


def load_env_checker():
    path = ROOT / "scripts/check_claude_pptx_env.py"
    spec = importlib.util.spec_from_file_location("check_claude_pptx_env", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RuntimePathTests(unittest.TestCase):
    def test_output_root_honors_explicit_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            requested = Path(tmp) / "custom deliverables"
            self.assertEqual(requested.resolve(), output_root(requested))

    def test_output_root_falls_back_to_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                Path(tmp).resolve() / "outputs",
                output_root(env={}, cwd=Path(tmp)),
            )

    def test_output_root_uses_project_and_never_plugin_cache(self) -> None:
        with tempfile.TemporaryDirectory(prefix="Claude Project ") as tmp:
            result = output_root(env={"CLAUDE_PROJECT_DIR": tmp})
            self.assertEqual(Path(tmp).resolve() / "outputs", result)
            self.assertNotEqual(ROOT / "outputs", result)

    def test_document_skill_compatibility_detects_guides(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp)
            plugin = config / "cache/document-skills"
            skill = plugin / "skills/pptx"
            skill.mkdir(parents=True)
            for name in ("SKILL.md", "pptxgenjs.md", "editing.md"):
                (skill / name).write_text(name, encoding="utf-8")
            installed = config / "plugins/installed_plugins.json"
            installed.parent.mkdir(parents=True)
            installed.write_text(
                json.dumps(
                    {
                        "plugins": {
                            "document-skills@anthropic-agent-skills": [
                                {"installPath": str(plugin)}
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            result = document_skills_compatibility({"CLAUDE_CONFIG_DIR": str(config)})
            self.assertTrue(result["ok"])

    def test_document_skill_missing_is_incompatible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = document_skills_compatibility({"CLAUDE_CONFIG_DIR": tmp})
            self.assertFalse(result["ok"])
            self.assertIn("pptxgenjs.md", result["missing"])

    def test_pptxgenjs_resolution_order(self) -> None:
        module = load_env_checker()
        success = json.dumps({"path": "X:/node_modules/pptxgenjs/index.js", "version": "4.0.1"})
        with mock.patch.object(module, "command_path", side_effect=lambda name, *_: name):
            with mock.patch.object(module, "npm_global_root", return_value=Path("G:/npm")):
                with mock.patch.object(module, "run_probe", return_value=(True, success)):
                    self.assertEqual("project", module.resolve_pptxgenjs(Path("P:/project"))["module_source"])
                with mock.patch.object(
                    module, "run_probe", side_effect=[(False, "no"), (True, success)]
                ):
                    self.assertEqual("plugin", module.resolve_pptxgenjs(Path("P:/project"))["module_source"])
                with mock.patch.object(
                    module,
                    "run_probe",
                    side_effect=[(False, "no"), (False, "no"), (True, success)],
                ):
                    self.assertEqual("global", module.resolve_pptxgenjs(Path("P:/project"))["module_source"])

    def test_bridge_runs_from_space_path_and_targets_project_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="Claude Project ") as project_tmp:
            project = Path(project_tmp)
            other_cwd = project / "nested working dir"
            other_cwd.mkdir()
            spec_path = project / "spec.yaml"
            spec_path.write_text(
                """
meta:
  duration_min: 1
  slide_count: 1
  format: individual
  output_prefix: portable-demo
slides:
  - id: 1
    title: Demo
    layout: title
    content: Point
    timing_sec: 60
    owner: Individual
""",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["CLAUDE_PROJECT_DIR"] = str(project)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/slide_spec_to_pptx_brief.py"),
                    str(spec_path),
                    "--json",
                ],
                cwd=other_cwd,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            result = json.loads(proc.stdout)
            self.assertEqual(str((project / "outputs").resolve()), result["output_dir"])
            self.assertIn(str(project / "outputs" / "portable-demo-presentation.pptx"), result["brief"])
            self.assertNotIn(str(ROOT / "outputs"), result["brief"])

    def test_node_wrapper_loads_installed_plugin_dependency(self) -> None:
        wrapper = ROOT / "scripts/run_with_pptxgenjs.js"
        if not (ROOT / "node_modules/pptxgenjs").exists():
            self.skipTest("npm dependencies are not installed")
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["CLAUDE_PROJECT_DIR"] = tmp
            proc = subprocess.run(
                ["node", str(wrapper), "--probe"],
                cwd=tmp,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
        result = json.loads(proc.stdout)
        self.assertEqual("plugin", result["source"])
        self.assertTrue(result["version"])


if __name__ == "__main__":
    unittest.main()
