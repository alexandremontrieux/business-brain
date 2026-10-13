---
type: position
tags: [domain/ai-security, domain/cybersecurity]
status: forming
created: 2026-10-13
reviewed:
origin: agent
related: ["[[Measuring LLMs' Impact on N-day Exploits]]"]
confidence: low
evidence: ["[[Measuring LLMs' Impact on N-day Exploits]]"]
concepts: []
proposal:
  action: create
  target:
  proposed_by: claude
  proposed_on: 2026-10-13
  rationale: The only source in the vault has takeaways but no position; this makes explicit whether Alexandre adopts its conclusion and shows the evidence is a single source.
  source_refs: ["30_Sources/Measuring LLMs' Impact on N-day Exploits.md (Key takeaways)"]
---

# Patch cadence must shrink because N-day is now N-hour

## Claim

Because frontier LLMs collapse N-day exploit development from expert-weeks to hours, monthly patch cadences and multi-week staged rollouts no longer hold; organisations should treat the patch gap as the primary exposure and plan for near-immediate deployment of security patches.

## Why I hold it

- Anthropic's red team built working Firefox and Windows kernel exploits from patches alone, within hours, for a few thousand dollars ([[Measuring LLMs' Impact on N-day Exploits]]).
- The scarce resource that used to slow attackers, reverse-engineering expertise, is no longer scarce.

## Counterarguments

- One vendor-published study on two targets; independent replication and real-world incident data are missing. Confidence should stay low until a second source exists.
- Faster patching has its own failure cost (broken systems); the realistic answer may be exploit-class mitigations and memory-safe languages rather than cadence alone, which the same source also argues.

## Where it applies

Client conversations on AI risk and on security operating models; a talking point, not yet a recommendation.

## History

- 2026-10-13 — proposed by agent from the source's takeaways; Alexandre has not stated this himself.

## Links

- [[Measuring LLMs' Impact on N-day Exploits]]
