import os

import dotenv
from black.trans import defaultdict
from openai import OpenAI
from prisma.models import conversation

from processing import get_doctor_system, get_patient_system

dotenv.load_dotenv(".\\.env")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

model = "meta-llama-3.1-8b-instruct"  # Choose any available model
system_content = "You are a helpful assistant"

user_data = {
    "Vorname": "Florian",
    "Nachname": "Spreng",
    "Geschlecht": "Männlich",
    "Alter": 22
}

conversation_historie = []


def sendMessage(message, role, i):
    # Start OpenAI client
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    if role == "patient":
        role_content = get_patient_system(user_data, "patient_1")
    elif role == "medic":
        role_content = get_doctor_system(user_data, "medic_1")

    # Get response
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": role_content},
                  {"role": role, "content": message},
                  {"role": role, "content": f"Das ist der bisherige gesprächsverlauf: {conversation_historie}"}
                  ],
        model=model,
    )
    print(f"Message={i}, User={role}:", chat_completion.choices[0].message.content)
    conversation_historie.append(f"Message={i}, User={role}:{chat_completion.choices[0].message.content}")
    return chat_completion.choices[0].message.content


def main():
    message = "Guten Tag, wie geht es ihnen"
    conversation_historie.append(f"Message=0, User=medic:{message}")
    print(f"Message=0, User=medic:", message)
    for i in range(1, 10):
        message = sendMessage(message, "patient", i)
        i += 1
        message = sendMessage(message, "medic", i)
        i += 1


main()
