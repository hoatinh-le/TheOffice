#!/usr/bin/env python3
"""Check every agents/*.md and commands/*.md frontmatter against .github/schema/frontmatter.json."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / ".github/schema/frontmatter.json").read_text())
KEY_LINE = re.compile(r"^([A-Za-z][\w-]*):\s*(.*)$")


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    fields = {}
    for line in lines[1:end]:
        m = KEY_LINE.match(line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def check(path, kind):
    rules = SCHEMA[kind]
    fields = parse_frontmatter(path.read_text())
    errors = []
    if fields is None:
        return [f"{path}: missing or malformed --- frontmatter block"]
    for key in rules["required"]:
        if not fields.get(key):
            errors.append(f"{path}: missing required frontmatter field '{key}'")
    if kind == "agent" and "model" in fields:
        if fields["model"] not in rules["model_values"]:
            errors.append(
                f"{path}: model '{fields['model']}' not one of {rules['model_values']}"
            )
    allowed = set(rules["required"]) | set(rules.get("optional", []))
    for key in fields:
        if key not in allowed:
            errors.append(f"{path}: unrecognized frontmatter field '{key}'")
    return errors


def main():
    errors = []
    for path in sorted((ROOT / "agents").glob("*.md")):
        errors += check(path, "agent")
    for path in sorted((ROOT / "commands").glob("*.md")):
        errors += check(path, "command")

    if errors:
        print(f"{len(errors)} frontmatter problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("All agent/command frontmatter OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
