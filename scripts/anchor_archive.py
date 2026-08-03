"""External-proof anchor candidate for a day's published Top-3 Picker archive.

ANCHOR / PROOF-PREP ONLY. Reads an existing immutable archive under
output/published_archive/top3_YYYY-MM-DD.md, extracts its recorded hashes,
computes the SHA256 of the archive file itself, and writes a small anchor file
under output/published_archive/anchors/.

It never modifies the archive, the picks report, the card, forward_log.csv,
models, feature lists, or any live script. Stdlib only; no model code imported.

KEY PRINCIPLE: this anchor file is NOT external proof on its own. It only
prepares a payload. External evidential value comes ONLY from pushing it to a
third-party service (a git remote), where the *push receipt time on the remote*
is the external timestamp. Local commit dates are forgeable (git commit --date),
so the local commit time is worth nothing as evidence.

WRITE-ONCE: never overwrites an existing anchor. There is deliberately no
--force flag. If an anchor is ever wrong, do NOT replace it — write a new
versioned file (top3_YYYY-MM-DD.sha256.v2.txt) with a note explaining why.

Usage:
    python scripts/anchor_archive.py --date YYYY-MM-DD
"""
from __future__ import annotations
import argparse
import hashlib
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ARCH_DIR = PROJECT / "output" / "published_archive"
ANCHOR_DIR = ARCH_DIR / "anchors"


def _rel(p):
    """Repo-relative posix path for anchor metadata — keeps the machine/username out of public anchors.
    Falls back to the bare filename if not under the project root (never raises)."""
    try:
        return p.resolve().relative_to(PROJECT).as_posix()
    except Exception:
        return p.name

NOT_PROOF_NOTE = (
    "external proof anchor candidate — not external proof until pushed to remote "
    "(the external timestamp is the push receipt time on the remote, "
    "not the local commit time, which is forgeable via git commit --date)"
)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def extract_field(lines: list[str], prefix: str) -> str | None:
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    args = ap.parse_args()
    date = args.date

    arch = ARCH_DIR / f"top3_{date}.md"
    if not arch.exists():
        print(f"No archive for {date} ({arch}); nothing to anchor.")
        print("Run scripts/archive_picks.py first.")
        return 1

    anchor = ANCHOR_DIR / f"top3_{date}.sha256.txt"
    if anchor.exists():
        print(f"REFUSING: anchor already exists: {anchor}")
        print("Anchors are write-once. There is no --force.")
        print("If this anchor is wrong, write a new versioned file "
              f"(top3_{date}.sha256.v2.txt) with a note explaining why — never replace.")
        return 1

    lines = arch.read_text(encoding="utf-8").splitlines()
    published = extract_field(lines, "- published:")
    picks_sha = extract_field(lines, "- picks_sha256:")
    card_sha = extract_field(lines, "- card_sha256:")

    if not picks_sha:
        print(f"Could not find picks_sha256 in {arch}; aborting.")
        return 1

    archive_sha = sha256(arch)
    generated = datetime.now().astimezone()

    ANCHOR_DIR.mkdir(exist_ok=True)

    body = [
        f"# External proof anchor candidate — Top-3 Picker {date}",
        "",
        f"date:              {date}",
        f"archive_timestamp: {published if published else '(not found)'}",
        f"picks_sha256:      {picks_sha}",
        f"card_sha256:       {card_sha if card_sha else '(not found)'}",
        f"archive_path:      {_rel(arch)}",
        f"archive_sha256:    {archive_sha}",
        f"generated:         {generated.strftime('%Y-%m-%d %H:%M:%S %Z')} (local)",
        "",
        f"NOTE: {NOT_PROOF_NOTE}",
        "",
    ]
    anchor.write_text("\n".join(body), encoding="utf-8")

    print(f"anchor -> {anchor}")
    print(f"  date:              {date}")
    print(f"  archive_timestamp: {published}")
    print(f"  picks_sha256:      {picks_sha}")
    print(f"  card_sha256:       {card_sha}")
    print(f"  archive_sha256:    {archive_sha}")
    print(f"  NOTE: {NOT_PROOF_NOTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
