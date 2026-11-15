#!/bin/sh
# backup-partitions -- dump critical partitions from a rooted device over adb.
#
# usage: tools/backup-partitions.sh devices/<name>.toml [partition ...]
# default partitions: persist modem boot vendor efs
# (efs is skipped automatically when the partition does not exist)
#
# Requirements: rooted device (su available), adb authorized.
# Order of operations is fixed: codename check, then dump, then checksum.
# This script never flashes anything; it only reads.
#
# Why persist/modem/EFS first: calibrations and IMEI live there. Losing
# them is hardware pain that no amount of data backup cures.

set -eu

if [ "$#" -lt 1 ]; then
    echo "usage: backup-partitions.sh <passport.toml> [partition ...]" >&2
    exit 2
fi
passport=$1; shift
parts=${*:-"persist modem boot vendor efs"}

if [ ! -f "$passport" ]; then
    echo "REFUSED: passport '$passport' not found" >&2
    exit 2
fi
expected=$(sed -n 's/^codename *= *"\([^"]*\)".*/\1/p' "$passport")
if [ -z "$expected" ]; then
    echo "REFUSED: passport has no codename" >&2
    exit 2
fi

state=$(adb get-state 2>/dev/null || true)
if [ "$state" != "device" ]; then
    echo "REFUSED: adb device not in 'device' state (got: '$state')" >&2
    exit 3
fi
actual=$(adb shell getprop ro.product.device | tr -d '\r\n')
if [ "$(printf '%s' "$actual" | tr '[:upper:]' '[:lower:]')" != "$expected" ]; then
    echo "REFUSED: adb device '$actual' does not match passport '$expected'" >&2
    exit 4
fi

stamp=$(date -u +%Y%m%dT%H%M%SZ)
dest="backups/$expected/$stamp"
mkdir -p "$dest"
echo "codename: $expected -> $dest"

rc=0
for part in $parts; do
    path="/dev/block/bootdevice/by-name/$part"
    if ! adb shell su -c "test -e '$path'" >/dev/null 2>&1; then
        echo "  skip  $part (no such partition on this device)"
        continue
    fi
    echo "  dump  $part"
    adb shell su -c "dd if='$path' of=/sdcard/surma-$part.img" >/dev/null 2>&1 \
        && adb pull "/sdcard/surma-$part.img" "$dest/$part.img" >/dev/null 2>&1 \
        && adb shell su -c "rm -f /sdcard/surma-$part.img" >/dev/null 2>&1 \
        || { echo "  FAIL  $part" >&2; rc=1; }
done

if [ "$rc" -eq 0 ]; then
    ( cd "$dest" && sha256sum ./*.img > SHA256SUMS 2>/dev/null || true )
    echo "done: $(ls "$dest" | grep -c '\.img$') partition image(s), checksums written"
else
    echo "completed with failures; see the FAIL lines above" >&2
fi
exit "$rc"
