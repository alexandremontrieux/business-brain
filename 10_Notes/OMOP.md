---
type: note
tags: [domain/data-architecture, domain/healthcare-data]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[FHIR]]", "[[Canonical Data Model]]", "[[Medallion Architecture]]", "[[Data Modelling Across the Medallion Layers]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# OMOP

## Core idea

Observational Medical Outcomes Partnership common data model, maintained by the OHDSI community, built for research and analysis. A relational schema with tables such as `person`, `visit_occurrence`, `condition_occurrence`, `drug_exposure`, `measurement` and `procedure_occurrence`. The key ingredient is the **standardised vocabulary**: local codes (ICD-10, SNOMED, LOINC, ATC, own codes) are mapped to one set of standard concepts, so the same analysis query runs on data from several hospitals and gives comparable results.

## Why it matters

- Suited to cohort selection, epidemiology and multi-centre research (OHDSI tools such as ATLAS build queries on it).
- Both a canonical model (everyone maps to the same schema and concepts) and a normalised one (separate tables, keys, no repetition).
- Typical pipeline: sources, FHIR (silver), OMOP (gold for research). Microsoft Healthcare Data Solutions and Databricks provide example transformations.
- Not consumption-ready for managers: values are `concept_id`s that need vocabulary lookups. Researchers can use it directly; business reporting needs a [[Dimensional Modelling]] layer.
- The vocabulary mapping is the hardest and most instructive part.

## Links

- [[FHIR]]
- [[Canonical Data Model]]
- [[Medallion Architecture]]
- [[Data Modelling Across the Medallion Layers]]
