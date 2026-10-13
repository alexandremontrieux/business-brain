---
type: meta
tags: [meta/taxonomy]
status:
created: 2026-06-12
reviewed: 2026-10-13
origin: manual
related: ["[[Dashboard]]"]
---

# Taxonomy

The controlled vocabulary for this vault, explained for humans. The machine-readable copy is
`schema.json`; `_scripts/brain.py validate` enforces it. **If the two differ, `schema.json` wins**
and this file needs fixing. Adding a value is a proposal (see `AGENTS.md` §6).

## type (one per note, required)

| value | meaning | folder |
|---|---|---|
| `note` | atomic knowledge note: what a thing is, why it matters | `10_Notes/` |
| `framework` | reusable method, model, structure | `20_Frameworks/` |
| `source` | clipped article / external reference, with takeaways | `30_Sources/` |
| `position` | **an opinion Alexandre holds**: claim, evidence, counterarguments, confidence | `40_Positions/` |
| `entity` | client, organisation, offering, tool, standard, professional contact | `50_Entities/` |
| `meta` | vault infrastructure (this file, dashboard, procedures) | `99_Meta/` |

The split that matters: notes and frameworks are **descriptive**, positions are **normative**.
"A canonical model usually lives in silver" is a note. "Start a canonical model small and
sharp rather than complete and vague" is a position. When a note starts arguing, extract the
argument into a position and link back.

## status

| type | values |
|---|---|
| note | `seedling` → `growing` → `evergreen` (→ `retired`) |
| framework | `draft` → `tested` → `published` (→ `retired`) |
| source | `unread` → `read` → `processed` (→ `retired`) |
| position | `forming` → `held` → `revised` (→ `retired`) |
| entity | `active` ↔ `dormant` (→ `retired`) |

`retired` replaces deletion. A retired note keeps its links and history.

## Common fields (all types)

| field | meaning |
|---|---|
| `created` | date the note was created |
| `reviewed` | date **Alexandre** last confirmed the note is still right. Freshness is computed from this. Agents never set it; approving a proposal sets it. |
| `origin` | where it came from: `manual`, `clipper`, `meetingbrain`, `conversation`, `agent` |
| `related` | wikilinks to related notes (the graph edge list; keep it honest) |
| `aliases` | optional, other names Obsidian should resolve to this note |
| `source` | optional on notes: free text on where the content came from (a project, a conversation) |

## Type-specific fields

| type | fields |
|---|---|
| framework | `domain` (free, lowercase), `maturity`: `experimental` → `working` → `proven` |
| source | `author`, `url`, `captured` (datetime of clipping) |
| position | `confidence`: `low` / `medium` / `high`; `evidence`: links to sources, notes, meetings that support it; `concepts`: links to the notes/frameworks the position is about |
| entity | `kind`: `client`, `organisation`, `person`, `tool`, `offering`, `standard` |

### Confidence and evidence

Confidence is a self-assessment, evidence is what backs it. The dashboard flags positions where
the two disagree: `high` needs at least two evidence links, `medium` at least one. A `high`
position resting on one source is the kind of opinion this brain exists to expose.

## Proposals

A note in `60_Proposals/` is a draft awaiting a decision. Its frontmatter carries the note's
normal fields plus a `proposal` block:

```yaml
proposal:
  action: create        # create | update | merge | retire | taxonomy | review
  target:               # path of the existing note, for update/merge/retire
  proposed_by: claude   # agent or person
  proposed_on: 2026-10-13
  rationale: one sentence on why this belongs in the brain
  source_refs: ["Meetingbrain/Projecten/x.md", "conversation 2026-10-13"]
```

Approving = move it to the target folder and remove the block (or ask an agent to apply it).

## tags

Tags are the cross-cutting axis; links are the primary one. Shallow hierarchy, lowercase, hyphenated.

- `domain/...` — subject area
- `meta/...` — vault management
- free tags — anything else

### Registered tags

| tag | meaning |
|---|---|
| `domain/ai-strategy` | how an organisation adopts, governs, and creates value from AI |
| `domain/ai-security` | AI/LLM safety, misuse, and security research |
| `domain/cybersecurity` | vulnerabilities, exploits, patching, defense |
| `domain/data-architecture` | data platform architecture and modelling (medallion, canonical, dimensional, Data Vault) |
| `domain/healthcare-data` | healthcare data standards and ecosystems (FHIR, OMOP, hospital data) |
| `domain/consulting` | consulting craft: engagements, presales, delivery, bench |
| `domain/knowledge-management` | knowledge systems, communities, catalogs, this brain |
| `llm-capabilities` | empirical measurements of what LLMs can do |
| `operating-model` | how people, process, and technology are organised to deliver |
| `meta/taxonomy`, `meta/moc`, `meta/procedure` | vault management |

An unregistered tag is a validation warning, not an error: register it here and in `schema.json`
when it is used by a second note.

## Images & diagrams

Visuals are assets, not notes. Author diagrams as Mermaid inside the note wherever possible.
Raster images go in `_attachments/` with descriptive names (`ai-operating-model.png`, never
`Pasted image 2026...`) and are embedded with `![[name.png]]`.

## Organizing principle

Links and tags are primary. Folders are coarse buckets keyed to `type` only; never nest deeper
for topic. A note's topic lives in its tags and its `[[links]]`, not its folder path.
