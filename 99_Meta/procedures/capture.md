---
type: meta
tags: [meta/procedure]
status:
created: 2026-10-13
reviewed: 2026-10-13
origin: manual
related: ["[[_taxonomy]]"]
---

# Procedure: capture

**Goal:** get raw input into `00_Inbox/` fast, without judgement, so nothing is lost. Triage comes later.

## Inputs
- Text Alexandre types or pastes (Teams, mail, a thought).
- A web clipping (the Obsidian Web Clipper writes directly to `00_Inbox/`; nothing to do).
- A file or screenshot (goes to `_attachments/`, plus a one-line inbox note pointing at it).

## Steps
1. Create `00_Inbox/YYYY-MM-DD <short descriptive title>.md`.
2. Frontmatter: `origin` (manual / clipper / conversation / meetingbrain), `captured` (datetime), `source_refs` if any. No `type` yet: the inbox is untyped by design.
3. Body: the raw content, lightly cleaned (fix encoding, strip boilerplate). Do **not** summarise, retype or interpret; that is triage's job and it must see the original.
4. If Alexandre adds a remark ("this contradicts what I thought about X"), keep it verbatim in a `## Remark` section.

## Rules
- Never write into `10_`–`50_` from capture.
- One input, one inbox note. Do not merge inputs.
- Do not create the note if an identical one landed today (same title or same url).
