# Licensing

Status: recorded decision, not legal advice. Before any public release,
check per-package licenses again.

## Project code

GPL-3.0-or-later (`LICENSE` in the repository root). Chosen over
AGPL-3.0 in the 2026-11-11 chat: AGPL protects server deployments; a
system running on a device does not need it, and it repels a part of
developers and manufacturers. The kernel stays GPL-2.0-only — that is
not negotiable and not ours to change. Userspace programs are separate
works and may carry their own licenses.

When a Surma SDK / libraries become a thing third parties build apps
against, they are expected to move to softer terms (LGPL, MPL or
Apache-2.0) so that applications are not forced into copyleft.

## Forking, brands, looks

- Forking GPL/LGPL code (Lomiri and friends) is fine: modify, rename,
  distribute — keep copyright notices, keep the same license for
  changes, never close it. Honest attribution ("based on Lomiri /
  UBports") earns trust rather than costing it.
- "Ubuntu", the circle of friends, and related marks are Canonical
  trademarks: stripped, everywhere.
- Ubuntu font: under its licence, modified versions must be renamed.
- Suru icons and stock wallpapers: CC-BY-SA — attribution and share-alike
  obligations attach. The clean path is an own theme and own icons,
  which also gives Surma its own face.

## Vendor blobs

Modem, camera ISP, DSP and bootloader firmware run on separate signed
processors; rewriting them is out of reach. Surma therefore never
redistributes blobs: they are extracted from the device's own firmware
at install time, the postmarketOS / Halium pattern. Legally clean, and
device coverage survives.

## Windows branch

Windows itself is never distributed. The repository carries what lives
around it: UEFI firmware work (Renegade-line), ACPI tables per device,
an installer that fetches the image from official sources (Microsoft
tools or UUP dump) operated by the user, and the Surma shell on top.
