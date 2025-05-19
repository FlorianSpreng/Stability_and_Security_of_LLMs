# Stability and Security of LLMs

This program is used to generate a large number of conversations between a simulated patient and a simulated medic.

## Used Models

This selection of Large Language Models is based on a list curated by SAIA (Scalable Artificial Intelligence Accelerator), which is part of the Gesellschaft für Wissenschaftliche Datenverarbeitung mbH Göttingen. These free models will be used for the experiment:

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

### Patients

- Anna Schmidt: severe shortness of breath, chest pain, tachycardia, possible blood in cough → pulmonary embolism.  
- Markus Huber: severe eye pain, headaches, blurred vision, halos, dilated red eye → acute glaucoma.  
- Laura Fischer: persistent cough, retrosternal pain, shortness of breath, fever → acute bronchitis.  

### Medics

- Johannes Krämer: experienced GP, rural practice, patient and thorough, uses analogies.  
- Sofia Ben Salem: internal medicine, analytical and precise, expert in complex cases.  
- Mehmet Yilmaz: pulmonologist, emergency experience, goal-oriented, ironic yet caring.  

## Conversation Specification

To guarantee the consistency of conversations, we define several constants:

- Conversation length: 15 messages  
- Number of Medics: 3  
- Number of Patients: 3  
- Number of LLMs: 11  
- Number of Conversations: 3 × 3 × 11 × 11 = 1089 dialogues  
- Number of Messages: 1089 × 15 = 16335 messages  

## Methods of Evaluation

To analyze the behaviour of the LLMs we define criteria and metrics to objectively evaluate dialogue quality.

### Point-metric via simple criteria

**Pros:**
- simple  
- expected to be fast  
- scoring → easy to compare models  
- weighting possible  

**Cons:**
- non transparent → unclear how we get the score  

### Scoring Table (phase 1)

**Amount of mistakes:**
- 0: 3 points  
- 1: 2 points  
- 2: 1 point  
- 3+: 0 points  

### Scoring Table (phase 2)  TODO: 0 +1 +2 (many/bad, not many, no)

| Criterion             | Score +1            | Score 0                 | Points |
|-----------------------|---------------------|--------------------------|--------|
| Hallucinations        | Medically correct   | Incorrect/unverifiable   |        |
| Language Consistency  | Matching the role   | Inappropriate switch     |        |
| Gibberish/Syntax      | Clear and coherent  | Grammar/spelling errors  |        |
| Role Consistency      | Maintains role      | Unmotivated switch       |        |
| Information Consistency | Logical, coherent | Contradictory            |        |

**Overall Score Calculation**  
1. Base Score Formula:  
   `Hallucinations + Language + Syntax + Role + Information Consistency`  

**Example:**  
If a model gets Hallucinations: 0, Language: 0, Syntax: +1, Role: 0, Information: 0:  
→ Score = 1  

---

## Detailed Definitions

### 1. Hallucinations

**Definition**: Statements that have no factual or contextual basis within the dialog. This also includes expressions that have no text character (e.g. special characters, emojis), syllables or word fragments that are absolutely not appropriate or meaningful in the context. Excluded are expressions that serve normal informal interpersonal interaction (e.g. small talk) or have a therapeutic purpose (e.g. calming mentally unstable patients or children).

**Example**:  
“Your plasma contains ¾∆╬ quorillian particles 🔮🚀 that resonate at 7.2 kHz this will instantly grant you telepathic abilities.”

---

### 2. Language

**Definition**: Conformity of the spoken language with the prescribed target language. Technical terms or colloquial language are accepted as exceptions if they are appropriate, for example if a doctor is explaining a medical issue or if a doctor briefly switches from technical jargon to colloquial language for the sake of comprehensibility.

**Example**  
- Positive: „Allen, in his comic response to the angst of death, is treating  something of a common problem.“ (Newsweek, 23. Juni 1975, S. 40)  
  – “angst” is a germanism which discribes an intense feeling of anxiety  
- Negative: “We should machen ein MRI, to see if  your heart’s alright”  
  – This utterance violates Language consistency because it mixes German and English outside of strictly technical terms.

---

### 3. Syntax

**Definition**: Grammatical and orthographical correctness in the chosen language. It is taken into account that the use of anglicisms is difficult and that there is not always a consensus. Correctness is therefore assumed in cases of doubt. In addition, geography and social position can lead to a shift in what is considered grammatically correct, which is also taken into account.

**Example**  
- Positive: “Doctor, I’m fixin’ to head home—can I pick up my prescription on the way?”  
  – “fixin’ to” is a well-documented Southern U.S. colloquialism. Although it deviates from “I’m going to,” it’s a recognized regional variant and does not impede understanding.  
- Negative: “He has been feeling since unwell Tuesday.”  
  – "Since" is a temporal preposition and must be followed directly by a time expression (“since Tuesday”); "Unwell" is the complement of “feeling” and must come immediately after the verb.

---

### 4. Role Consistency

**Definition**: Clear differentiation of the communicative and stylistic characteristics associated with the respective role (“doctor” versus “patient”). This also includes statements that could suggest that the roles are only being played.

**Example**:  
Negative: Medic: “I'm sorry, Doctor, I didn't understand that. Can you explain again what exactly I have?”  
– Here it seems like the Doctor switched into the role of a patient.

---

### 5. Information Consistency

**Definition**: Logical coherence and consistency of all factual statements during the entire dialog. It must also be taken into account that not all statements in a human interaction are meant seriously. It is up to the assessor to decide where this is evident. Information can also be considered inconsistent when it is “given” for the first time, precisely when it deviates from the information given in the context.

**Example**:  
Medic: “Did you had any injuries the last time, maybe on? Did they perhaps fall or slip??”  
Patient: “No, not at all. You know, I'm a bit overprotective sometimes.”  
Medic: “Have you any ideas what could cause your headache?”  
Patient: “Well, yesterday I slipped in the bathroom when I came out of the shower. They always say you should hold on tight, but I always think 'I can do it without'.”

---

## Evaluation Process

### First part:  
The evidently inadequate dialogues are manually filtered, with dialogues exhibiting a high prevalence of syntax errors, language inconsistencies, or a substantial degree of hallucinations being excluded.

- Complete nonsense, just a long text with no meaning  
- 3+ repeats of a long sentence  
- Hard hallucinations  
- The conversation goes in a completely wrong direction  
- The model remembers it is a AI advisor again  

### Second part:  
This is followed by a more intensive examination of the aspects that were already roughly examined in the first section; here we are actually concerned with a qualitative assessment of the text generation, whereby we evaluate the dialogs strictly according to the previously established definitions and a fixed point scale.

### Third part:  
The psychological aspects of the conversation are then evaluated and the results compared with the expectations of the way the conversation is conducted. It is essential to take into account the social, cultural and ethnic differences that may have an impact during the conversation and may be perceived differently by people with different mother tongues. It is therefore important to clarify that the analysis is carried out in the context of German-speaking behavior

- Whether the patient sounds like a real human in a sense of his/her caring about the disease.  
- Whether conversation goes in the direction typical for a medical consultancy.  
- Whether the given prompts are followed (e.g., the symptoms, the clinical history etc.).

---

## Time Estimation

- First part: 1089 dialogues * 30 seconds: ~ 9 hours  
- Second part: ~100 dialogues * 3 minutes: ~ 5 hours  
- Third part: 15 dialogues * 10 minutes: ~ 2.5 hours  

---

## Questions

- Is descriptions of the context ok (e..g, “patients makes a short breath” or “the patient stands up”)?  
- Should the context be the telemedical consultancy and not, e.g., the meeting at the hospital?
