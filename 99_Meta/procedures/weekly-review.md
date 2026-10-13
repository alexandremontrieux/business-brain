---
type: meta
tags: [meta/procedure]
status:
created: 2026-10-13
reviewed: 2026-10-13
origin: manual
related: ["[[_taxonomy]]"]
---

# Procedure: weekly-review (structure and freshness)

**Goal:** keep the graph healthy without touching content: surface what is stale, thin, duplicated or disconnected, as proposals or as a review note.

## Steps
1. Run `python _scripts/brain.py validate`, `index`, `stale`, `orphans`, `thin-positions`, `proposals`.
2. Rebuild `_index.*`. That is the only direct write; a broken link, even one whose target was simply renamed, goes into the review as a proposed fix.
3. Write `60_Proposals/YYYY-MM-DD weekly review.md` (`type: meta`, `origin: agent`, `proposal.action: review`, no target) containing:
   - **Validation errors** with the fix proposed for each.
   - **Stale notes** (reviewed > threshold): per note, one line saying whether it still looks right, and a suggested `reviewed` bump or an edit.
   - **Thin positions**: confidence not backed by evidence; suggest lowering confidence or name the evidence that is missing.
   - **Orphans** and **near-duplicates** (titles or aliases that overlap; notes sharing most tags and links), with merge suggestions.
   - **Unregistered tags** used by ≥2 notes, with a taxonomy proposal.
   - **Proposals older than 30 days**: drop or nudge.
   - **Graph shape**: the 5 most-linked notes and any tag with a single note, as a hint on where the brain is dense or thin.
4. Commit on `proposals/YYYY-MM-DD-review`.

## Rules
- Reorganising folders, renaming, merging: proposal only.
- Never change `schema.json` or `_taxonomy.md` directly.
