---
type: meta
tags: [meta/procedure]
status:
created: 2026-10-13
reviewed: 2026-10-13
origin: manual
related: ["[[_taxonomy]]"]
---

# Procedure: consult

**Goal:** answer a question from Alexandre's own knowledge first, and make visible where the answer is his opinion versus description versus a gap.

## Steps
1. Load `99_Meta/_index.json` (run `brain.py index` if older than the newest note). Search titles, aliases, tags, then full text of candidates.
2. Read the matching notes fully. Follow `related` one hop when the question is broad.
3. Answer with three layers, labelled:
   - **What the brain says** — descriptive content from notes, frameworks, sources, with `[[links]]` cited.
   - **Where Alexandre is opinionated** — positions that apply, with their confidence and evidence count. Quote the claim. Mention counterarguments recorded in the position.
   - **What the brain does not cover** — gaps, and whether general knowledge is being used to fill them. Say so explicitly; never pass general knowledge off as something in the brain.
4. If the question exposes a gap or a contradiction between notes, offer to capture it (a question is often the seed of a position).

## Rules
- Consult writes nothing. Offer capture; do not do it silently.
- Freshness matters: flag any cited note whose `reviewed` is older than the stale threshold.
