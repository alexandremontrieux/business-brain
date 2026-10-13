---
type: note
tags: [domain/data-architecture]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[Canonical Data Model]]", "[[Semantic Model]]", "[[Data Modelling Across the Medallion Layers]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# Conceptual Data Model

## Core idea

A technology-independent description of the business reality: the key concepts and how they relate (a patient has stays, a stay takes place on a ward, a physician records a diagnosis). No keys, data types or tables. Its purpose is to agree with the business *what we are talking about* before design starts.

## Why it matters

It is the first link in the chain conceptual, canonical, dimensional, semantic:

- Conceptual: shared understanding of the concepts.
- [[Canonical Data Model]]: technical, source-neutral structure for integration (tables, keys, code lists). The implementable translation of the conceptual model.
- Dimensional model (see [[Dimensional Modelling]]): shape for querying.
- [[Semantic Model]]: meaning and measures for users.

A good conceptual model makes the canonical design easier, and a good canonical model makes the semantic model simpler and more reliable.

## Links

- [[Canonical Data Model]]
- [[Semantic Model]]
- [[Data Modelling Across the Medallion Layers]]
