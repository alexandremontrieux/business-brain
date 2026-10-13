---
type: position
tags: [domain/data-architecture]
status: forming
created: 2026-10-13
reviewed:
origin: agent
related: ["[[Canonical Data Model]]", "[[Data Modelling Across the Medallion Layers]]"]
confidence: medium
evidence: ["[[Canonical Data Model]]"]
concepts: ["[[Canonical Data Model]]", "[[Conceptual Data Model]]"]
proposal:
  action: create
  target:
  proposed_by: claude
  proposed_on: 2026-10-13
  rationale: The Canonical Data Model note already argues this; it is an opinion, not a description, and belongs in a position so its confidence and evidence are visible.
  source_refs: ["10_Notes/Canonical Data Model.md (section Characteristics checklist)", "Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13"]
---

# Start a canonical model small and sharp

## Claim

A canonical data model should start with a few concepts and sharp shared definitions, and grow by adding mappings, rather than attempting all sources and all concepts at once. A small model with sharp definitions beats a complete model with vague ones.

## Why I hold it

- The typical failure modes of canonical models are starting too big and missing governance (see [[Canonical Data Model]]).
- One shared definition per concept (what is a visit, when does it start and end) is the single most important trait; that is a definition problem, not a coverage problem.
- A model that is stable and extensible means a new source is a new mapping, not a rebuild, so breadth can come later without penalty.

## Counterarguments

- With an adopted standard (FHIR, OMOP) the breadth comes for free and the risk shifts to fit, not size; "small" then means a small *profile* of the standard rather than a small model.
- In a many-source, high-audit environment a Data Vault defers definitions instead of sharpening them up front, which may be the better trade (see [[Data Vault]]).

## Where it applies

Organisations designing their own or hybrid canonical model in silver; less relevant when a standard is mandated.

## History

- 2026-10-13 — proposed by agent from existing note content; not yet confirmed by Alexandre.

## Links

- [[Canonical Data Model]]
- [[Data Modelling Across the Medallion Layers]]
