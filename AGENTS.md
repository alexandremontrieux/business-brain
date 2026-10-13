# AGENTS.md — operating contract for the Business Brain

This vault is Alexandre's personal knowledge graph: plain Markdown files with YAML
frontmatter and `[[wikilinks]]`, viewed in Obsidian, versioned in git. **This file is
the contract every agent follows**, whichever agent it is (Claude, Codex, Cursor,
a cron script). Nothing agent-specific lives in the vault; if you need agent-specific
glue, keep it outside the repo and point it here.

Read in this order before doing anything: this file → `99_Meta/_taxonomy.md` →
`99_Meta/schema.json` → the procedure in `99_Meta/procedures/` that matches the task.

## 1. Purpose

Consolidate Alexandre's knowledge and expertise so that it is easy to **consult**, and so
that it is visible **where his knowledge is opinionated** (positions), **how well-founded**
those opinions are (evidence, confidence), and **how fresh** everything is (`reviewed`).

## 2. Invariants (never break these)

1. **Propose first.** Agents do not create, change, move, rename or delete anything in
   `10_`–`50_` or `99_Meta/_taxonomy.md` / `schema.json` without explicit approval.
   Agents write freely only to `00_Inbox/`, `60_Proposals/`, `99_Meta/_index.*`,
   `99_Meta/scan-state.json` and `99_Meta/changelog.md`. Everything else, including fixing a
   broken link in an existing note, is a proposal.
2. **Never delete.** Retire (`status: retired` / `archived`) instead. Humans delete.
3. **The taxonomy wins.** Values for `type`, `status`, `confidence`, `kind`, `origin` and
   registered tags come from `99_Meta/schema.json` (machine) and `_taxonomy.md` (human).
   A new value is itself a proposal.
4. **Linking judgement stays with Alexandre.** Suggest links with a reason; do not fabricate
   links to notes that do not exist. "No strong link yet" is a valid answer.
5. **Sanitise.** No client-confidential data, no personal data about third parties beyond
   their professional role, no credentials. Meetingbrain notes are already cleaned; keep it so.
6. **Plain Markdown only.** No agent-specific syntax, no proprietary embeds. Diagrams as
   Mermaid; raster images in `_attachments/` with descriptive names.
7. **One subject per note.** Prefer updating an existing note over creating a near-duplicate.
   Check with `python _scripts/brain.py find "<term>"` first.

## 3. Folder and type map

| Folder | `type` | What it holds |
|---|---|---|
| `00_Inbox/` | any / none | Raw capture: manual notes, web clippings, pasted snippets. Untriaged. |
| `10_Notes/` | `note` | Atomic knowledge notes: what a thing is and why it matters. |
| `20_Frameworks/` | `framework` | Reusable methods, models, structures. |
| `30_Sources/` | `source` | Clipped articles and external references, with takeaways. |
| `40_Positions/` | `position` | **Alexandre's opinions**: a claim, the evidence, counterarguments, confidence. |
| `50_Entities/` | `entity` | Clients, organisations, offerings, tools, standards, (professional) people. |
| `60_Proposals/` | any, with `proposal:` block | Agent-drafted notes/changes awaiting Alexandre's decision. |
| `90_Templates/` | — | Templater templates, one per type. |
| `99_Meta/` | `meta` | Taxonomy, schema, dashboard, procedures, index, changelog, config. |
| `_attachments/` | — | Images and files, no frontmatter. |
| `_scripts/` | — | Deterministic tooling (`brain.py`). Agent-agnostic. |

Topic lives in **tags and links**, not folders. Never nest folders by topic.

## 4. Frontmatter (summary; `schema.json` is normative)

Every typed note has: `type`, `tags`, `status`, `created`, `reviewed`, `origin`, `related`.

- `reviewed` — date a human last confirmed the note is still right. Freshness is computed
  from this, not from file mtime. An agent sets it only while applying a change Alexandre has
  just approved, to the approval date; never during a scan, review or on its own judgement.
