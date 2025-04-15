import json
import os
import configparser


def get_patient_system(user_data, persona):

    user_data_string = (
        "Über den Artzt hast du volgende infos: "
        f"Der Name: {user_data['Vorname']} {user_data['Nachname']} "
        f"Das Geschlecht: {user_data['Geschlecht']} "
        f"Das Alter: {user_data['Alter']} "
        "Bedenke bei deinen Antworten, dass sich Verhaltensweisen eines Menschen abhängig "
        "von seinem gegenüber und der Informationen "
        "über die eigene Person auf seine Verhaltensweisen (zb. wie jemand Angesprochen wird) "
        "auswirken könne. "
    )

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
        f"{user_data_string}\n"
        f"{json.dumps(json.loads(config['PremiumPics']['text']), indent=4)}\n"
        f"{open(os.path.join('data', 'patients', 'supplemental_prompt.txt'),
                'r',
                encoding='utf-8',
                ).read()
        }\n"
    )

    return system_prompt

def get_doctor_system(user_data, doctor_persona):
    #config = configparser.ConfigParser()
    #with open(
    #        f"doctors/{doctor_persona}/doctor_config.ini", "r", encoding="utf-8"
    #) as f:
    #    config.read_file(f)

    user_data_string = (
        "Über dich hast du folgende Informationen: "
        f"Name: {user_data['Vorname']} {user_data['Nachname']}, "
        f"Geschlecht: {user_data['Geschlecht']}, "
        f"Alter: {user_data['Alter']} Jahre.\n"
        "Passe dein Gesprächsverhalten entsprechend an (z.B. kindgerecht, respektvoll, altersangepasst etc.).\n"
    )

    #arzt_info = (
    #    f"Du bist ein Arzt mit dem folgenden Hintergrund: {config['Hintergrund']['text']}\n"
    #    f"Deine Fachrichtung ist: {config['Fachrichtung']['text']}\n"
    #    f"Dein Kommunikationsstil: {config['Kommunikation']['text']}\n"
    #)

    system_prompt = (
        f"{open(os.path.join('data', 'medics', 'pre_prompt.txt'), 'r', encoding='utf-8').read()}\n"
        #f"{arzt_info}"
        f"{user_data_string}"
        f"{open(os.path.join('data', 'medics', 'supplemental_prompt.txt'), 'r', encoding='utf-8').read()}\n"
    )

    return system_prompt
