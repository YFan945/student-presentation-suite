#!/usr/bin/env python3
"""Validate Student Presentation Slide Spec YAML."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_optional_dependencies():
    try:
        import jsonschema
        import yaml
    except ImportError as exc:
        print(
            "Missing dependency. Install plugin validation dependencies with: "
            "python -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(3) from exc
    return jsonschema, yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Slide Spec YAML")
    parser.add_argument("spec", type=Path, help="Slide Spec YAML file")
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "references" / "slide-spec.schema.json",
        help="JSON Schema path",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    jsonschema, yaml = load_optional_dependencies()
    try:
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        data = yaml.safe_load(args.spec.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    except OSError as exc:
        result = {"valid": False, "error": str(exc), "errors": []}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Slide Spec validation failed: {exc}")
        raise SystemExit(2) from exc

    result = {
        "valid": not errors,
        "error_count": len(errors),
        "errors": [
            {
                "path": "." + ".".join(str(part) for part in error.path),
                "message": error.message,
            }
            for error in errors
        ],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("Slide Spec is invalid:")
        for error in result["errors"]:
            print(f"- {error['path']}: {error['message']}")
    else:
        print("Slide Spec is valid.")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
