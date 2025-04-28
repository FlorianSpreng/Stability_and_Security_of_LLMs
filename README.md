# Stability and Security of LLMs
This program is used to generate a large number of conversations between a simulated patient and a simulated medic. The project has the following properties:

## Used Models
This selection of **L**arge **L**anguage **M**odels is based on a list curated by SAIA (**S**calable **A**rtificial **I**ntelligence **A**ccelerator), which is part of the **Gesellschaft für Wissenschaftliche Datenverarbeitung mbH Göttingen**. These free models will be used for the experiment:
- Llama 3.1 8B Instruct
- InternVL2.5 8B MPO
- DeepSeek R1
- DeepSeek R1 Distill Llama 70B
- Llama 3.3 70B Instruct
- Llama 3.1 SauerkrautLM Instruct
- Llama 3.1 Nemotron 70B
- Mistral Large Instruct
- Codestral 22B
- E5 Mistral 7B Instruct
- Qwen 2.5 72B Instruct
- Qwen 2.5 VL 72B Instruct
- Qwen 2.5 Coder 32B Instruct

## Used Personas
These are the characters simulated by the models for the conversations.

### Patients
- Anna Schmidt is experiencing severe shortness of breath, chest pain that worsens with deep breathing, tachycardia, and an unusual cough with possible blood. She is afraid of suffocating and is struggling to breathe and think clearly. Diagnosis: pulmonary embolism.
- Markus Huber is experiencing sudden, severe eye pain, headaches, blurred vision, halos around lights, and discomfort in the red, dilated eye. The diagnosis is acute glaucoma. The patient is seeking urgent help due to the intense pain and visual disturbances.
- Laura Fischer has been experiencing a persistent cough for several days, with increasing pain behind the breastbone, shortness of breath, and fever. The diagnosis is acute bronchitis. The patient is anxious and shy about the condition, but now feels concerned due to the prolonged symptoms and hopes it’s not something serious.

### Medics
- Johannes Krämer is an experienced general practitioner with over 25 years of work in a large hospital. He now practices in a rural setting, where his communication style is patient and thorough, often using relatable analogies to explain medical concepts.
- Sofia Ben Salem is an experienced internal medicine specialist with a background in multicultural care, having worked for 10 years at a university hospital. She communicates in an analytical, precise manner, and is particularly effective when addressing complex medical cases.
- Mehmet Yilmaz is a pulmonologist with extensive experience in acute care, having worked in emergency departments for many years. He now runs a practice focused on chronic diseases. His communication style is quick, goal-focused, and slightly ironic, but always caring and direct.

## Conversation Specification
To guarantee the consistency of conversations, we define several constants to better understand the complexity of the project.

- **Conversation length:** 30 messages
- **Number of Medics:** 3
- **Number of Patients:** 3 (fixed)
- **Number of LLMs:** 12 (as listed above)
- **Number of Conversations:** <br>
   $
   N_{\text{dialogues}} = N_{\text{patient types}} \times N_{\text{medic types}} \times N_{\text{patient LLMs}} \times N_{\text{medic LLMs}} = 3 \times 3 \times 12 \times 12 = 1296 \text{ dialogues}
   $
- **Number of Messages:** <br>
   $
   N_{\text{messages}} = N_{\text{dialogues}} \times \text{Conversation length} = 1296 \times 30 = 38880 \text{ messages}
   $