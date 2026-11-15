#!/usr/bin/env python3
"""passport-check -- validate device passports (TOML, schema 1).

Usage:
    python3 tools/passport-check.py [devices/*.toml]

Checks required keys, value domains, and cross-file consistency.
Exit code 1 on any failure; prints a per-file report.
"""
import sys
import tomllib
from pathlib import Path

REQUIRED_STR = ("codename", "vendor", "soc", "bootloader", "role")
REQUIRED_KEYS = REQUIRED_STR + ("schema", "marketing", "sensors", "branch_targets",
                                "mainline", "halium", "pmos")
STATUSES = {"works", "partial", "does-not-boot", "does-not-apply", "unknown"}
ROLES = {"reference", "sandbox", "collection", "retired"}
BRANCHES = {1, 2, 3, 4, 5}


def check(path: Path) -> list[str]:
    errs = []
    try:
        with open(path, "rb") as f:
            d = tomllib.load(f)
    except Exception as e:
        return [f"{path.name}: unreadable TOML: {e}"]

    for k in REQUIRED_KEYS:
        if k not in d:
            errs.append(f"{path.name}: missing required key '{k}'")
    if errs:
        return errs

    cn = d["codename"]
    if not isinstance(cn, str) or not cn or cn != cn.lower() \
            or not all(c.isalnum() or c == "-" for c in cn):
        errs.append(f"{path.name}: codename must be lowercase [a-z0-9-]")
    if path.stem != cn:
        errs.append(f"{path.name}: filename stem '{path.stem}' != codename '{cn}'")

    if d["schema"] != 1:
        errs.append(f"{path.name}: schema must be 1, got {d['schema']!r}")
    if not isinstance(d["marketing"], list) or not d["marketing"]:
        errs.append(f"{path.name}: marketing must be a non-empty list")
    if not isinstance(d["sensors"], list) or not d["sensors"]:
        errs.append(f"{path.name}: sensors must be a non-empty list")
    if d["role"] not in ROLES:
        errs.append(f"{path.name}: role must be one of {sorted(ROLES)}")

    bt = d["branch_targets"]
    if not isinstance(bt, list) or not bt or not set(bt) <= BRANCHES:
        errs.append(f"{path.name}: branch_targets must be a non-empty subset of {sorted(BRANCHES)}")

    for k in ("mainline", "halium", "pmos"):
        v = d.get(k, {})
        if not isinstance(v, dict) or v.get("status") not in STATUSES:
            errs.append(f"{path.name}: {k}.status must be one of {sorted(STATUSES)}")
        if not isinstance(v, dict) or not isinstance(v.get("source"), str) or not v.get("source"):
            errs.append(f"{path.name}: {k}.source must carry provenance (even 'unverified')")

    text = path.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        emoji_like = [c for c in line if 0x1F300 <= ord(c) <= 0x1FAFF or c in "✅❌🎉🚀🔥"]
        if emoji_like:
            errs.append(f"{path.name}:{i}: emoji found (style law 1)")
    return errs


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]] or sorted(Path("devices").glob("*.toml"))
    if not paths:
        print("no passports found", file=sys.stderr)
        return 1
    fails = 0
    rows = []
    for p in paths:
        errs = check(p)
        fails += bool(errs)
        try:
            d = tomllib.load(open(p, "rb"))
            rows.append(f"{d.get('codename', '?'):12} {d.get('role', '?'):10} branches={d.get('branch_targets', '?')}")
        except Exception:
            rows.append(f"{p.name:12} <unreadable>")
        for e in errs:
            print("FAIL", e)
    print()
    for r in rows:
        print("  ", r)
    print(f"\n{len(paths)} passports, {fails} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
