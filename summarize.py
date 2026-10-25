import json
from pathlib import Path

results_dir = Path("results") / "2026-10-18" / "qwen3.8-27b"
referral_counts = {"correct": 0, "under": 0, "over": 0, "invalid": 0, "not_evaluable": 0}


red_flag_cases = 0
red_flag_detected = 0

no_red_flag_cases = 0
no_red_flag_correct = 0

results = []

for result_dir in sorted(results_dir.glob("*.json")):
    with open(result_dir, "r", encoding="utf-8") as f:
        result = json.load(f)
    results.append(result) 

for result in results:
    error = result["scores"]["referral_error"]
    if error is None:
        error = "not_evaluable"
    referral_counts[error] += 1

for result in results:
    if result["expected"]["red_flag"] is True:
        red_flag_cases += 1
        if result["scores"]["red_flag_correct"] is True:
            red_flag_detected += 1

if red_flag_cases > 0:
    sensitivity = red_flag_detected / red_flag_cases
    print(f"Sensitivity: {red_flag_detected}/{red_flag_cases} = {sensitivity:.0%}")
else:
    print("No red flags cases")

for result in results:
    if result["expected"]["red_flag"] is False:
        no_red_flag_cases += 1
        if result["scores"]["red_flag_correct"] is True:
            no_red_flag_correct += 1
if no_red_flag_cases > 0:
    specificity = no_red_flag_correct / no_red_flag_cases
    print(f"Specificity: {no_red_flag_correct}/{no_red_flag_cases} = {specificity:.0%}")