import configparser, dotenv, os, time, json, logging, sys
from logging import info, error

from openai import OpenAI
from datetime import datetime
from tqdm import tqdm
from processing_en import get_doctor_system, get_patient_system

from typing import List, Dict, Any

failed_runs: List[tuple[str, str, str, str]] = []
message: str = ""
conversation_historie: List[Dict[str, Any]] = []
conversation_log: List[Any] = []

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout  # <--- statt stderr
)

dotenv.load_dotenv(os.path.join(".", ".env"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

config = configparser.ConfigParser()
with open("config.ini", "r", encoding="utf-8") as f:
    config.read_file(f)

conv_length = range(1, int(config["run specs"]["conv_length"]))
patient_length = range(int(config["run specs"]["patient_length"]))
medic_length = range(int(config["run specs"]["medic_length"]))


def thoughtchop(message: str) -> str:
    if "<think>" in message:
        message = message.split("</think>")[1].replace("\n", "")
    return message


def send_message(
    role: str,
    i: int,
    system_prompt: str,
    model: str
) -> None:
    global message
    global conversation_historie
    global conversation_log

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    chat_completion = client.chat.completions.create(

        messages=[{"role": "system",
                   "content": f"Behaviour: {system_prompt} + conversation history: {conversation_historie}"},
                  {"role": "user", "content": f"{role}: {message}"}
                  ],
        model=model
    )

    conversation_log.append(f"{now}: {chat_completion}")
    response = thoughtchop(chat_completion.choices[0].message.content)

    info(f"Message={i}, User={role}: {response}")
    conversation_historie.append({"time": now, "role": role, "content": response})
    message = response


def safe_conversation_history(
    medic_model: str,
    patient_model: str,
    statstring: str
) -> None:
    global conversation_log
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs(os.path.join(".log", "meta"), exist_ok=True)
    os.makedirs(os.path.join(".log", "conversation"), exist_ok=True)

    with open(os.path.join(".log", "meta", f"{now}__{medic_model}__{patient_model}.log"), "w", encoding="utf-8") as f:
        f.write(f"{now}\n")
        f.write(f"{statstring}\n")
        for item in conversation_log:
            f.write(f"{item}\n\n")
    info(f"meta conversation safed in {os.path.join('.log', 'meta', f'{now}__{medic_model}__{patient_model}.log')}")

    with open(os.path.join(".log", "conversation", f"{now}__{medic_model}__{patient_model}.log"), "w", encoding="utf-8") as f:
        f.write(f"{now}\n")
        f.write(f"{statstring}\n")
        for item in conversation_historie:
            f.write(json.dumps(item, indent=4) + "\n")
    info(f"conversation safed in {os.path.join('.log', 'conversation', f'{now}__{medic_model}__{patient_model}.log')}")


def conversation(
    medic_role: str,
    patient_role: str,
    medic_model: str,
    patient_model: str,
    run: int
) -> None:
    global conversation_historie
    global conversation_log
    global failed_runs
    statstring = f"Patient={patient_role}, Medic={medic_role}, Patient Model={patient_model}, Medic Model={medic_model}, Try={run}"
    info(statstring)
    try:
        for i in conv_length:
            if i % 2 != 0:
                send_message("arzt", i, get_doctor_system(medic_role), medic_model)
            else:
                send_message("patient", i, get_patient_system(patient_role), patient_model)
    except Exception as e:
        error(f"Fehler bei Modell {medic_model} oder {patient_model}: {e}")
        failed_runs.append((medic_role, patient_role, medic_model, patient_model))
        conversation_log = []
        conversation_historie = []
        return

    safe_conversation_history(medic_model, patient_model, statstring)
    conversation_log = []
    conversation_historie = []


def main() -> None:
    global config
    global failed_runs
    retry_count = 0

    total_iterations = ((int(config["run specs"]["medic_length"])) *
                        (int(config["run specs"]["patient_length"])) *
                        len(config["models"]) *
                        len(config["models"])*
                        int(config["run specs"]["conv_length"]))

    with tqdm(total=total_iterations, desc="Progress", unit="Step") as pbar:
        for x in medic_length:
            for y in patient_length:
                for model_medic in config["models"]:
                    for model_patient in config["models"]:
                        conversation(f"medic_{x + 1}", f"patient_{y + 1}", model_medic, model_patient, retry_count)
                        pbar.update(int(config["run specs"]["conv_length"]))
                        time.sleep(3)

    retry_count += 1

    # Retry-Loop für gescheiterte Versuche
    while failed_runs:
        info(f"\nNeuer Durchlauf für {len(failed_runs)} fehlgeschlagene Versuche (Durchlauf {retry_count})")
        current_failed = failed_runs.copy()
        failed_runs.clear()  # Leeren für den neuen Sammeldurchlauf

        with tqdm(total=len(current_failed)*int(config["run specs"]["conv_length"]), desc="Progress", unit="Step") as pbar:
            for medic_role, patient_role, medic_model, patient_model in current_failed:
                info(f"Patient={patient_role}, Medic={medic_role}, Patient Model={patient_model}, Medic Model={medic_model}")
                conversation(medic_role, patient_role, medic_model, patient_model, retry_count)
                pbar.update(int(config["run specs"]["conv_length"]))
                time.sleep(3)

        retry_count += 1


if __name__ == "__main__":
    main()
