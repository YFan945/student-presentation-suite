#!/usr/bin/env python3
"""Generate and validate a minimal PPTX through the runtime wrapper."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="student-presentation-smoke-") as tmp:
        work = Path(tmp)
        pptx = work / "smoke-presentation.pptx"
        notes = work / "smoke-speaker-notes.md"
        preview = work / "smoke-preview.png"
        deck_script = work / "deck.js"
        deck_script.write_text(
            """
const pptxgen = require("pptxgenjs");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
slide.addText("Claude Code PPTX smoke test", {x: 0.8, y: 0.8, w: 8, h: 0.6, fontSize: 30});
slide.addText("Runtime resolution and delivery validation", {x: 0.8, y: 1.8, w: 8, h: 0.5, fontSize: 22});
pptx.writeFile({ fileName: process.argv[2] });
""",
            encoding="utf-8",
        )
        subprocess.run(
            [
                "node",
                str(ROOT / "scripts/run_with_pptxgenjs.js"),
                str(deck_script),
                str(pptx),
            ],
            check=True,
        )
        notes.write_text("# Speaker notes\n\nSmoke test.", encoding="utf-8")
        Image.new("RGB", (640, 360), "white").save(preview)
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "skills/student-presentation-ppt/scripts/pptx_delivery_check.py"),
                "--pptx",
                str(pptx),
                "--notes",
                str(notes),
                "--preview",
                str(preview),
                "--strict",
                "--json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(proc.stdout)
        if result.get("slide_count") != 1 or result.get("missing_expected_files"):
            raise SystemExit(f"Unexpected smoke result: {result}")
        print(json.dumps({"ok": True, "slide_count": 1}, indent=2))


if __name__ == "__main__":
    main()
