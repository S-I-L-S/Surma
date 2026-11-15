#!/usr/bin/env python3
"""gen-translations -- generate README.<lang>.md from translations/<lang>.md.

Translation sources carry a small HTML-comment header:

    <!-- surma-translation: lang=uk status=unverified -->

status is one of:
    human       -- reviewed by a human (native speakers preferred)
    machine     -- machine translation, unreviewed
    unverified  -- agent- or human-drafted, awaiting owner review

Generated files get a one-line banner with that status, so readers always
know what they are looking at. --check verifies that regeneration is a
no-op (CI uses it; a stale README.<lang>.md fails the build).

Usage:
    python3 tools/gen-translations.py            # (re)generate
    python3 tools/gen-translations.py --check    # verify, no writes
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "translations"
HEADER = re.compile(r"<!--\s*surma-translation:\s*lang=(\S+)\s+status=(\S+)\s*-->")
BANNERS = {
    "human": "Translation: human-reviewed.",
    "machine": "Translation: machine draft, may be wrong.",
    "unverified": "Translation: unverified draft, awaiting owner review.",
}


def generate(src: Path) -> str:
    text = src.read_text(encoding="utf-8").lstrip("\ufeff")
    m = HEADER.search(text)
    if not m:
        raise ValueError(f"{src.name}: missing '<!-- surma-translation: lang=.. status=.. -->' header")
    lang, status = m.group(1), m.group(2)
    if status not in BANNERS:
        raise ValueError(f"{src.name}: unknown status '{status}'")
    body = HEADER.sub("", text, count=1).lstrip()
    return f"# Surma ({lang})\n\n> {BANNERS[status]}\n\n{body}"


def main() -> int:
    check = "--check" in sys.argv[1:]
    if not SRC.exists():
        print(f"no {SRC} directory", file=sys.stderr)
        return 1
    srcs = sorted(SRC.glob("*.md"))
    if not srcs:
        print("no translation sources found", file=sys.stderr)
        return 1

    fails = 0
    for src in srcs:
        try:
            rendered = generate(src)
        except ValueError as e:
            print(f"FAIL {e}")
            fails += 1
            continue
        lang = HEADER.search(src.read_text(encoding="utf-8")).group(1)
        dest = ROOT / f"README.{lang}.md"
        if dest.exists() and dest.read_text(encoding="utf-8") == rendered:
            print(f"  ok    {dest.name}")
            continue
        if check:
            print(f"  stale {dest.name} (regenerate with gen-translations.py)")
            fails += 1
        else:
            dest.write_text(rendered, encoding="utf-8")
            print(f"  wrote {dest.name}")

    print(f"{len(srcs)} source(s), {'stale' if fails else 'up to date'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
