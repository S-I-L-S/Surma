#!/bin/sh
# flash-guard -- deterministic gate in front of fastboot.
#
# usage: tools/flash-guard.sh devices/<name>.toml -- fastboot [args...]
#
# Refuses to run unless:
#   1. the passport exists and carries a codename,
#   2. the connected fastboot device reports the same product,
#   3. a human types the codename to confirm.
# Then -- and only then -- it execs the requested fastboot command.
#
# Nothing here writes to the device; flash-guard is the door, not the hand.

set -eu

if [ "$#" -lt 3 ] || [ "$2" != "--" ]; then
    echo "usage: flash-guard.sh <passport.toml> -- fastboot <args...>" >&2
    exit 2
fi
passport=$1; shift

if [ ! -f "$passport" ]; then
    echo "REFUSED: passport '$passport' not found" >&2
    exit 2
fi
expected=$(sed -n 's/^codename *= *"\([^"]*\)".*/\1/p' "$passport")
if [ -z "$expected" ]; then
    echo "REFUSED: passport has no codename" >&2
    exit 2
fi

# some fastboot builds wait forever with no device attached; bound the wait
if command -v timeout >/dev/null 2>&1; then
    getvar() { timeout 10 fastboot getvar "$1"; }
else
    getvar() { fastboot getvar "$1"; }
fi
actual=$(getvar product 2>&1 | sed -n 's/^(bootloader) product: *//p; s/^product: *//p' | head -n 1)
if [ -z "$actual" ]; then
    echo "REFUSED: no fastboot device found" >&2
    exit 3
fi

echo "passport codename : $expected"
echo "connected product : $actual"
if [ "$(printf '%s' "$actual" | tr '[:upper:]' '[:lower:]')" != "$expected" ]; then
    echo "REFUSED: device does not match passport" >&2
    exit 4
fi

printf 'type the codename to confirm: '
typed=""
if ! read -r typed; then
    echo "REFUSED: nothing typed" >&2
    exit 5
fi
if [ "$typed" != "$expected" ]; then
    echo "REFUSED: confirmation mismatch" >&2
    exit 5
fi

echo "ok: executing fastboot for '$expected'"
exec "$@"
