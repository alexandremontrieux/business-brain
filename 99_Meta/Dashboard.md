---
type: meta
tags: [meta/moc]
status:
created: 2026-06-12
reviewed: 2026-10-13
origin: manual
related: ["[[_taxonomy]]"]
---

# 🧠 Dashboard

The control room. Live Dataview queries; they update as notes change. Freshness threshold is 90 days (see `brain.config.json`).

## 🗳️ Proposals waiting for a decision

```dataview
TABLE proposal.action AS action, proposal.proposed_by AS by, proposal.proposed_on AS on, proposal.rationale AS why
FROM "60_Proposals"
WHERE proposal
SORT proposal.proposed_on ASC
```

## 📥 Inbox — needs triage

```dataview
TABLE origin, file.cday AS created
FROM "00_Inbox" AND -"00_Inbox/_processed"
SORT file.cday ASC
```

## 🎯 Positions by confidence

```dataview
TABLE confidence, status, length(evidence) AS evidence, reviewed
FROM "40_Positions"
WHERE status != "retired"
SORT choice(confidence = "high", 3, choice(confidence = "medium", 2, 1)) DESC, reviewed ASC
```

## ⚠️ Positions on thin ice (confidence outruns evidence)

```dataview
TABLE confidence, length(evidence) AS evidence
FROM "40_Positions"
WHERE status != "retired"
  AND ((confidence = "high" AND length(evidence) < 2) OR (confidence = "medium" AND length(evidence) < 1))
```

## 🕰️ Stale — not reviewed in 90 days

```dataview
TABLE type, status, reviewed
FROM "10_Notes" OR "20_Frameworks" OR "30_Sources" OR "40_Positions" OR "50_Entities"
WHERE status != "retired" AND reviewed AND reviewed < date(today) - dur(90 days)
SORT reviewed ASC
```

## 📚 Sources — unread or unprocessed

```dataview
TABLE author, status, captured
FROM "30_Sources"
WHERE type = "source" AND status != "processed" AND status != "retired"
SORT captured DESC
```

## 🧩 Frameworks by status

```dataview
TABLE status, maturity, domain
FROM "20_Frameworks"
WHERE type = "framework" AND status != "retired"
SORT status ASC, file.name ASC
```

## 🌱 Notes that need growing

```dataview
LIST
FROM "10_Notes"
WHERE status = "seedling"
SORT file.mtime DESC
```

## 🏢 Entities

```dataview
TABLE kind, status, reviewed
FROM "50_Entities"
WHERE type = "entity" AND status != "retired"
SORT kind ASC, file.name ASC
```

## 🔗 Orphans — no outgoing links

```dataview
LIST
FROM "10_Notes" OR "20_Frameworks" OR "30_Sources" OR "40_Positions" OR "50_Entities"
WHERE length(file.outlinks) = 0
SORT file.name ASC
```

## 🕸️ Recently touched

```dataview
TABLE type, status, file.mtime AS modified
FROM "10_Notes" OR "20_Frameworks" OR "30_Sources" OR "40_Positions" OR "50_Entities"
SORT file.mtime DESC
LIMIT 10
```
