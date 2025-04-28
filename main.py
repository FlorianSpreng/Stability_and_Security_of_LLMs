import configparser, dotenv, os
from openai import OpenAI
from datetime import datetime
from processing import get_doctor_system, get_patient_system

dotenv.load_dotenv(os.path.join(".", ".env"))

message = ""
conversation_historie = []
conversation_log = []

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

def thoughtchop(message):
    if "<think>" in message:
        message = message.split("</think>")[1].replace("\n", "")
    return message


def send_message(role, i, system_prompt, model):
    global message
    global conversation_historie
    global conversation_log

    chat_completion = client.chat.completions.create(

        messages=[{"role": "system", "content": f"Verhaltensanweisung {system_prompt} + bisheriger Gesprächsverlauf: {conversation_historie}"},
                  {"role": "user", "content": f"{role}: {message}"}
                  ],
        model=model
    )

    conversation_log.append(chat_completion)
    response = thoughtchop(chat_completion.choices[0].message.content)

    print(f"Message={i}, User={role}: {response}")
    conversation_historie.append({"role": role, "content": response})
    message = response


def safe_conversation_history(model, medic, patient):
    global conversation_log
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(os.path.join(".log", f"{now}.log"), "w", encoding="utf-8") as f:
        print(f"Model={model}, medic={medic}, patient={patient}\n")
        for item in conversation_log:
            f.write(f"{item}\n")
    print(f"conversation safed in {now}.log")

def run(medic_role, patient_role, model):
    print("1")
    global conversation_historie
    global conversation_log
    start_time = datetime.now()
    print(f"Start", start_time)
    print("run is running...")
    for i in range(1, 10):
        if i % 2 != 0:
            send_message("arzt", i, get_doctor_system(medic_role), model)
        else:
            send_message("patient", i, get_patient_system(patient_role), model)
    end_time = datetime.now()
    print("Ende:", end_time)

    delta = end_time - start_time
    print("Dauer:", delta)
    print("In Sekunden:", delta.total_seconds())
    safe_conversation_history(model, medic_role, patient_role)
    conversation_log = []
    conversation_historie = []

def main():
    config = configparser.ConfigParser()
    with open("config.ini", "r", encoding="utf-8") as f:
        config.read_file(f)
    for x in range(1, 4):
        for y in range(1, 4):
            for model in config["models"]:
                try:
                    run("medic_1", "patient_1", model)
                except Exception as e:
                    print(f"Fehler bei Modell {model}: {e}")

if __name__ == "__main__":
    main()
