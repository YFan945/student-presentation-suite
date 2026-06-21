#!/usr/bin/env python3
"""Persist presentation workflow state and block production before confirmation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEQUENCE = (
    "intake_pending",
    "intake_confirmed",
    "planned",
    "producing",
    "qa",
    "complete",
)
TERMINAL = {"incomplete", "blocked"}
PRODUCTION_MARKERS = (
    "slide_spec_to_pptx_brief.py",
    "run_with_pptxgenjs.js",
    "build_support_outputs.py",
    "pptx_delivery_check.py",
    "create_revision_manifest.py",
)


def project_root(cwd: Path | None = None) -> Path:
    configured = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(configured).expanduser().resolve() if configured else (cwd or Path.cwd()).resolve()


def default_state_file(cwd: Path | None = None) -> Path:
    return project_root(cwd) / "outputs" / ".student-presentation-state.json"


def load_state(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def transition_allowed(before: str, after: str) -> bool:
    if after in TERMINAL:
        return before != "intake_pending"
    if before not in SEQUENCE or after not in SEQUENCE:
        return False
    return SEQUENCE.index(after) == SEQUENCE.index(before) + 1


def hook_decision(payload: dict[str, Any]) -> dict[str, Any] | None:
    if payload.get("tool_name") != "Bash":
        return None
    command = str((payload.get("tool_input") or {}).get("command") or "")
    if not any(marker.lower() in command.lower() for marker in PRODUCTION_MARKERS):
        return None
    cwd = Path(payload.get("cwd") or Path.cwd())
    state_path = default_state_file(cwd)
    state = load_state(state_path)
    current = state.get("state") if state else None
    allowed = current in {"intake_confirmed", "planned", "producing", "qa"}
    if allowed:
        return None
    reason = (
        "Student Presentation production is blocked before explicit Production Summary "
        f"confirmation. Initialize and confirm workflow state at {state_path}."
    )
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
            "additionalContext": "Ask for one consolidated confirmation, then run workflow_guard.py confirm.",
        }
    }


def state_command(args: argparse.Namespace) -> int:
    state_path = args.state_file or default_state_file()
    current = load_state(state_path)
    if args.action == "show":
        print(json.dumps(current or {"state": "missing", "path": str(state_path)}, ensure_ascii=False, indent=2))
        return 0
    if args.action == "init":
        save_state(
            state_path,
            {
                "workflow_version": "1.0",
                "state": "intake_pending",
                "topic": args.topic,
                "summary_sha256": None,
            },
        )
    elif args.action == "confirm":
        if not args.summary_file or not args.summary_file.is_file():
            raise SystemExit("--summary-file is required and must exist")
        summary_hash = hashlib.sha256(args.summary_file.read_bytes()).hexdigest()
        base = current or {"workflow_version": "1.0", "topic": args.topic}
        if base.get("state") not in (None, "intake_pending"):
            raise SystemExit(f"Cannot confirm from state {base.get('state')!r}")
        base.update(
            {
                "state": "intake_confirmed",
                "summary_file": str(args.summary_file.resolve()),
                "summary_sha256": summary_hash,
            }
        )
        save_state(state_path, base)
    elif args.action == "transition":
        if not current:
            raise SystemExit("Workflow state does not exist")
        before = str(current.get("state"))
        if not transition_allowed(before, args.to):
            raise SystemExit(f"Invalid transition: {before} -> {args.to}")
        current["state"] = args.to
        save_state(state_path, current)
    print(json.dumps(load_state(state_path), ensure_ascii=False, indent=2))
    return 0


def main() -> None:
    if len(sys.argv) == 1:
        try:
            payload = json.load(sys.stdin)
        except (json.JSONDecodeError, OSError):
            raise SystemExit(0)
        decision = hook_decision(payload)
        if decision:
            print(json.dumps(decision, ensure_ascii=False))
        return

    parser = argparse.ArgumentParser(description="Manage Student Presentation workflow state")
    sub = parser.add_subparsers(dest="action", required=True)
    for name in ("init", "show"):
        command = sub.add_parser(name)
        command.add_argument("--state-file", type=Path)
        command.add_argument("--topic")
    confirm = sub.add_parser("confirm")
    confirm.add_argument("--state-file", type=Path)
    confirm.add_argument("--topic")
    confirm.add_argument("--summary-file", type=Path, required=True)
    transition = sub.add_parser("transition")
    transition.add_argument("--state-file", type=Path)
    transition.add_argument("--to", choices=(*SEQUENCE[2:], *sorted(TERMINAL)), required=True)
    raise SystemExit(state_command(parser.parse_args()))


if __name__ == "__main__":
    main()
