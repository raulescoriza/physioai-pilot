# Step 1 — Case set scope (v1.0, confirmed)

> Status: **confirmed on 2026-10-16**. Any later change is recorded under "Changelog".

## Goal of the case set
Measure whether LLMs reason **safely and with clinical appropriateness** on musculoskeletal physiotherapy cases:
detect red flags, propose correct hypotheses and suggest an evidence-based plan.

## D1 — Clinical scope
Outpatient musculoskeletal physiotherapy, 5 regions.

| Region | Code | Pilot cases (10) | Final cases (100) |
|---|---|---|---|
| Lumbar | LUMB | 3 | 25 |
| Cervical | CERV | 2 | 20 |
| Shoulder | SHLD | 2 | 20 |
| Knee | KNEE | 2 | 20 |
| Ankle/foot | ANKL | 1 | 15 |

**Why:** the most frequent reasons for outpatient consultation, direct clinical experience of the author, and solid clinical guidelines to anchor the gold labels.
**Out of scope in v1:** neurology, respiratory, paediatrics, pelvic floor, complex post-surgical.

**Decision:** ✅ accepted, all 5 regions.

## D2 — Red flag proportion
~20% of cases with a true red flag requiring referral, plus ~10% "confounders" that look alarming but are not.

Types covered: cauda equina syndrome, fracture (traumatic or osteoporotic), malignancy, infection, cervical arterial dysfunction, deep vein thrombosis and inflammatory disease (e.g., axial spondyloarthritis).

**Why:** easy cases alone do not measure safety. Confounders measure the opposite failure: over-referral, which is also a clinical error.

**Decision:** ✅ accepted.

## D3 — Language
The whole repository — case clinical text, system prompt, documentation and code — is written in **English** (field `language: en`). Spanish or German versions can come later as a separate cross-lingual experiment.

**Why:** a single, fully English repository is directly usable by any contributor or evaluator, and is the cleanest form for public publication.

**Decision:** ✅ accepted (changed on 2026-10-25: full English for the public repository, replacing the earlier "Spanish first" decision).

## D4 — Case origin (ethics and privacy)
**Fixed rule:** cases are **synthetic**, inspired by real clinical patterns but **never** based on a specific patient or containing identifiable data.

**Why:** avoids GDPR and ethical issues, and allows the case set to be published.

## D5 — Source of the gold answer
The author's clinical judgement, backed by reference guidelines where available, cited in each case (`references` field). Examples: the IFOMPT International Framework for Red Flags (2020) and the NICE low back pain guideline.

**Why:** a cited source makes every label defensible to any reviewer, not just the author's opinion.

**Decision:** ✅ accepted.

## D6 — Format and storage
- **One YAML file per case** in `cases/`, following `cases/_template.yaml`.
- Strict separation: the `case` block is what the model sees; the `gold` block (expected answer) is never sent to it.
- The `screening` block is **identical in every case** (same questions, same order). Only the answers change, so the length of the history never leaks the answer.
- Everything versioned in Git so results are reproducible.

**Why YAML:** easy to write and read (long clinical text) and loads directly in Python. Automatic schema validation comes later.

## D7 — License (decided at publication time)
Candidate: CC BY 4.0 for the cases and MIT for the code.

---
## Changelog
- 2026-10-25 — v1.2 full English: all case clinical text, system prompt and remaining docs translated from Spanish; D3 language decision updated; confidential data (`.env`, local session state) removed from version control.
- 2026-10-16 — v1.1 structure translated to English; standardized screening block; `suspicion_level` and `safety_netting` added to gold.
- 2026-10-16 — v1.0 decisions D1–D5 confirmed.
- 2026-10-16 — v0.1 initial draft.
