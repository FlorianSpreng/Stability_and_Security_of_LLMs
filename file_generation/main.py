import configparser, dotenv, os, json, logging, sys, re, time

from logging import info, error
from openai import OpenAI
from datetime import datetime
from tqdm import tqdm

from file_generation.conv_his import ConvHis
from processing.processing import get_doctor_system, get_patient_system
from typing import List, Dict, Any
from mock_saia import chat_completions
import conv_his

failed_runs: List[tuple[str, str, str, str]] = []
message: str = ""
conversation_log: List[Any] = []
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

dotenv.load_dotenv(os.path.join("", ".env"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

config = configparser.ConfigParser()
with open("./config.ini", "r", encoding="utf-8") as f:
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
    model: str,
    conv_his: Dict[datetime, Dict[str, Any]]
) -> None:
    global message
    global conversation_log


    chat_completion = chat_completions( #client.chat.completions.create

        messages=[{"role": "system",
                   "content": f"Behaviour: {system_prompt} + conversation history: {conv_his}"},
                  {"role": "user", "content": f"{role}: {message}"}
                  ],
        model=model
    )
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    conversation_log.append(f"{now}: {chat_completion}")
    response = thoughtchop(chat_completion.choices[0].message.content)

    info(f"Message={i}, User={role}: {response}")
    conv_his.append(now, {"role": role, "content": response})
    message = response


def conversation(
    medic_role: str,
    patient_role: str,
    medic_model: str,
    patient_model: str,
    run: int,
    lang: str
) -> None:
    global conversation_log
    global failed_runs
    global message
    conv_his = ConvHis(f"{medic_model}__{patient_model}")
    statstring = f"Patient={patient_role}, Medic={medic_role}, Patient Model={patient_model}, Medic Model={medic_model}, Try={run}"
    info(statstring)
    try:
        for i in conv_length:
            if i % 2 != 0:
                send_message("arzt", i, get_doctor_system(medic_role, lang), medic_model, conv_his)
            else:
                send_message("patient", i, get_patient_system(patient_role, lang), patient_model, conv_his)
    except Exception as e:
        error(f"Fehler bei Modell {medic_model} oder {patient_model}: {e}")
        failed_runs.append((medic_role, patient_role, medic_model, patient_model))
        conversation_log = []
        conv_his = None
        message = ""
        return

    conv_his.save_conv_his()
    conversation_log = []
    message = ""

def already_done(
    medic_role: str,
    patient_role: str,
    medic_model: str,
    patient_model: str,
    lang: str
) -> bool:
    header = f"Patient={patient_role}, Medic={medic_role}, Patient Model={patient_model}, Medic Model={medic_model}"
    base_path = os.path.join('.log', 'real_data', 'clear', lang, 'conversation')

    # Regex-Pattern für den Dateinamen
    pattern = re.compile(
        r".*__" + re.escape(medic_model) + r"__" + re.escape(patient_model) + r"\.log",
        re.IGNORECASE
    )

    if not os.path.exists(base_path):
        return False

    for file in os.listdir(base_path):
        if pattern.match(file):
            full_path = os.path.join(base_path, file)
            if os.path.isfile(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if header in line:
                            return True
    return False



def main(lang) -> None:
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
                        if not already_done(f"medic_{x + 1}", f"patient_{y + 1}" , model_medic, model_patient, lang):
                            conversation(f"medic_{x + 1}", f"patient_{y + 1}", model_medic, model_patient, retry_count, lang)
                            time.sleep(3)
                        pbar.update(int(config["run specs"]["conv_length"]))

    retry_count += 1

    # Retry-Loop für gescheiterte Versuche
    while failed_runs:
        info(f"\nNeuer Durchlauf für {len(failed_runs)} fehlgeschlagene Versuche (Durchlauf {retry_count})")
        current_failed = failed_runs.copy()
        failed_runs.clear()  # Leeren für den neuen Sammeldurchlauf

        with tqdm(total=len(current_failed)*int(config["run specs"]["conv_length"]), desc="Progress", unit="Step") as pbar:
            for medic_role, patient_role, medic_model, patient_model in current_failed:
                if not already_done(patient_role, medic_role, medic_model, patient_model, lang):
                    info(f"Patient={patient_role}, Medic={medic_role}, Patient Model={patient_model}, Medic Model={medic_model}")
                    conversation(medic_role, patient_role, medic_model, patient_model, retry_count, lang)
                    time.sleep(3)
                pbar.update(int(config["run specs"]["conv_length"]))

        retry_count += 1


if __name__ == "__main__":
    main(sys.argv[1])

