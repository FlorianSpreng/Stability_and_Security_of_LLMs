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

- **Conversation length:** 15 messages
- **Number of Medics:** 3
- **Number of Patients:** 3 (fixed)
- **Number of LLMs:** 11 (as listed above)
- **Number of Conversations:** <br>
   $
   N_{\text{dialogues}} = N_{\text{patient types}} \times N_{\text{medic types}} \times N_{\text{patient LLMs}} \times N_{\text{medic LLMs}} = 3 \times 3 \times 11 \times 11 = 1089 \text{ dialogues}
   $
- **Number of Messages:** <br>
   $
   N_{\text{messages}} = N_{\text{dialogues}} \times \text{Conversation length} = 1089 \times 15 = 16335 \text{ messages}
   $

## Methods of Evaluation
To analyze the bahaviour of th LLMs we have to find specific creteria and metrics to evaluate the quality of an dialogue
objectively. In general we can use two systems:

### Pointmetric via simple creteria
Here we would define several aspects which want or don't wan to see  in the dialogues. Whenever we notice one of this
aspects in the dialogue, we give the model the predetermined amount of points (e.g. -1 for negative and +1 for positive 
aspects) so we can offset when a dialog has both good and bad aspects.

#### (+)
 - simple
 - expected to be fast
 - scoring 
   -> easy to compare models
 - Weighting possible
#### (-)
 - non transparent
   -> unclear how we get the score

#### Bewertungstabelle
| **Criterion**               | **Score +1**                                             | **Score -1**                                         | **Weight** | **Points** |
|-----------------------------|----------------------------------------------------------|------------------------------------------------------|------------|------------|
| **Hallucinations**          | Medically correct and verifiable statements              | Medically incorrect or unverifiable statements       | 30%        |            |
| **Language Consistency**    | Consistent language matching the role                    | Sudden, inappropriate language switch                | 20%        |            |
| **Gibberish/Syntax Errors** | Grammatically correct, clear and coherent                | Spelling mistakes, grammar errors, unclear structure | 10%        |            |
| **Role Consistency**        | Maintains the assigned role throughout                   | Unmotivated or accidental role switches              | 15%        |            |
| **Information Consistency** | Logical, coherent information                            | Contradictory or inconsistent information            | 15%        |            |
| **Misinformation**          | Accurate and precise medical explanations                | Inaccurate or misleading medical explanations        | 10%        |            |
| **Model Purpose Awareness** | Clearly states it's not designed for dialogue (bonus)    | (n/a – no penalty if not stated)                     | +5% bonus  |            |


**Overall Score Calculation:**

1. **Base Score:**

$$
\text{Base Score} = (\text{Hallucinations points} \times 0.3) + (\text{Language Consistency points} \times 0.20) + (\text{Gibberish/Syntax Errors points} \times 0.10) + (\text{Role Consistency points} \times 0.15) + (\text{Information Consistency points} \times 0.15) + (\text{Misinformation points} \times 0.10)
$$

2. **Bonus:**

If the model shows **purpose awareness**, add +0.05 to the final result.

**Example:**

If a model gets:
- Hallucinations: 0
- Language Consistency: -1
- Gibberish/Syntax Errors: +1
- Role Consistency: 0
- Information Consistency: -1
- Misinformation: +1
- Purpose Awareness: +1 (bonus)

You get:

$$
\text{Base Score} = (0 \times 0.3) + (-1 \times 0.20) + (1 \times 0.10) + (0 \times 0.15) + (-1 \times 0.15) + (1 \times 0.10) = -0.15
$$

**Total Score = Base Score + Bonus = -0.20 + 0.05 = -0.15**
