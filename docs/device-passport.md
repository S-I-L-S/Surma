# Device passport format

One TOML file per device, named by codename: `devices/<codename>.toml`.
Validated by `tools/passport-check.py`. The passport is the single place
where device knowledge lives; scripts and agents read it instead of
guessing.

Schema version 1:

```toml
schema      = 1                       # required, integer
codename    = "marble"                # required, lowercase [a-z0-9-]
vendor      = "Xiaomi"                # required
marketing   = ["POCO F5", "Redmi Note 12 Turbo (China)"]  # required, >= 1
soc         = "Snapdragon 7+ Gen 2 (SM7475-AB)"           # required
ram         = "8/12 GB LPDDR5"        # optional
storage     = "256/512 GB UFS 3.1"    # optional

bootloader  = "unlockable; unlocked on the owner's unit"  # required, prose

sensors     = ["accelerometer", "gyroscope", "light", "proximity"]  # required
sensors_note = "modern Qualcomm: via Snapdragon Sensor Core DSP"     # optional

role          = "sandbox"            # required: reference | sandbox | collection | retired
branch_targets = [1, 2]              # required, subset of 1..5

mainline = { status = "unknown",  source = "unverified" }   # required
halium   = { status = "unknown",  source = "unverified" }   # required
pmos     = { status = "unknown",  source = "unverified" }   # required

notes = "free-form prose"              # optional
```

Rules:

1. `status` values: `works`, `partial`, `does-not-boot`,
   `does-not-apply` (the OS path makes no sense for this device),
   `unknown`. Anything not proven by a log or an upstream link stays
   `unknown`.
2. `source` carries provenance: `unverified`, or a pointer —
   `owner chat 2026-11-07`, `pmos wiki <url>`, `test log <date>`.
3. `branch_targets` numbers match the five branches in
   [architecture.md](architecture.md).
4. `codename` must equal the fastboot/adb-reported product or device
   name; `tools/flash-guard.sh` and `tools/backup-partitions.sh` refuse
   to run on a mismatch.
5. No emoji in passports; prose stays ASCII.

A passport with unknown statuses is still a valid passport — it is the
honest starting point, and it ages into the filled one.
