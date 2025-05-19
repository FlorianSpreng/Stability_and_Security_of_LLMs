import json
import re
from pathlib import Path
from collections import defaultdict

conversation_path = Path('.log/real_data/clear/en/conversation')
conversations = []

def extract_infos_from_header(lines):
    for line in lines:
        if line.startswith("Patient="):
            match = re.search(
                r'Patient=(patient_\d+), Medic=(medic_\d+), Patient Model=([a-zA-Z0-9\.\-]+), Medic Model=([a-zA-Z0-9\.\-]+), Try=(\d+)',
                line)
            if match:
                return match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)
    return None, None, None, None, None

for file in sorted(conversation_path.glob('*.log')):
    with file.open(encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 2:
        print("❌ Fehler beim Lesen der Datei:", file.name)
        continue

    patient_id, medic_id, patient_model, medic_model, tries = extract_infos_from_header(lines[:5])
    if not all([patient_id, medic_id, patient_model, medic_model, tries]):
        print(f"⚠️ Fehlerhafte Header-Zeile in Datei: {file.name}")
        continue

    conversations.append({
        'file': file.name,
        'patient_id': patient_id,
        'medic_id': medic_id,
        'patient_model': patient_model,
        'medic_model': medic_model,
        'tries': int(tries),
    })

# Übersicht ausgeben
for conv in conversations:
    print(f"📄 Datei:             {conv['file']}")
    print(f"   - Patient-ID:      {conv['patient_id'].split('_')[1]}")
    print(f"   - Medic-ID:        {conv['medic_id'].split('_')[1]}")
    print(f"   - Patient-Model:   {conv['patient_model']}")
    print(f"   - Medic-Model:     {conv['medic_model']}")
    print(f"   - Tries:           {conv['tries']}")
    print("")
