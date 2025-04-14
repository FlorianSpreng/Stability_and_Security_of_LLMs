import os

import dotenv
from docutils.nodes import system_message
from openai import OpenAI

dotenv.load_dotenv(".\\.env")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

model = "meta-llama-3.1-8b-instruct"  # Choose any available model
system_content = "You are a helpful assistant"

def sendMessage(message, user, i):
    # Start OpenAI client
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    # Get response
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": system_content},
                  {"role": user, "content": message},
                  #{"role": "assistant",
                  #"content": "The Eiffel Tower stands at a height of 324 meters (1,063 feet) above ground level. "
                  #            "However, if you include the radio antenna on top, the total height is 330 meters (1"
                  #            ",083 feet)."},
                  ],
        model=model,
    )
    print(f"Message={i}, User={user}:", chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


def main():
    message = "Hi, how are you?"
    for i in range(1, 31):
        message = sendMessage(message, "user1", i)
        i += 1
        message = sendMessage(message, "user2", i)
        i += 1

main()
