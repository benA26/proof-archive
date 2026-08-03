# Proof automation - 2026-07-09

_Operations note. This does not alter picks, models, cards, or historical proof records._

## Problem

The daily Top-3 Picker archive was being created locally by `scripts/run_daily_morning.ps1`, but external anchoring still required a separate manual Git step. That caused the 2026-07-08 and 2026-07-09 archives to be published locally pre-race but pushed late, forcing honest late-anchor labels.

## Local runner change

The local 07:00 runner `scripts/run_daily_morning.ps1` has been updated on this machine to perform the proof step immediately after the immutable archive exists:

1. Run the normal daily flow: `pick`, `log_picks`, `f4_shadow`, `archive_picks`, `mobile_report`.
2. Create the write-once anchor with `scripts/anchor_archive.py --date <today>` if it does not already exist.
3. Stage **only**:
   - `output/published_archive/top3_<today>.md`
   - `output/published_archive/anchors/top3_<today>.sha256.txt`
4. Commit with message `Publish Top-3 archive <today>` if those two files changed.
5. Push `main` to `origin`.

The idempotency path was also updated: if today's archive already exists, the runner does **not** rerun model scripts or overwrite the archive; it only attempts to create/push the missing proof anchor.

## Safety boundaries

- No broad `git add`.
- No model files staged.
- No cards outside the immutable published archive staged.
- No logs staged.
- No `--force` archive overwrite.
- If the proof push fails, the runner logs the failure and exits non-zero so the missed proof is visible.

## Repository allowlist note

The `top3-proof` repo intentionally ignores almost everything. It tracks `output/published_archive/**` and `scripts/anchor_archive.py`, but not the local runner script. Therefore this note records the automation design in the proof archive without weakening the strict allowlist or adding operational code to the proof repo.

## Expected effect

From the next successful 07:00 run, the archive and anchor should be committed and pushed before racing, assuming network access to GitHub is available. If GitHub is unavailable, the day must still be labelled honestly as a late anchor when pushed later.
