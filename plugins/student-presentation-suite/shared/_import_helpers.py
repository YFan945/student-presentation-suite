"""Helpers for importing shared modules from plugin-root-relative paths."""

from __future__ import annotations

import sys
from pathlib import Path


def load_inspect_pptx(script_path: str | Path) -> type:
    """Import and return the shared ``inspect_pptx`` function.

    Adds the plugin root to ``sys.path`` temporarily to resolve the
    ``shared`` package, then cleans up after itself.  Safe to call
    multiple times — repeated calls are cached by the import system.
    """
    plugin_root = Path(script_path).resolve().parents[3]
    root_str = str(plugin_root)
    added = root_str not in sys.path
    if added:
        sys.path.insert(0, root_str)
    try:
        from shared import inspect_pptx
    finally:
        if added:
            try:
                sys.path.remove(root_str)
            except ValueError:
                pass
    return inspect_pptx
