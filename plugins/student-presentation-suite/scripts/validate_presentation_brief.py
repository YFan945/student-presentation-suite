#!/usr/bin/env python3
"""Validate a Student Presentation Brief YAML/JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Student Presentation Brief")
    parser.add_argument("brief", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "references" / "presentation-brief.schema.json",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        import jsonschema
        import yaml
    except ImportError as exc:
        print("Install requirements.txt before validating briefs.", file=sys.stderr)
        raise SystemExit(3) from exc
    try:
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        raw = args.brief.read_text(encoding="utf-8")
        data = json.loads(raw) if args.brief.suffix.lower() == ".json" else yaml.safe_load(raw)
        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    except (OSError, json.JSONDecodeError, yaml.YAMLError, jsonschema.SchemaError) as exc:
        result = {"valid": False, "error": str(exc), "errors": []}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else str(exc))
        raise SystemExit(2) from exc
    items = [
        {
            "path": "." + ".".join(str(part) for part in error.path),
            "message": error.message,
        }
        for error in errors
    ]
    result = {"valid": not items, "error_count": len(items), "errors": items}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif items:
        for item in items:
            print(f"- {item['path']}: {item['message']}")
    else:
        print("Presentation Brief is valid.")
    if items:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
