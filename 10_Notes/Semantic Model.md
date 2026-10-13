---
type: note
tags: [domain/data-architecture]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[Canonical Data Model]]", "[[Conceptual Data Model]]", "[[Dimensional Modelling]]", "[[Data Modelling Across the Medallion Layers]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# Semantic Model

## Core idea

The consumption-side model that fixes meaning for users and tools: what "length of stay" is, how admissions are counted, which relations exist between tables, which hierarchies (ward, campus, hospital) and calculated measures. In Power BI / Fabric this is the semantic model (dataset) on top of the gold layer, so everyone gets the same answer to the same question.

## Watch out: two meanings

- Analytics meaning (above): measures, relationships and hierarchies for reporting.
- Formal meaning: ontologies and knowledge graphs (SNOMED, RDF) that capture meaning in a machine-readable way. Ask which one is meant.

## Relation to the other models

Semantic sits at the end of the chain: [[Conceptual Data Model]] (shared understanding), [[Canonical Data Model]] (integration), [[Dimensional Modelling]] (star schemas in gold), semantic model (business definitions on top). Business users should consume the semantic model, not the canonical one.

## Links

- [[Canonical Data Model]]
- [[Conceptual Data Model]]
- [[Dimensional Modelling]]
- [[Data Modelling Across the Medallion Layers]]
