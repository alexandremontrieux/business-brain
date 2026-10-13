---
type: note
tags: [domain/data-architecture]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[Canonical Data Model]]", "[[Dimensional Modelling]]", "[[Medallion Architecture]]", "[[Data Modelling Across the Medallion Layers]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# Data Vault

## Core idea

An integration modelling technique built from **hubs** (business keys), **links** (relationships) and **satellites** (descriptive attributes with history). It integrates on business keys and keeps what each source delivers, so meaning is applied later. That makes it auditable, fully historised and easy to extend with new sources.

## When to use it

A possible choice for **silver**, as an alternative to a canonical model:

- Fits: many source systems, strict audit requirements, frequent schema changes (a large hospital with dozens of systems).
- Costs: more modelling work and more complex queries. With few sources or a small team it is usually too heavy.

A canonical model forces one shared definition up front (faster to use, more rigid when definitions change). Data Vault defers that decision. Either way gold is typically dimensional. A vault is not consumption-ready; a dimensional layer and [[Semantic Model]] still follow.

Learning idea for the dummy hospital: build a small vault in silver (hub patient, hub stay, a link between them, satellites for attributes) and compare it to the canonical variant on complexity, flexibility and history.

## Links

- [[Canonical Data Model]]
- [[Dimensional Modelling]]
- [[Medallion Architecture]]
- [[Data Modelling Across the Medallion Layers]]
