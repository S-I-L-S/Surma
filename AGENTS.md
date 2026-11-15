# AGENTS.md — working rules for agents in this repository

Owner-level laws live in [docs/style.md](docs/style.md); this file is
the agent-facing summary plus the safety machinery. When taste and this
file disagree, this file wins.

## Hard rules

1. **No emoji** in any user-facing file. ASCII, symbols, kaomoji only ( .-.
2. **Languages.** Every user-facing document exists in uk, ru, en at
   minimum. Translations live in `translations/`, generated files via
   `tools/gen-translations.py`; CI runs it with `--check`. Machine or
   agent drafts carry status `unverified` until the owner reviews them.
3. **Facts discipline.** Hardware claims are `verified` or `unverified`
   with a source. Never promote `unverified` to `verified` without a
   test log or an upstream link. When unsure, write `unknown`.
4. **Passports.** Device knowledge lives in `devices/<codename>.toml`
   only. Validate with `tools/passport-check.py`; keep format per
   [docs/device-passport.md](docs/device-passport.md).
5. **Destructive device operations** — `fastboot flash/erase`,
   `dd` to block devices, `mkfs` — must never run without, in order:
   passport match via `tools/flash-guard.sh`, partition backup via
   `tools/backup-partitions.sh`, typed human confirmation. `persist`
   and `modem` (and EFS where present) are backed up before anything
   else. No exceptions, regardless of model size or confidence.

## Background (owner context, recorded 2026-11)

- Owner: Sviatoslav Ihorovych Liada-Siverskyi (GitHub `Liada-Siverskyi`).
- Repos must look distinctive, beautiful, tidy; the owner likes elaborate
  structures and multi-language surfaces.
- Reference stand: Xperia 1 IV (`pdx224`); sandbox: Redmi Note 12 Turbo
  / POCO F5 (`marble`, unlocked bootloader). Experiments go to the
  sandbox, not the reference.
- Full project history: the claude.ai Surma project; local export dated
  2026-11-15 lives in the owner's documents directory.
- Work language with the owner: Russian or Ukrainian; repository
  language: English primary, translations per law 2.

## When an agent is unsure

Write `unknown`, mark `unverified`, and say so in the PR description.
Honest gaps age well; confident guesses brick phones.
