from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    # Wir holen uns den Request-Body, um zu sehen, was reinkam (optional fürs Debugging)
    data = request.get_json()

    # Hier simulieren wir die Antwortstruktur der Academic Cloud / OpenAI API
    mock_response = {
        "id": "chatcmpl-mock12345",
        "object": "chat.completion",
        "created": 1718020000,
        "model": data.get("model", "mock-model"),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Simulierte Antwort: Der Patient klagt über Kopfschmerzen. Bitte Untersuchung einleiten."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 15,
            "total_tokens": 25
        }
    }
    return jsonify(mock_response)


if __name__ == '__main__':
    # Läuft auf Localhost Port 8000
    app.run(host='127.0.0.1', port=8000)