from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "workflow_guard.py"


def load_module():
    spec = importlib.util.spec_from_file_location("workflow_guard", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkflowGuardTests(unittest.TestCase):
    def test_blocks_production_without_confirmation(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", {}, clear=True):
                decision = module.hook_decision(
                    {
                        "tool_name": "Bash",
                        "cwd": tmp,
                        "tool_input": {"command": "python slide_spec_to_pptx_brief.py spec.yaml"},
                    }
                )
        self.assertEqual(
            "deny",
            decision["hookSpecificOutput"]["permissionDecision"],
        )

    def test_allows_after_confirmation(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "outputs" / ".student-presentation-state.json"
            state_path.parent.mkdir()
            state_path.write_text(json.dumps({"state": "intake_confirmed"}), encoding="utf-8")
            with mock.patch.dict("os.environ", {}, clear=True):
                decision = module.hook_decision(
                    {
                        "tool_name": "Bash",
                        "cwd": tmp,
                        "tool_input": {"command": "node run_with_pptxgenjs.js deck.js"},
                    }
                )
        self.assertIsNone(decision)

    def test_ignores_unrelated_bash(self) -> None:
        module = load_module()
        self.assertIsNone(
            module.hook_decision(
                {"tool_name": "Bash", "tool_input": {"command": "git status"}}
            )
        )

    def test_blocked_state_does_not_allow_more_production(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "outputs" / ".student-presentation-state.json"
            state_path.parent.mkdir()
            state_path.write_text(json.dumps({"state": "blocked"}), encoding="utf-8")
            with mock.patch.dict("os.environ", {}, clear=True):
                decision = module.hook_decision(
                    {
                        "tool_name": "Bash",
                        "cwd": tmp,
                        "tool_input": {"command": "node run_with_pptxgenjs.js deck.js"},
                    }
                )
        self.assertEqual("deny", decision["hookSpecificOutput"]["permissionDecision"])


if __name__ == "__main__":
    unittest.main()
