---
type: note
tags: [domain/data-architecture]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[Data Modelling Across the Medallion Layers]]", "[[Canonical Data Model]]", "[[Dimensional Modelling]]", "[[Data Vault]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# Medallion Architecture

## Core idea

A layered pattern for organising a lakehouse by how refined the data is: **bronze** (raw, as ingested), **silver** (cleaned, integrated, conformed) and **gold** (consumption-ready). The layers describe the *level of refinement*, not the *shape* of the data. What model you use inside each layer (canonical, Data Vault, star schema) is a separate choice, see [[Data Modelling Across the Medallion Layers]].

## Why it matters

- Medallion is the de-facto pattern in healthcare data platforms: Microsoft Healthcare Data Solutions in Fabric, Databricks and CareEvolution all structure their offering this way. Healthcare data is heterogeneous and messy (HL7, FHIR, DICOM, EPD exports), so keeping raw data for traceability and standardising step by step fits well.
- It is rarely used alone. In practice it is combined with:
  - a healthcare standard as the model in silver/gold (see [[FHIR]] and [[OMOP]]),
  - domain ownership through data mesh / data products (each data product can run its own medallion flow internally),
  - data fabric (metadata and virtualisation layer) where data cannot be centralised,
  - federated analytics for multi-centre research, where data stays in each hospital.
- Common critique: layers are technical, not organised around business domains. Combining medallion with data products addresses that.

## Layer summary

| Layer | Purpose | What happens |
|---|---|---|
| Bronze | Preserve the source | Append-only raw copy plus load metadata. No model imposed. |
| Silver | Make it trustworthy and integrated | Clean, type, deduplicate, harmonise, map codes, link keys. Detail level is kept. |
| Gold | Make it usable | Business-ready models, aggregates, measures. |

## Links

- [[Data Modelling Across the Medallion Layers]]
- [[Canonical Data Model]]
- [[Dimensional Modelling]]
- [[Data Vault]]
- [[FHIR]]
- [[OMOP]]
