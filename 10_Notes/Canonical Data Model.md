---
type: note
tags: [domain/data-architecture]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[Data Modelling Across the Medallion Layers]]", "[[Conceptual Data Model]]", "[[Semantic Model]]", "[[Dimensional Modelling]]", "[[Data Vault]]", "[[Medallion Architecture]]", "[[FHIR]]", "[[OMOP]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# Canonical Data Model

## Core idea

One shared, source-neutral data model that every source system is translated into. Instead of connecting every system to every other system, each source gets one mapping to the canonical model. It is a *role* a model plays, not a specific standard. It is usually normalised: separate tables per concept (person, visit, condition) linked by keys, each fact stored once.

In a medallion setup it typically lives in **silver**: silver describes the operations, the canonical model describes the target they work towards.

## What happens in silver (and what does not)

Silver changes the *form and quality* of data, gold changes the *level of detail*.

- Clean and type (dates, numbers, placeholder values), deduplicate, flag invalid records.
- Harmonise names and structure (`sex` and `gender_cd` become `gender`; flatten nested FHIR JSON; split wide tables into entities).
- Standardise codes and units (local diagnosis codes to ICD-10/SNOMED, mg/dL to mmol/L).
- Harmonise keys and link entities across sources (one `person_id`, via a master patient index or matching). Combining tables here is integration of the same entity, not aggregation.
- Keep history and lineage (validity dates, load time, source system) and apply quality rules.
- Not in silver: sums, averages, counts per department or month, facts and dimensions with derived measures. That is gold.
- Grey area: row-level derived fields such as length of stay (end minus start). Many teams keep these in gold so silver stays close to the source.

## Where the model comes from

Not necessarily from an industry standard. Three routes:

1. Adopt a standard (FHIR, OMOP, openEHR in healthcare; ACORD, FIBO, CIM elsewhere). Less design work, interoperability, but may not fit the use case.
2. Design an own enterprise model. Fits the organisation's language, but costs alignment effort and external interoperability is your own problem.
3. Hybrid (most common): standard as base, extended with local extensions.

## Characteristics checklist

There is no formal norm or certification. These traits make a model deserve the name:

- Source-neutral (not shaped like one system).
- One shared definition per concept (what is a visit, when does it start and end). This is the most important one.
- One structure for all sources.
- Standardised code lists and units.
- Clear keys and documented relationships.
- Documented mappings and lineage (per field: source and transformation).
- Stable and extensible (a new source means a new mapping, not a rebuild).
- Ownership and governance, otherwise teams drift into private variants.

Typical failure modes: starting too big (all sources, all concepts at once) and missing governance. A small model with sharp definitions beats a complete model with vague ones.

## Consumption readiness

Usually not consumption-ready for business users: many tables and joins, technical names (in OMOP many values are `concept_id`s to look up), no derived measures (two people will define length of stay differently), and optimised for integrity rather than query speed. Consumption-ready needs a [[Dimensional Modelling]] layer in gold plus a [[Semantic Model]]. Technical users (data scientists, researchers) can use a canonical model directly, e.g. OMOP cohort queries.

## Links

- [[Conceptual Data Model]] — the business-level input to the canonical design.
- [[Semantic Model]] — consumption side.
- [[Dimensional Modelling]] — gold, built from the canonical model.
- [[Data Vault]] — alternative integration approach in silver.
- [[Data Modelling Across the Medallion Layers]]
- [[Medallion Architecture]]
- [[FHIR]]
- [[OMOP]]
