# Decision log

Decisions are recorded once and carry a date and a status. Re-opening a
decision means adding a new row, not editing history.

| Date       | Decision                                                                                       | Status   |
|------------|------------------------------------------------------------------------------------------------|----------|
| 2026-11-07 | Five-branch architecture: one shared layer over linux / linux+bsd / bsd / bsd+linux / windows  | accepted |
| 2026-11-07 | Sensor layer is kernel-independent: `surma-sensord` with pluggable backends                    | accepted |
| 2026-11-08 | Branch 5 ships no OS images: UEFI, ACPI, installer using official sources, shell only          | accepted |
| 2026-11-10 | Forking allowed where it saves time; own theme and icons preferred over CC-BY-SA derivatives   | accepted |
| 2026-11-11 | Order of work: branches 1-2 on phones first, BSD on non-phone hardware later, Windows last     | accepted |
| 2026-11-11 | Own code first; land a working base on one device, then replace foreign parts piece by piece   | accepted |
| 2026-11-11 | Light stack: musl, busybox, runit/OpenRC, wlroots/Smithay, zram; UI budget 1 GB RAM            | accepted |
| 2026-11-11 | Vendor blobs are never redistributed; pulled from the device at install time                   | accepted |
| 2026-11-11 | License for project code: GPL-3.0-or-later (AGPL-3.0 considered, rejected as server-oriented)  | accepted |
| 2026-11-11 | Device knowledge lives in TOML passports, one file per device, validated by tooling            | accepted |
| 2026-11-15 | Repository scaffold created in a local agent session from the claude.ai Surma project export   | accepted |

Notes on the two reversed-in-discussion points:

- **License.** The owner first leaned to AGPL-3.0; the chat concluded
  AGPL matters for servers, not for a system on a device, and repels
  contributors. GPL-3.0-or-later recorded; SDK/libraries to be split
  permissive later (LGPL/MPL/Apache) when third-party apps matter.
- **Halium.** Not adopted as-is. Used at most as a transitional backend
  inside `surma-sensord` while the own binder-based layer is built.
