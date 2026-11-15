# Surma

Surma is a mobile-first operating system umbrella: one shared userland
(`surma-shell`, `surma-apps`, `surma-sensord`) running on top of several
swappable foundations — Linux, BSD, and (last) a Windows boot path.
Targets are phones, tablets, and other small devices, with a hard budget:
a working interface in 1 GB of RAM or less.

The project is written to be as self-made as practical: own shell, own
sensor daemon, own device-port format, own translation pipeline. Vendor
code is used where it must be (modem firmware, signed boot chains), but it
is never redistributed — it is pulled from the device itself at install time.

## Shape

```
        surma-shell / surma-apps / surma-sensord
                          |
     +---------+----------+----------+---------+
     |         |          |          |         |
   [1]       [2]        [3]        [4]        [5]
   linux    linux+bsd    bsd      bsd+linux   windows
```

| # | Branch    | Base idea                                                     | Status   |
|---|-----------|---------------------------------------------------------------|----------|
| 1 | linux     | mainline-first mobile Linux, postmarketOS-style               | planned  |
| 2 | linux+bsd | Linux kernel with a BSD userland, Chimera-style               | planned  |
| 3 | bsd       | pure BSD on laptops, servers, x86 tablets                     | planned  |
| 4 | bsd+linux | FreeBSD with Linuxulator and LinuxKPI                         | planned  |
| 5 | windows   | Renegade UEFI + user-supplied Windows ARM64 image, Surma shell on top | research |

Branch 5 ships no operating system images: the repository carries UEFI
firmware work, ACPI tables, an installer that uses official sources, and
the shell. See [licensing](docs/licensing.md).

## Current state

This repository is a scaffold: decision log, architecture notes, device
passports, and safety tooling exist; no runnable OS code yet. The honest
order of work is in the [roadmap](docs/roadmap.md).

## Documentation

- [Architecture](docs/architecture.md) — shared layer, branches, sensor stack
- [Decisions](docs/decisions.md) — decision log with dates and status
- [Devices](docs/devices.md) — the collection and the reference stands
- [Device passport format](docs/device-passport.md) — one TOML file per device
- [Licensing](docs/licensing.md) — what is GPL, what is pulled, what is never distributed
- [Style laws](docs/style.md) — rules every contribution follows
- [Roadmap](docs/roadmap.md) — milestones and order of work

## Reference stands

- Sony Xperia 1 IV (`pdx224`) — reference device, mainline-first target
- Redmi Note 12 Turbo / POCO F5 (`marble`) — sandbox, experiments live here

Everything else in the collection is catalogued in [devices](devices/).

## Repository laws

1. No emoji, anywhere. ASCII, symbols, and kaomoji only ( .-.
2. Every user-facing document exists in uk, ru, and en at minimum; more
   languages are generated through `tools/gen-translations.py`, machine
   drafts are marked as such, native-speaker PRs are invited.
3. Hardware facts are either verified or marked unverified, with a source.
   Nothing in between.
4. Destructive device operations are gated, in this order: passport check,
   partition backup, typed human confirmation.

## Translations

Read in: [українська](README.uk.md), [русский](README.ru.md).
See `tools/gen-translations.py` for the pipeline and
`translations/` for sources.

## License

GPL-3.0-or-later for project code; see [LICENSE](LICENSE) and the
[licensing notes](docs/licensing.md).
