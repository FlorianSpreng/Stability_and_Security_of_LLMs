import hashlib
import os
from pathlib import Path

conversation_path = Path('.', '.log', 'real_data', 'clear', 'en', 'conversation')
encrypted_conversation_path = str(conversation_path).replace("clear", "encrypted")
encrypted_conversation_path = Path(encrypted_conversation_path)
os.makedirs(encrypted_conversation_path, exist_ok=True)

def anonymize_filename(filename: str) -> str:
    """Erzeugt einen MD5 Hash des Dateinamens und hängt die originale Dateiendung an."""
    base, ext = os.path.splitext(filename)
    hashed = hashlib.md5(base.encode('utf-8')).hexdigest()
    return hashed + ext

for file in sorted(conversation_path.glob('*.log')):
    with file.open(encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    encrypted_file_name = anonymize_filename(file.name)

    # Schreibe die Zuordnung in codes.txt (richtiger Modus: 'a')
    with open(os.path.join(encrypted_conversation_path, 'codes.txt'), 'a', encoding='utf-8') as f:
        f.write(f"{file.name} : {encrypted_file_name}\n")

    # Schreibe die gefilterten Inhalte in die Zieldatei
    with open(os.path.join(encrypted_conversation_path, encrypted_file_name), 'w', encoding='utf-8') as f:
        for line in lines:
            entferne = "\","
            if "\"role\":" in line:
                f.write(f"\n{
                    line.split('\"role\":')[1].translate(str.maketrans('', '', entferne)).strip()}:")
            if "\"content\":" in line:
                f.write(f"\n{
                    line.split('content\":')[1].translate(str.maketrans('', '', entferne)).strip()}\n")
