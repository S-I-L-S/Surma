# Devices

The collection doubles as the test bench. Sources: owner chats of
2026-11-07 and 2026-11-10; statuses are unverified until a passport
field carries a test log.

| Codename      | Device                             | SoC / platform            | Role       | Branches |
|---------------|------------------------------------|---------------------------|------------|----------|
| `pdx224`      | Sony Xperia 1 IV                   | SM8450 (SD 8 Gen 1)       | reference  | 1, 2     |
| `marble`      | Redmi Note 12 Turbo / POCO F5      | SM7475-AB (SD 7+ Gen 2)   | sandbox    | 1, 2, 5(r) |
| `lavender`    | Redmi Note 7                       | SDM660                    | collection | 1        |
| `tiare`       | Redmi Go                           | MSM8917 (SD 425)          | collection | 1        |
| `rolex`       | Redmi 4A                           | MSM8917 (SD 425)          | collection | 1        |
| `santoni`     | Redmi 4X                           | MSM8937 (SD 435)          | collection | 1        |
| `impad-9415`  | ImPAD 9415 tablet                  | Atom x3-C3230RK, Mali-450 | collection | 1 (quest)|

Working rules agreed in the chats:

- Xperia 1 IV is the main stand: device tree known to mainline efforts,
  official LineageOS support; modem, cameras and sensors still to be
  earned. The Redmi Note 12 Turbo is the sandbox — experiments happen
  there first, once the Xperia is in hand.
- The Windows branch (5) prefers a disposable bench; Lumia 950 XL is the
  cheap, proven Renegade candidate if the "Lumia-style" path is wanted.
- Every device keeps a [passport](devices/) — one TOML file: codename,
  SoC, bootloader state, sensor inventory, per-OS support status with
  provenance. Format in [device-passport.md](device-passport.md).
- Before any flash: persist and modem (and EFS where present) are dumped.
  Those partitions hold calibrations and IMEI; losing them is hardware
  pain, not data loss.

Collection wishlist from the 2026-11-10 chat (not passports yet): Sony
from 2012 on, Samsung S-series up to S24, selected Xiaomi/Mi, Apple up
to iPhone 15 Pro Max, Lumia family, Nubia Z, Tecno Slim, Nothing Phone,
OnePlus, Meizu MX4 / Pro 5 (official Ubuntu Phones), Sharp, plus the
historical bench: Nokia N900/N9, Palm Pre, BlackBerry Passport, Fairphone,
PinePhone, Librem 5, Pixels.

Openness, from the same chat: easiest — Nothing, OnePlus, Xiaomi/Redmi,
Sony; medium — Samsung S (Knox), Nubia, Tecno; hardest — Apple (checkm8
ceases at iPhone X), Lumia/Surface boot chains.
