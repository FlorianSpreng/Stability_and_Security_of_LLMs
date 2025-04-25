import os
import dotenv
from openai import OpenAI

from processing import get_doctor_system, get_patient_system

dotenv.load_dotenv(os.path.join(".", ".env"))

model = "meta-llama-3.1-8b-instruct"  # Choose any available model
system_content = "You are a helpful assistant"

message = ""

user_data = {
    "Vorname": "Florian",
    "Nachname": "Spreng",
    "Geschlecht": "Männlich",
    "Alter": 22
}

conversation_historie = []

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)


def get_configurations():
    pass


def send_message(role, i, system_prompt):
    global message

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": f"Verhaltensanweisung {system_prompt} + bisheriger Gesprächsverlauf: {conversation_historie}"},
            {"role": role,
             "content": message}
                  ],
        model=model,
    )

    response = chat_completion.choices[0].message.content
    print(f"Message={i}, User={role}: {response}")
    conversation_historie.append({"role": role, "content": response})
    message = response


def main():
    for x in range(1,4):
        for y in range(1,4):
            for i in range(1, 10):
                if i % 2 != 0:
                    send_message("arzt", i, get_doctor_system(f"medic_{x}"))
                else:
                    send_message("patient", i, get_patient_system(f"patient_{y}"))


if __name__ == "__main__":
    main()
