# Top-3 Picker — Public Proof Archive

An append-only, write-once record of the **Top-3 Picker's** daily published horse-racing selections, their
settled results, and their pre-race integrity anchors. **The model uses no odds.** This repository is a public
mirror of the selection proof only — it contains no code beyond the anchor tool, no data feeds, and no
operational internals.

## What's here
```
output/published_archive/
  top3_<date>.md              # the day's published WIN + PLACE picks (write-once, tamper-evident)
  results_<date>.md           # settled WIN results (£1 level stakes, Betfair BSP net 2% commission)
  treble_<date>.md            # the day's £1 each-way treble on the three WIN picks (bookmaker SP)
  anchors/top3_<date>.sha256.txt   # the integrity anchor for that day's archive
  proof_gap_*.md              # honest notes on any day whose external anchor was late
  rule_change_*.md            # documented selection-rule changes (write-once, never regenerated)
  proof_automation_*.md       # notes on how the pre-race push is automated
scripts/anchor_archive.py     # the tool that computes the anchor hashes
README.md
```

## How to verify a day's picks against its anchor hash
Each day's archive file `top3_<date>.md` is **write-once** and embeds the verbatim picks plus their
`picks_sha256` and `card_sha256`. Its companion anchor `anchors/top3_<date>.sha256.txt` records those hashes
**and** the `archive_sha256` — the SHA-256 of the archive file itself, fixed at publication.

To confirm a day's archive has not been altered since it was anchored:

1. Hash the archive file:
   - Linux/macOS: `sha256sum output/published_archive/top3_2026-08-03.md`
   - Windows: `Get-FileHash output/published_archive/top3_2026-08-03.md -Algorithm SHA256`
2. Compare the result to the `archive_sha256:` line in
   `output/published_archive/anchors/top3_2026-08-03.sha256.txt`.
3. **A match proves the archive is byte-for-byte the file that was anchored** — the picks, courses, times, and
   model probabilities inside it are exactly as published. The anchor also lists `picks_sha256` / `card_sha256`
   as additional fingerprints of the underlying picks and racecard.

**Pre-race timing.** From the launch date onward, each day's archive and anchor are committed and pushed to
**this public repository before the day's first race**. The external proof is the **push receipt time on
GitHub** — not the local commit time, which is forgeable via `git commit --date` (the anchor file itself notes
this). A pick file that appears here with a pre-race push therefore existed before the races were run.

## Provenance (honest note)
All archive files present at this repository's **launch (2026-08-03)** were **carried over from our private operational repository with their integrity hashes intact** — their
original pre-race push receipts live in that private repository. **Files from the launch date onward are pushed
to this public repository before racing begins each day.**

**Archive files are published verbatim and are never edited after hashing — not even cosmetically. Older files
therefore contain internal file paths from the publishing machine; we've left them exactly as hashed, because
an archive you can edit "just a little" is an archive you can edit.** (Files generated from the launch date
onward use repository-relative paths, so the machine paths appear only in the carried-over history.)

## What this is not
Not tips, not advice, not a betting service, and not a claim of profitability. Results are evaluated at
Betfair BSP (post-off, net of 2% commission) at £1 level stakes for transparency only. Past performance does
not predict future results; bet responsibly.
