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

## D2 — Red flag proportion
~20% of cases with a true red flag requiring referral, plus ~10% "confounders" that look alarming but are not.

Types covered: cauda equina syndrome, fracture (traumatic or osteoporotic), malignancy, infection, cervical arterial dysfunction, deep vein thrombosis and inflammatory disease (e.g., axial spondyloarthritis).

**Why:** easy cases alone do not measure safety. Confounders measure the opposite failure: over-referral, which is also a clinical error.

## D3 — Language
The whole repository — case clinical text, system prompt, documentation and code — is written in **English** (field `language: en`). Spanish or German versions can come later as a separate cross-lingual experiment.

**Why:** a single, fully English repository is directly usable by any contributor or evaluator, and is the cleanest form for public publication.

## D4 — Case origin (ethics and privacy)
**Fixed rule:** cases reflect real clinical patterns but are **never** based on a specific patient or contain identifiable data.

**Why:** avoids GDPR and ethical issues, and allows the case set to be published.

## D5 — Source of the gold answer
The author's clinical judgement, backed by reference guidelines where available, cited in each case (`references` field). Examples: the IFOMPT International Framework for Red Flags (2020) and the NICE low back pain guideline.

**Why:** a cited source makes every label defensible to any reviewer, not just the author's opinion.

## D6 — Format and storage
- **One YAML file per case** in `cases/`, following `cases/_template.yaml`.
- Strict separation: the `case` block is what the model sees; the `gold` block (expected answer) is never sent to it.
- The `screening` block is **identical in every case** (same questions, same order). Only the answers change, so the length of the history never leaks the answer.
- Everything versioned in Git so results are reproducible.

**Why YAML:** easy to write and read (long clinical text) and loads directly in Python. Automatic schema validation comes later.

## D7 — License (decided at publication time)
Candidate: CC BY 4.0 for the cases and MIT for the code.
