---
type: meta
tags: [meta/procedure]
status:
created: 2026-10-13
reviewed: 2026-10-13
origin: manual
related: ["[[_taxonomy]]"]
---

# Procedure: triage

**Goal:** move items out of `00_Inbox/` into the vault as properly typed, tagged and linked notes, with Alexandre deciding.

## Operating mode: propose first
1. Read every item in `00_Inbox/`. Run `python _scripts/brain.py index` and read `99_Meta/_index.json` to know what exists.
2. For each item, write a proposal into `60_Proposals/` (template `90_Templates/proposal.md`) **or**, in an interactive session, present it in chat and stop for approval. One item at a time.
3. Apply only after approval. Never delete the inbox item; after applying, move it to `00_Inbox/_processed/` (excluded from the dashboard; Alexandre empties it).
4. If unsure about type or links, say so. Do not guess confidently.

## For each item, propose
- **Title**: cleaned, descriptive; note if the file should be renamed.
- **type**: note / framework / source / position / entity, with a one-line reason. The question for `position`: "is this a claim Alexandre would defend?" If an item mixes description and opinion, propose two notes: a descriptive one and a position linking to it.
- **status**: the starting value for that type.
- **tags**: 1–3, from the registered list; flag an unregistered one explicitly.
- **frontmatter**: full, per the template of the type. `reviewed` is left for Alexandre's approval date.
- **links**: existing notes this should link to, each with a reason. Search `_index.json` by title, alias and tags. "No strong link yet" is acceptable. Never link to a non-existent note.
- **destination folder**.
- For a `source`: draft 2–3 key takeaways in plain language; propose `status: processed` if Alexandre clearly read it. Keep the clipped original under a `<!-- Clipped article below -->` separator.
- For a `position`: draft the claim as a sentence someone could disagree with, list the evidence links, write the strongest counterargument you can find in the vault or in the source, propose a `confidence` that the evidence supports.

## Attachments
List files in `_attachments/` not embedded by any note (ignore README and `_processed/`). Propose the note each belongs in. Suggest a Mermaid version when the image is a diagram that could be text.

## What stays with Alexandre
The final call on what an idea connects to and why it matters. Surface candidates; he decides.

## After approval
Write frontmatter, rename if agreed, move to the destination folder, set `reviewed` to the approval date (the one moment an agent may set it), run `brain.py validate`, append a line to `99_Meta/changelog.md`, commit with prefix `triage:`. When the inbox is empty, give a one-line summary and list what was deferred.
