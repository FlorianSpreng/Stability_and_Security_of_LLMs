import os
import json
from typing import Dict, Any


class ConvHis:
    def __init__(self, con_name: str):
        self.name = con_name
        self.conversation_historie: Dict[str, Any] = {}

    def append(self, time: str, data: Any):
        # Wir speichern das komplette Objekt (Dict), damit nichts verloren geht
        self.conversation_historie[time] = data

    def save_conv_his(self):
        # Sicherer Pfad
        directory = os.path.join(".log", "test")
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, f"{self.name}.json")

        # Speichern mit Puffer-Leerung
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.conversation_historie, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())