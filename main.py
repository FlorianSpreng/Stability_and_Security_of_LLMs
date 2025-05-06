import configparser, dotenv, os
import json
import time
from os.path import exists

from openai import OpenAI
from datetime import datetime

from tqdm import tqdm

from processing_en import get_doctor_system, get_patient_system

dotenv.load_dotenv(os.path.join(".", ".env"))
retry_count = 0
failed_runs = []
message = ""
conversation_historie = []
conversation_log = []

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


def thoughtchop(message):
    if "<think>" in message:
        message = message.split("</think>")[1].replace("\n", "")
    return message


def send_message(role, i, system_prompt, model):
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

    print(f"Message={i}, User={role}: {response}")
    conversation_historie.append({"time": now, "role": role, "content": response})
    message = response


def safe_conversation_history(medic_model, patient_model, medic, patient):
    global conversation_log
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    os.makedirs(os.path.join(".log", "meta"), exist_ok=True)
    os.makedirs(os.path.join(".log", "conversation"), exist_ok=True)

    with open(os.path.join(".log", "meta", f"{now}__{medic_model}__{patient_model}.log"), "w", encoding="utf-8") as f:
        f.write(f"{now}\n")
        for item in conversation_log:
            f.write(f"{item}\n\n")
    print(f"conversation safed in {now}.log")

    with open(os.path.join(".log", "conversation", f"{now}__{medic_model}__{patient_model}.log"), "w", encoding="utf-8") as f:
        f.write(f"{now}\n")
        for item in conversation_historie:
            f.write(json.dumps(item, indent=4) + "\n")


def conversation(medic_role, patient_role, medic_model, patient_model, retry=False):
    global conversation_historie
    global conversation_log
    try:
        for i in conv_length:
            if i % 2 != 0:
                send_message("arzt", i, get_doctor_system(medic_role), medic_model)
            else:
                send_message("patient", i, get_patient_system(patient_role), patient_model)
    except Exception as e:
        print(f"Fehler bei Modell {medic_model} oder {patient_model}: {e}")
        # Speichere den fehlerhaften Versuch nur, wenn es kein Retry war (doppelte Einträge vermeiden)
        if not retry:
            failed_runs.append((medic_role, patient_role, medic_model, patient_model))
        return

    safe_conversation_history(medic_model, patient_model, medic_role, patient_role)
    conversation_log = []
    conversation_historie = []


def main():
    global config
    global retry_count
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
                        print(f"Patient={y}, Medic={x}, Patient Model={model_patient}, Medic Model={model_medic}")
                        conversation(f"medic_{x + 1}", f"patient_{y + 1}", model_medic, model_patient)
                        pbar.update(int(config["run specs"]["conv_length"]))
                        time.sleep(3)

    # Retry-Loop für gescheiterte Versuche
    while failed_runs:
        print(f"\nNeuer Durchlauf für {len(failed_runs)} fehlgeschlagene Versuche (Durchlauf {retry_count + 1})")
        current_failed = failed_runs.copy()
        failed_runs.clear()  # Leeren für den neuen Sammeldurchlauf

        for medic_role, patient_role, medic_model, patient_model in current_failed:
            conversation(medic_role, patient_role, medic_model, patient_model, retry=True)
            time.sleep(3)

        retry_count += 1


def mainTest():
    global config
    for model in config["models"]:
        conversation(f"medic_1", f"patient_1", model)
        print(model)
        time.sleep(3)


if __name__ == "__main__":
    main()
