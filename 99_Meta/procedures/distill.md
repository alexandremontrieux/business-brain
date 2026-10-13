---
type: meta
tags: [meta/procedure]
status:
created: 2026-10-13
reviewed: 2026-10-13
origin: manual
related: ["[[_taxonomy]]"]
---

# Procedure: distill (AI conversations → brain)

**Goal:** turn a working session with an AI agent, or an exported conversation, into inbox items or proposals, so what was learnt or decided is not lost in a chat log.

## Triggers
- Alexandre says "distill this" / "put this in the brain" at the end of a session.
- A conversation export (Markdown/JSON) lands in `00_Inbox/`.
- A scheduled scan of local agent session logs, if configured in `brain.config.json` → `sources.conversations`.

## Steps
1. Read the whole conversation. Ignore chit-chat, tool noise and anything that is project status rather than knowledge.
2. Extract, in this priority: (a) positions Alexandre stated or arrived at, with the reasoning as evidence; (b) concepts that were explained and would be worth re-reading; (c) frameworks or checklists that emerged; (d) corrections to existing notes.
3. For each: if the session is interactive, present the candidate in one paragraph and ask "capture, propose, or skip?". If unattended, write a proposal (`origin: conversation`, `source_refs`: conversation title + date).
4. The agent's own general-knowledge explanations are **not** Alexandre's knowledge. They become a `note` only if he engaged with them (asked, corrected, applied). A position is only his if he stated it, not the agent.
5. Run `brain.py validate`, changelog, commit `distill:`.

## Rules
- At most 5 items per conversation. Depth over volume.
- Quote Alexandre's words for a position claim where possible; do not improve his opinion for him.
