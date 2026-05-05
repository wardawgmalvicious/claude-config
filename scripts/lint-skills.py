#!/usr/bin/env python3
"""Validate SKILL.md frontmatter against repo conventions.

Usage: lint-skills.py <SKILL.md path>...

Exits 0 if every file passes, 1 if any file fails, 2 on usage error.
Output: one line per failure: <filepath>:<rule>: <message>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^[a-z0-9-]+$")
NAME_CHAR_RE = re.compile(r"[a-z0-9-]")
RESERVED_WORDS = ("anthropic", "claude")
NAME_MAX = 64
DESCRIPTION_MAX = 1024
BODY_MAX_LINES = 500
FRONTMATTER_SCAN_LINES = 50
BOM = b"\xef\xbb\xbf"


def lint_file(path: Path) -> list[str]:
    failures: list[str] = []

    def fail(rule: str, msg: str) -> None:
        failures.append(f"{path}:{rule}: {msg}")

    raw = path.read_bytes()
    if raw.startswith(BOM):
        fail("no-bom", "BOM detected; remove.")
        raw = raw[len(BOM):]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        fail("utf-8", f"file is not valid UTF-8: {e}")
        return failures

    lines = text.splitlines()

    if not lines or lines[0] != "---":
        fail("frontmatter", "missing or malformed YAML frontmatter (no opening ---).")
        return failures

    closing = None
    for i in range(1, min(FRONTMATTER_SCAN_LINES, len(lines))):
        if lines[i] == "---":
            closing = i
            break
    if closing is None:
        fail("frontmatter", f"missing or malformed YAML frontmatter (no closing --- within first {FRONTMATTER_SCAN_LINES} lines).")
        return failures

    fm_text = "\n".join(lines[1:closing])
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        fail("frontmatter-yaml", f"YAML parse error: {e}")
        return failures

    if not isinstance(fm, dict):
        fail("frontmatter-yaml", "frontmatter is not a YAML mapping.")
        return failures

    name = fm.get("name")
    if name is None:
        fail("name-required", "missing required field `name`.")
    elif not isinstance(name, str):
        fail("name-type", f"`name` must be a string, got {type(name).__name__}.")
    elif name == "":
        fail("name-empty", "`name` is empty.")
    else:
        if len(name) > NAME_MAX:
            fail("name-length", f"`name` length {len(name)} exceeds {NAME_MAX}.")
        if not NAME_RE.match(name):
            bad = sorted({c for c in name if not NAME_CHAR_RE.match(c)})
            fail("name-charset", f"`name` contains disallowed character(s): {bad!r}; allowed: lowercase letters, digits, hyphens.")
        lowered = name.lower()
        for word in RESERVED_WORDS:
            if word in lowered:
                fail("name-reserved", f"`name` contains reserved word {word!r}.")

    desc = fm.get("description")
    if desc is None:
        fail("description-required", "missing required field `description`.")
    elif not isinstance(desc, str):
        fail("description-type", f"`description` must be a string, got {type(desc).__name__}.")
    elif len(desc) > DESCRIPTION_MAX:
        fail("description-length", f"`description` length {len(desc)} exceeds {DESCRIPTION_MAX}.")

    if "paths" in fm:
        paths_field = fm["paths"]
        if isinstance(paths_field, str):
            fail("paths-type", "`paths` must be a YAML list, not a string.")
        elif not isinstance(paths_field, list):
            fail("paths-type", f"`paths` must be a YAML list, got {type(paths_field).__name__}.")
        else:
            for i, entry in enumerate(paths_field):
                if not isinstance(entry, str) or entry == "":
                    fail("paths-entry", f"`paths[{i}]` must be a non-empty string.")

    body_lines = lines[closing + 1:]
    if len(body_lines) > BODY_MAX_LINES:
        fail("body-length", f"body length {len(body_lines)} lines exceeds {BODY_MAX_LINES}.")

    return failures


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: lint-skills.py <SKILL.md>...", file=sys.stderr)
        return 2

    all_failures: list[str] = []
    for arg in argv[1:]:
        path = Path(arg)
        if not path.is_file():
            all_failures.append(f"{path}:file: not a file.")
            continue
        all_failures.extend(lint_file(path))

    for line in all_failures:
        print(line)

    return 0 if not all_failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
