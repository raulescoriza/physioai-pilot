# PhysioAI

A case set and evaluation harness for measuring whether LLMs reason **safely and with clinical
appropriateness** on outpatient musculoskeletal physiotherapy cases: detecting red flags,
deciding on referral and its urgency, formulating hypotheses and proposing an evidence-based plan.

All cases are real clinical patterns but are never based on a specific patient and contain no identifiable data.

## Repository layout

```
cases/          One YAML file per case (see cases/_template.yaml)
prompts/        System prompts (prompts/system_v1.md)
results/        Model outputs and scores, organised by date and model
docs/           Scope and design decisions for the case set
run_case.py     Runs every case against a model and scores the answer
summarize.py    Aggregates a run: sensitivity, specificity, referral error counts
```

## Case format

Each case file has two blocks:

- **`case`** — the only thing sent to the model: patient data, chief complaint, history,
  symptom behaviour, a **standardised screening block** (identical questions, same order, in
  every case, so the length of the history never leaks the answer), regional screening,
  past history, medication and examination findings.
- **`gold`** — the expected answer, **never sent to the model**: red flag and its type,
  suspicion level, referral level, primary and acceptable hypotheses, plan elements that must
  be included or avoided, safety-netting advice and the references backing the label.

Cases are labelled `standard`, `red_flag` (a true red flag requiring referral) or
`confounder` (looks alarming but is not — measuring over-referral, which is also a
clinical error).

The full design rationale lives in [`docs/scope.md`](docs/scope.md).

## Requirements

- Python 3.10+
- An OpenAI-compatible chat completions endpoint (local or hosted)

```
pip install -r requirements.txt
```

## Configuration

Copy the example environment file and fill in your own values:

```
cp .env.example .env
```

```
LLM_BASE_URL=...   # base URL of your OpenAI-compatible endpoint (…/v1)
LLM_MODEL=...      # model name to request
LLM_API_KEY=...    # API key (or your endpoint's value)
```

`.env` is gitignored and must never be committed.

## Usage

```
python run_case.py     # runs every case in cases/ against the configured model
python summarize.py    # summarises the latest run (sensitivity / specificity)
```

Each case is stored under `results/<date>/<model>/<case-id>.json` with the raw response,
the parsed JSON answer, the scores against the gold, and the expected values.

## Status

Pilot set: 10 cases across 5 regions (3 lumbar, 2 cervical, 2 shoulder, 2 knee, 1 ankle/foot).
The full case set (100 cases) is being built following the same template. The gold labels
remain under clinical review where noted in the case headers.

## License

To be decided at publication: CC BY 4.0 for the cases, MIT for the code (see
[`docs/scope.md`](docs/scope.md), D7).
