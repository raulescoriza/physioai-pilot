import yaml
import json
from datetime import datetime
from pathlib import Path
import os
import urllib.request
from dotenv import load_dotenv

load_dotenv()   # lee el .env y carga sus valores

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_API_KEY = os.getenv("LLM_API_KEY")

REFERRAL_LEVELS = ["none", "routine", "urgent", "emergency"]

with open ("prompts/system_v1.md", "r", encoding="utf-8") as file:
        system_prompt = file.read()

# To read all the cases, store in a variable all the cases
case_paths = sorted(Path("cases").glob("*.yaml"))

def call_model(system_prompt, user_message):
    url = f"{LLM_BASE_URL}/chat/completions"

    # 1. Lo que enviamos: el modelo y los dos mensajes
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0,
    }

    # 2. Montar la petición: el JSON pasa a bytes y se indican las cabeceras
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}",
        },
        method="POST",
    )

    # 3. Enviarla y leer la respuesta
    with urllib.request.urlopen(request, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    # 4. Sacar solo el texto del modelo
    return data["choices"][0]["message"]["content"]

def evaluate_case(case_path):

    with open (case_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    case = data["case"]
    gold = data["gold"]

    user_message = yaml.dump(case, allow_unicode=True, sort_keys=False)

    response = call_model(system_prompt, user_message)

    parsed = None
    parse_error = None

    try: 
        parsed = json.loads(response)
    
    except json.JSONDecodeError as e:
        parse_error = str(e)

    if parsed is None:
        red_flag_correct = None
        referral_correct = None
        referral_error = None
    else:
        red_flag_correct = gold["red_flag"] == parsed["red_flag"]

        if parsed["referral"] not in REFERRAL_LEVELS:
            referral_correct = False
            referral_error = "invalid"
        else:
            referral_correct = gold["referral"] == parsed["referral"]
            diff = REFERRAL_LEVELS.index(gold["referral"]) - REFERRAL_LEVELS.index(parsed["referral"])
            if diff == 0:
                referral_error = "correct"
            elif diff > 0:
                referral_error = "under"
            else:
                referral_error = "over"


    result = {
        "case_id" : data["id"],
        "case_version" : data["version"],
        "model" : LLM_MODEL,
        "prompt_version" : "system_v1",
        "timestamp" : datetime.now().isoformat(),
        "raw_response" : response,
        "parsed" : parsed,
        "parse_error" : parse_error,
        "scores": {
            "red_flag_correct": red_flag_correct,
            "referral_correct": referral_correct,
            "referral_error" : referral_error
        },
        "expected": {
            "red_flag": gold["red_flag"],
            "referral": gold["referral"],
},
    }
    # print(parsed["red_flag"])
    #print(json.dumps(result, ensure_ascii=False, indent=2))

    # strfttime convert the date into string with the choosen format, in this case: "2026-10-17"
    today = datetime.now().strftime("%Y-%m-%d")

    # with Path, it creates the route within the text-> results/today/result/...
    out_path = Path("results") / today / result["model"]/ f"{data['id']}.json"

    # creates the directories, parents= create the parent missing repositories, exist = if it exists, 
    # nothing else happens
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # with the route, w to write, it "opens like an empty blank", then 
    # with json.dump what you want to write, in which file (f), and how.
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    #print(red_flag_correct)
    #print(f"Guardado en {out_path}")

for case_path in case_paths:
    if case_path.name.startswith("_"):
        continue
    evaluate_case(case_path)