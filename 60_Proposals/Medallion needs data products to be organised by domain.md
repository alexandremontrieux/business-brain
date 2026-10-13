---
type: position
tags: [domain/data-architecture]
status: forming
created: 2026-10-13
reviewed:
origin: agent
related: ["[[Medallion Architecture]]"]
confidence: medium
evidence: ["[[Medallion Architecture]]"]
concepts: ["[[Medallion Architecture]]"]
proposal:
  action: create
  target:
  proposed_by: claude
  proposed_on: 2026-10-13
  rationale: The Medallion note records a critique and a response (layers are technical, combine with data products); that response is an opinion worth tracking against Alexandre's data product methodology work.
  source_refs: ["10_Notes/Medallion Architecture.md (Why it matters)", "Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13"]
---

# Medallion needs data products to be organised by domain

## Claim

Medallion architecture on its own organises data by technical refinement, not by business domain; it should be combined with domain-owned data products, each running its own medallion flow internally, rather than used as the top-level structure of a platform.

## Why I hold it

- The common critique of medallion is that bronze/silver/gold are technical layers with no business ownership (see [[Medallion Architecture]]).
- In healthcare platforms medallion is in practice always combined with something else: a standard in silver/gold, data mesh / data products, fabric or federated analytics.
- Fits AE's data product methodology, where ownership and consumption contracts sit at domain level.

## Counterarguments

- For a small organisation with one data team, domain decomposition adds coordination cost without the ownership benefit; a single medallion is simpler and good enough.
- Vendors (Fabric Healthcare Data Solutions, Databricks) ship medallion as the top-level structure, so going against it costs alignment with tooling and documentation.

## Where it applies

Platform design conversations for organisations with multiple domains or multiple source-owning teams.

## History

- 2026-10-13 — proposed by agent from existing note content; not yet confirmed by Alexandre.

## Links

- [[Medallion Architecture]]
- [[Data Modelling Across the Medallion Layers]]
