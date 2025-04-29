import configparser, dotenv, os
import json
import time
from os.path import exists

from openai import OpenAI
from datetime import datetime

from tqdm import tqdm

from processing_en import get_doctor_system, get_patient_system

dotenv.load_dotenv(os.path.join(".", ".env"))

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

        messages=[{"role": "system", "content": f"Behaviour: {system_prompt} + conversation history: {conversation_historie}"},
                  {"role": "user", "content": f"{role}: {message}"}
                  ],
        model=model
    )

    conversation_log.append(f"{now}: {chat_completion}")
    response = thoughtchop(chat_completion.choices[0].message.content)

    print(f"Message={i}, User={role}: {response}")
    conversation_historie.append({"time": now, "role": role, "content": response})
    message = response

def safe_conversation_history(model, medic, patient):
    global conversation_log
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not exists(os.path.join(".log", model)):
        os.mkdir(os.path.join(".log", model))
    if not exists(os.path.join(".log", model, "meta")):
        os.mkdir(os.path.join(".log", model, "meta"))
    if not exists(os.path.join(".log", model, "conversation")):
        os.mkdir(os.path.join(".log", model, "conversation"))

    with open(os.path.join(".log",model, "meta", f"{now}.log"), "w", encoding="utf-8") as f:
        #print(f"Model={model}, medic={medic}, patient={patient}\n")
        f.write(f"{now}\n")
        for item in conversation_log:
            f.write(f"{item}\n\n")
    #print(f"conversation safed in {now}.log")

    with open(os.path.join(".log", model, "conversation", f"{now}.log"), "w", encoding="utf-8") as f:
        #print(f"Model={model}, medic={medic}, patient={patient}\n")
        f.write(f"{now}\n")
        for item in conversation_historie:
            f.write(json.dumps(item, indent=4) + "\n")

def conversation(medic_role, patient_role, model):
    global conversation_historie
    global conversation_log
    start_time = datetime.now()
    #print(f"Start", start_time)
    #print("run is running...")
    try:
        for i in conv_length:
            if i % 2 != 0:
                send_message("arzt", i, get_doctor_system(medic_role), model)
            else:
                send_message("patient", i, get_patient_system(patient_role), model)
    except Exception as e:
        print(f"Fehler bei Modell {model}: {e}")
    end_time = datetime.now()
    #print("Ende:", end_time)

    delta = end_time - start_time
    #print("Dauer:", delta)
    #print("In Sekunden:", delta.total_seconds())
    safe_conversation_history(model, medic_role, patient_role)
    conversation_log = []
    conversation_historie = []


def main():
    global config
    total_iterations = (int(config["run specs"]["medic_length"]) *
                        int(config["run specs"]["patient_length"]) *
                        len(config["models"]))

    with tqdm(total=total_iterations, desc="Progress", unit="Step") as pbar:
        for x in medic_length:
            for y in patient_length:
                for model in config["models"]:
                    conversation(f"medic_{x + 1}", f"patient_{y + 1}", model)
                    time.sleep(3)

def mainTest():
    global config
    for model in config["models"]:
        conversation(f"medic_1", f"patient_1", model)
        print(model)
        time.sleep(3)




if __name__ == "__main__":
    mainTest()