- `origin` — `manual` | `clipper` | `meetingbrain` | `conversation` | `agent`.
- `position` adds `confidence` (`low`|`medium`|`high`), `evidence` (links), `concepts` (links).
  A `high` confidence position with fewer than two evidence links is flagged by the dashboard.
- `entity` adds `kind` (`client`|`organisation`|`person`|`tool`|`offering`|`standard`).
- `source` adds `author`, `url`, `captured`.
- `framework` adds `domain`, `maturity`.
- Optional on any type: `aliases`. Optional on `note`: `source` (free text on where it came from).
- Proposals add a `proposal` block: `action` (`create`|`update`|`merge`|`retire`|`taxonomy`|`review`),
  `target` (path, required for update/merge/retire), `proposed_by`, `proposed_on`, `rationale`,
  `source_refs`. `origin` on a proposal says where the content came from (`meetingbrain`,
  `conversation`, `clipper`, `manual`), not that an agent wrote it; `agent` is for agent-generated
  meta content such as a weekly review.

## 5. Operating modes

Each mode has a procedure file in `99_Meta/procedures/`. Follow it literally.

| Mode | Trigger | Reads | Writes | Procedure |
|---|---|---|---|---|
| **capture** | Alexandre gives input, pastes text, or a clipping lands | the input | `00_Inbox/` | `capture.md` |
| **triage** | "triage the inbox" / inbox non-empty | `00_Inbox/`, vault | `60_Proposals/` then, on approval, `10_`–`50_` | `triage.md` |
| **consult** | any question about Alexandre's knowledge or opinions | whole vault | nothing (answer in chat, cite notes) | `consult.md` |
| **daily-scan** | scheduled, daily | Meetingbrain notes changed since last run | `60_Proposals/`, `99_Meta/changelog.md` | `daily-scan.md` |
| **distill** | end of an AI working session, or an exported conversation in the inbox | the conversation | `00_Inbox/` or `60_Proposals/` | `distill.md` |
| **weekly-review** | scheduled, weekly | whole vault, `brain.py` reports | `60_Proposals/`, `99_Meta/_index.*`, `changelog.md` | `weekly-review.md` |

## 6. Proposals

A proposal is a complete, ready-to-move note in `60_Proposals/` whose frontmatter carries the
`proposal` block. Approval is a human act: Alexandre either moves the file to its target folder
(and strips the `proposal` block, or asks an agent to), edits it first, or deletes it.
Agents may apply an approved proposal when told to. Proposals older than 30 days are listed
on the dashboard as "stale proposals"; the weekly review asks whether to drop them.

When working through git, a batch of proposals goes on a branch `proposals/YYYY-MM-DD-<mode>`
and, if a remote with pull requests is available, as a PR. Direct commits to `main` are for
approved changes and Alexandre's own edits only. Agent commit message prefix: `capture:`,
`triage:`, `scan:`, `distill:`, `review:`, `apply:`, `meta:`. The Obsidian Git plugin's
automatic `vault backup:` commits are Alexandre's own edits and need no prefix.

## 7. Tooling

`python _scripts/brain.py <command>` (stdlib only, runs anywhere):

- `validate` — frontmatter present and schema-valid, folder matches type, links resolve, tags registered. Exit code 1 on errors. Run before every commit; CI runs it on every push/PR.
- `index` — rebuilds `99_Meta/_index.md` and `_index.json` (all typed notes with key fields). Agents use the JSON instead of walking the tree.
- `stale [--days N]` — notes whose `reviewed` is older than N days (default from `brain.config.json`).
- `orphans` — typed notes with no inbound and no outbound links.
- `thin-positions` — positions whose evidence count is below the confidence threshold.
- `proposals` — lists pending proposals with age.
- `find "<term>"` — title/alias/tag search, to check for duplicates before creating.

Configuration (paths to Meetingbrain, stale threshold, etc.) lives in `brain.config.json`.
Machine-specific paths go in `brain.config.local.json` (git-ignored).

## 8. Style

Notes are written in English unless the subject is Dutch-only. Concise, declarative, sources
named. Headings follow the template of the type. A note states what Alexandre thinks only in a
`position`; notes and frameworks stay descriptive and link to the positions that depend on them.
