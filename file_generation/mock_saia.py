# mock_saia.py

# Diese Funktion hier simuliert das OpenAI-Interface
def chat_completions(messages, model):
    # Hier könntest du jetzt die Logik einbauen,
    # die auf die POST-Anfrage an deinen Flask-Server reagiert

    # Für den Anfang reicht ein einfaches Objekt, das die erwartete Struktur hat
    class MockResponse:
        def __init__(self, content):
            self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': content})})]

    return MockResponse("Dies ist eine simulierte Antwort des Modells.")