import os, configparser


# Builds a system prompt from the information in the patient_{id}_config.ini
# and the information available about the doctor
def get_patient_system(persona):
    config = configparser.ConfigParser()
    with open(
            f"data_en/patients/{persona}_config.ini", "r", encoding="utf-8"
    ) as f:
        config.read_file(f)

    diagnose_string = (
        f"You have: {config['Diagnose']['text']}. Keep in mind that I'm telling you this information as an AI. "
        f"The patient is a layperson and has no knowledge of their diagnosis. This information is only intended "
        f"to help you describe the reported symptoms more accurately based on the diagnosis... Additionally, "
        f"the condition may improve or worsen over the course of the conversation, which you should/can initialize "
        f"appropriately in line with the diagnosis."
    )

    system_prompt = (
        f"{open(os.path.join('data_en', 'patients', 'pre_prompt.txt'), 'r').read()}\n"
        f"{config['Records']['text']}\n"
        f"{diagnose_string}\n"
        f"You have the following personality: {config['Persoenlichkeit']['text']}\n"
        f"{open(os.path.join('data_en', 'patients', 'supplemental_prompt.txt'), 'r', encoding='utf-8').read()}\n"
    )

    return system_prompt


# Builds a system prompt from the information in the medic_{id}_config.ini
def get_doctor_system(medic):
    config = configparser.ConfigParser()
    with open(os.path.join('data_en', 'medics', f'{medic}_config.ini'), "r", encoding="utf-8") as f:
        config.read_file(f)

    user_data_string = (
        "You have the following information about yourself: "
        f"Full name: {config['personal data']['prename']} {config['personal data']['name']}, "
        f"Gender: {config['personal data']['sex']}, "
        f"Age: {config['personal data']['age']} years.\n"
        f"You are a doctor with the following background: {config['acting data']['background']}\n"
        f"Your medical specialty is: {config['acting data']['medical_field']}\n"
        f"Your communication style: {config['acting data']['communication_style']}\n"
        "Adjust your conversational behavior accordingly (e.g., child-appropriate, respectful, age-appropriate, etc.).\n"
    )

    system_prompt = (
        f"{open(os.path.join('data_en', 'medics', 'pre_prompt.txt'), 'r', encoding='utf-8').read()}\n"
        f"{user_data_string}"
        f"{open(os.path.join('data_en', 'medics', 'supplemental_prompt.txt'), 'r', encoding='utf-8').read()}\n"
    )

    return system_prompt
