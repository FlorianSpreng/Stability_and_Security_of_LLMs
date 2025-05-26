import os
import gradio as gr
from typing import Tuple, List

# === Vorbereitung ===
LOG_DIR = os.path.join(".log", "real_data", "encrypted", "de", "conversation")
log_files: List[str] = sorted([os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR) if f.endswith(".log")])
total_files: int = len(log_files)

CATEGORIES: List[str] = [
    "Hallucinations",
    "Language Consistency",
    "Gibberish/Syntax",
    "Role Consistency",
    "Information Consistency"
]

def setfile(index: int):
    if index < 5:
        index = index + 1
        output_box = gr.Textbox(lines=30,
                                label=f"File {index}/{len(log_files)}",
                                value=open(log_files[index - 1]).read(),
                                interactive=False)
        return output_box, index
    return gr.Textbox(lines=30,
                      label="Gespräch",
                      value = "",
                      interactive=False), index

with gr.Blocks() as demo:
    state = gr.State(0)  # Index der aktuellen Datei
    counters = gr.State([0] * (2 * len(CATEGORIES)))  # Zähler für Arzt + Patient

    output_box, state.value = setfile(0)
    next_button = gr.Button("Nächste Datei")
    next_button.click(
        fn=setfile,
        inputs=[state],
        outputs=[output_box, state]
    )

if __name__ == "__main__":
    demo.launch(server_port=5004)
