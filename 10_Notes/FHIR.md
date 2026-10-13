---
type: note
tags: [domain/data-architecture, domain/healthcare-data]
status: seedling
created: 2026-10-13
reviewed: 2026-10-13
origin: conversation
related: ["[[OMOP]]", "[[Canonical Data Model]]", "[[Medallion Architecture]]", "[[Data Modelling Across the Medallion Layers]]"]
source: Claude conversation, Data & Healthcare Ecosystem project, 2026-10-13
---

# FHIR

## Core idea

Fast Healthcare Interoperability Resources: an HL7 standard for exchanging healthcare data between systems (an EPD sharing with a lab system, an app or another hospital). Data is organised in **resources** (Patient, Encounter, Observation, Condition, MedicationRequest, Procedure) linked by references, usually exchanged as JSON over a REST API. Built for operational use: fetch a patient record, send a lab result, create an appointment.

## Why it matters

- In a lakehouse FHIR bundles typically land in bronze or silver. The nested JSON is not ideal for analysis, so it gets flattened.
- In the medallion chain it is a candidate canonical model for silver: sources are mapped to FHIR resources, then gold (reporting) or [[OMOP]] (research) is derived.
- Test data: Synthea generates synthetic patients as FHIR (and can export OMOP-compatible output).

FHIR is for moving data between systems; [[OMOP]] is for analysing it reliably.

## Links

- [[OMOP]]
- [[Canonical Data Model]]
- [[Medallion Architecture]]
- [[Data Modelling Across the Medallion Layers]]
