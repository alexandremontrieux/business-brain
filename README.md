# Business Brain

Alexandre's personal knowledge graph: plain Markdown + YAML frontmatter + `[[wikilinks]]`,
viewed in Obsidian, versioned in git, operated by AI agents under the contract in `AGENTS.md`.

What it is for: consolidate knowledge and expertise so that it is easy to **consult**, and so
that it is visible **where the knowledge is opinionated** (positions), **how well-founded** that
is (evidence, confidence) and **how fresh** it is (`reviewed`).

## Layout

```
AGENTS.md            the operating contract every agent follows (CLAUDE.md just points here)
brain.config.json    vault configuration; brain.config.local.json for machine-specific paths
00_Inbox/            raw capture, untriaged (manual notes, web clippings, pasted snippets)
10_Notes/            atomic knowledge notes            type: note
20_Frameworks/       methods, models, structures       type: framework
30_Sources/          clippings, external references    type: source
40_Positions/        opinions with evidence/confidence type: position
50_Entities/         clients, tools, offerings, people type: entity
60_Proposals/        agent-drafted changes awaiting a decision
90_Templates/        one Templater template per type
99_Meta/             _taxonomy.md, schema.json, Dashboard.md, procedures/, _index.*, changelog.md
_attachments/        images and files
_scripts/brain.py    validate · index · stale · orphans · thin-positions · proposals · find
.github/workflows    CI runs validate on every push and PR
```

Topic lives in tags and links, never in folders.

## Set up on a machine

1. Clone the repo somewhere **outside** OneDrive / Google Drive (sync tools and git fight):
   `git clone git@github.com:<you>/business-brain.git C:\Users\<you>\business-brain`
2. Obsidian → *Open folder as vault* → that folder. Settings → Community plugins → turn off
   Restricted mode. Dataview, Templater and Git ship in `.obsidian/plugins/` and are enabled.
3. Git plugin: it auto-commits and pushes every 10 minutes and pulls on start. Git must be
   installed on the machine and the remote must be reachable with your credentials once
   (`git push` from a terminal the first time).
4. Optional: install the **Obsidian Web Clipper** browser extension and point it at this vault,
   folder `00_Inbox`, template with `origin: clipper`.
5. Copy `brain.config.local.example.json` to `brain.config.local.json` and set the Meetingbrain path.
6. `python _scripts/brain.py validate` should report 0 errors.

## Daily use

- Open `99_Meta/Dashboard.md`: proposals waiting, inbox, positions by confidence, thin positions, stale notes.
- Capture anything into `00_Inbox/`. Don't sort while capturing.
- Ask an agent to **triage** the inbox; approve or reject each proposal.
- Decide on `60_Proposals/` when you feel like it: move the file to its folder (strip the
  `proposal` block) or delete it. Approving a note is the moment to set `reviewed`.
- Ask questions. The **consult** procedure makes an agent answer from the brain and label
  what is description, what is your opinion, and what is a gap.

## Agent operations

| mode | what | when |
|---|---|---|
| capture | raw input → inbox | ad hoc |
| triage | inbox → typed, linked notes, propose-first | ad hoc |
| consult | answer from the brain, label opinions and gaps | ad hoc |
| daily-scan | changed Meetingbrain notes → proposals | scheduled daily |
| distill | AI conversation → inbox/proposals | end of session, or export in inbox |
| weekly-review | validation, stale, thin, orphans, duplicates → review proposal | scheduled weekly |

Everything an agent needs is in `AGENTS.md` and `99_Meta/procedures/`. Switching agents means
pointing the new one at `AGENTS.md`; nothing else changes.

## Conventions in one breath

Every typed note: `type`, `tags`, `status`, `created`, `reviewed`, `origin`, `related`.
Notes and frameworks describe; positions argue. `reviewed` is set by a human, never by an agent.
Agents write only to `00_Inbox/`, `60_Proposals/`, `_index.*` and `changelog.md` without approval.
Nothing is deleted; things are retired. `schema.json` is the law, `_taxonomy.md` explains it.
