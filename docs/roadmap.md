# Roadmap

Order fixed in the 2026-11-11 chat: branches 1-2 on phones first, BSD on
non-phone hardware later, Windows last. Milestones re-order nothing;
they only sequence within that frame.

- **M0 — scaffold (this commit).** Decision log, architecture, passport
  format, seven passports, safety tools skeleton, translation pipeline,
  CI. Repository exists; nothing boots yet.
- **M1 — passports and safety tools hardened.** `flash-guard` and
  `backup-partitions` exercised end-to-end on a zeroed device; passport
  checker wired into CI; every collection device carries a passport.
- **M2 — branch 1 boots on `pdx224`.** Mainline-first base,
  postmarketOS-style; HAL/Halium fallback stays an open option per the
  2026-11-10 chat ("кучу сборок — и халиум, и как postmarketOS").
- **M3 — `surma-sensord` prototype.** iio backend first; qcom-ssc
  research on `marble` (libssc + hexagonrpcd, /usr/share/qcom data
  files); measurements from day one.
- **M4 — branch 2.** Same kernel, BSD userland, Chimera pattern;
  expected cheap once branch 1 stands.
- **M5 — branch 3.** Pure BSD on a laptop / x86 tablet; phones stay
  closed to it for now.
- **M6 — branch 5 research.** Renegade device list checked against
  SM8450 / SM7475; port-from-scratch costed if absent; Lumia 950 XL
  bench considered; no OS images ever shipped.
- **M7 — Android compatibility module.** Lazy Waydroid-class container,
  started on demand; own runtime stays a far-future direction.

Standing work, every milestone: passports updated with provenance,
translations regenerated, memory discipline (smem / ps_mem graphs per
build), no emoji anywhere.
