---
type: meta
tags: [meta/procedure]
status:
created: 2026-10-13
reviewed: 2026-10-13
origin: manual
related: ["[[_taxonomy]]"]
---

# Procedure: daily-scan (Meetingbrain → proposals)

**Goal:** every day, read the meeting notes that changed since the last scan and propose what belongs in the brain. Alexandre reviews proposals when he wants; nothing is applied automatically.

## Configuration
`brain.config.json` → `sources.meetingbrain.path` (the Meetingbrain folder, local override in `brain.config.local.json`), `sources.meetingbrain.exclude` (e.g. Inbox, Claude outputs). Last run is recorded in `99_Meta/scan-state.json`.

## Steps
1. List Meetingbrain notes with mtime newer than `last_scan`. Skip excluded folders. If none, write "no changes" to the changelog and stop.
2. Load `_index.json`. For each changed meeting note, look for:
   - **New concepts** explained or used that have no note (→ `note` proposal).
   - **Methods or structures** described that look reusable (→ `framework` proposal).
   - **Claims Alexandre made or defended** ("we should…", "I think…", "never do X") (→ `position` proposal, or `update` to an existing position with new evidence).
   - **Clients, tools, offerings, standards** that recur (→ `entity` proposal when seen in ≥2 meetings or clearly central).
   - **Contradictions** with an existing note or position (→ `update` proposal quoting both).
3. Be selective: at most 5 proposals per day; prefer updates to existing notes over new ones; skip anything that is a to-do or project status rather than knowledge.
4. Write each proposal into `60_Proposals/` with `origin: meetingbrain`, `proposal.source_refs` pointing at the meeting note(s), and the quoted passage that triggered it in a `## Evidence from meetings` section. Sanitise: no client-confidential figures, no third-party personal details beyond role.
5. Update `scan-state.json`, append a summary line to `changelog.md`, run `brain.py validate`, commit on branch `proposals/YYYY-MM-DD-scan` (or open a PR if a remote is available).

## Rules
- Never write to `10_`–`50_`.
- Never set `reviewed`.
- A proposal must stand alone: someone reading only the proposal file must be able to decide.
