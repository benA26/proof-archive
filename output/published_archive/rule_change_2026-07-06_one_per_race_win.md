# Rule-change documentation — one-per-race WIN selection (effective 2026-07-06)

_Additive documentation note. It records a selection-rule version change for the Top-3 Picker and
changes no model, no probabilities, no report, and no archive. It is the prose companion to the hash
anchor `anchors/rule_amendment_2026-07-05.sha256.txt` (pushed as commit `9b122d1`) — that anchor is
authoritative for the file hashes; this note explains the change._

## What changed
The official **WIN** pick selection rule was amended on **2026-07-05**, **effective from 2026-07-06**.

- **Old rule (through 2026-07-05):** WIN picks were the top 3 runners by model win probability, which
  could include **more than one horse from the same race**.
- **New rule (from 2026-07-06):** WIN picks are **one-per-race** — at most one horse per race, keeping
  the highest-win-probability horse in each race — matching the PLACE-pick rule.

**PLACE picks were already one-per-race** and are unchanged by this amendment.

## Effective boundary (read this for any review)
- Reports **up to and including 2026-07-05** were produced under the **OLD** rule (same-race
  duplicates possible in the WIN set).
- Reports **from 2026-07-06 onward** are produced under the **NEW** one-per-race WIN rule.
- **Any performance review MUST label the pre-change and post-change periods separately.** Mixing
  them conflates two different selection rules and is not a like-for-like comparison.

## The old rule did produce same-race duplicates (at least once)
On **2026-07-05**, the published WIN set contained **two horses from the same race** — Conciliate and
Instant Force, both in the **Ayr 14:41**. That report was produced under the old rule and **stands as
published**. Under the new rule that day's WIN set would have kept only Conciliate (higher win
probability) and promoted the next distinct-race horse — but the published 2026-07-05 report is
**write-once and is NOT regenerated**.

## What this is NOT
- **Not a model retrain. Not a feature change.** `t3lib.py`, the model files, the feature lists, and
  the scoring **probabilities are unchanged**. Only the post-scoring selection step in `pick.py`
  changed (the WIN set now de-duplicates by race, exactly as the PLACE set already did).
- Amended `pick.py` SHA256: **9287F0CAD02F8146E3E56B2C074C8C4C133DAF5E5B51240BFE17F2185F3400A5**
  (as recorded in the existing anchor `anchors/rule_amendment_2026-07-05.sha256.txt`).

## Integrity
- **Historical reports remain write-once and must not be regenerated or edited.**
- This note is additive; it modifies no pick, report, archive, anchor, or log.

_Recorded 2026-07-05 (documentation companion to commit 9b122d1)._

---

## Addendum 2026-07-06 — scope correction: `log_picks.py` carried the old rule

**What was wrong.** The 2026-07-05 amendment changed the one-per-race WIN rule in `pick.py`
(the report generator) but **not** in `scripts/log_picks.py`, which builds the forward track
record `forward_log.csv` with its **own** independent WIN selection. `log_picks.py` still used
the old duplicate-allowing WIN rule. As a result the first forward-log day produced under the
"new" rule — **2026-07-06** — diverged from the published report: its logged WIN set contained
**two horses from the same race** (Alterity and Queen's Hame, both Ripon 18:39, race_id 1571205),
whereas the published one-per-race WIN set was Victory Gold / Alterity / Keep It Classic.

**Discovered and fixed same day (2026-07-06).**

- **Code fix.** `scripts/log_picks.py` WIN selection changed to `force_opr=True` (one line), so
  its WIN set now de-duplicates by race exactly as PLACE already did and as `pick.py` now does.
  `py_compile` clean.
  - New `log_picks.py` SHA256: **`09EF268214B7BE8E8C016F99FB0F871A6A6A930B9149EABC5F78EADBC7270250`**
- **2026-07-06 forward-log resolution.** The six 2026-07-06 rows were **re-logged in place with
  `--force` at 10:25 local — before any 2026-07-06 race had run** (first race off 15:15); all six
  rows were ungraded/pre-race, so no settled result was altered. This corrects a same-day clerical
  divergence only.
  - WIN set changed: old **Victory Gold / Alterity / Queen's Hame** (Queen's Hame was the same-race
    duplicate of Alterity) → published set **Victory Gold (1572933) / Alterity (1571205) /
    Keep It Classic (1571208, Ripon 20:15)**, three distinct race_ids.
  - PLACE rows unchanged in content (Alterity / Victory Gold / Roxelina).
  - **No other date's rows were touched:** all 138 non-07-06 rows verified byte-for-byte identical
    before and after (SHA256 of the non-07-06 subset unchanged: `d36885b8…`); total row count
    unchanged at 144.

**What this is NOT.** Not a model, feature, or probability change; `t3lib.py` and the model files
are untouched. Only `log_picks.py`'s post-scoring selection step changed, to match the already-
documented one-per-race rule. Historical reports remain write-once and were not regenerated.

_Recorded 2026-07-06._
