---
type: note
tags: [domain/data-architecture]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[Canonical Data Model]]", "[[Semantic Model]]", "[[Data Vault]]", "[[Medallion Architecture]]", "[[Data Modelling Across the Medallion Layers]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# Dimensional Modelling

## Core idea

Kimball-style modelling for analysis and reporting. Deliberately denormalised: **fact tables** hold measurements or events (a stay, a lab test) with numbers such as length of stay or cost, **dimension tables** hold the context to filter and group by (patient, ward, physician, diagnosis, date). Together they form a star schema. It asks "how can a user query this quickly and understandably?", where a canonical model asks "what is the right source-neutral representation?".

## Why it matters

Typically sits in **gold**. Example: `fact_stay` with keys to `dim_patient`, `dim_ward`, `dim_diagnosis` and `dim_date`. "Average length of stay per ward per month" becomes one join per dimension and Power BI can work on it directly.

## Versus the canonical model

| | Canonical | Dimensional |
|---|---|---|
| Goal | Integrate sources | Analyse and report |
| Shape | Normalised, many tables | Denormalised, star schema |
| Designed around | Business concepts and meaning | Questions and measurements |
| Joins | Many | Few |
| Layer | Silver | Gold |

They complement each other: the dimensional model is normally built from the canonical model, and one silver can feed several gold models (a star schema for reporting, an OMOP model for research).

## Links

- [[Canonical Data Model]]
- [[Semantic Model]]
- [[Data Vault]] — alternative to a canonical model in silver.
- [[Medallion Architecture]]
- [[Data Modelling Across the Medallion Layers]]
