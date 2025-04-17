import json
import os
import configparser


# Baut aus den informationen aus der patient_{id}_config.ini und der informationen, die über den Arzt vorliegen
# einen Systemprompt
def get_patient_system(persona):
    config = configparser.ConfigParser()
    with open(
            f"data/patients/{persona}_config.ini", "r", encoding="utf-8"
    ) as f:
        config.read_file(f)

    diagnose_string = (
        f"Du hast: {config['Diagnose']['text']}. Bedenke, dass ich diese Info dir als KI mitteile. "
        f"Der Patient ist ein laie und hat von seiner Diagnose keine Ahnung. Die se info ist nur dafür da,"
        f"damit du die beschriebenen symptome anhand der Diagnose besser schildern kannst... Zudem kann "
        f"es im verlauf des gesprächs zu verbesserungen und verschlechterungen des zustandes kommen, was"
        f"du zur Diagnose passend initialisieren kannst/sollst."
    )

    system_prompt = (
        f"{open(os.path.join('data', 'patients', 'pre_prompt.txt'), 'r').read()}\n"
        f"{config['Records']['text']}\n"
        f"{diagnose_string}\n"
        f"Du verfügst über folgende Persoenlichkeit: {config['Persoenlichkeit']['text']}\n"
        f"{open(os.path.join('data', 'patients', 'supplemental_prompt.txt'),
                'r',
                encoding='utf-8',
                ).read()
        }\n"
    )

    return system_prompt


# Baut aus den informationen aus der medic_{id}_config.ini einen Systemprompt
def get_doctor_system(medic):
    config = configparser.ConfigParser()
    with open( os.path.join('data', 'medics', f'{medic}_config.ini'), "r", encoding="utf-8"
    ) as f:
        config.read_file(f)

    user_data_string = (
        "Über dich hast du folgende Informationen: "
        f"Voller Name: {config["personal data"]['prename']} {config["personal data"]['name']}, "
        f"Geschlecht: {config["personal data"]['sex']}, "
        f"Alter: {config["personal data"]['age']} Jahre.\n"
        f"Du bist ein Arzt mit dem folgenden Hintergrund: {config["acting data"]['background']}\n"
        f"Deine Fachrichtung ist: {config["acting data"]['medical_field']}\n"
        f"Dein Kommunikationsstil: {config["acting data"]['communication_style']}\n"
        "Passe dein Gesprächsverhalten entsprechend an (z.B. kindgerecht, respektvoll, altersangepasst etc.).\n"
    )


    system_prompt = (
        f"{open(os.path.join('data', 'medics', 'pre_prompt.txt'), 'r', encoding='utf-8').read()}\n"
        f"{user_data_string}"
        f"{open(os.path.join('data', 'medics', 'supplemental_prompt.txt'), 'r', encoding='utf-8').read()}\n"
    )

    return system_prompt
