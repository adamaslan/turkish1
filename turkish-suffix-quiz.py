import gradio as gr

suffix_examples = {
    "Plural": ("kitap", "kitaplar"),
    "Past Tense": ("git", "gitti"),
    "Future": ("yaz", "yazacak"),
}

def quiz_suffix(root, answer, suffix_type):
    correct = suffix_examples.get(suffix_type, ("", ""))[1]
    return "Correct!" if answer == correct else f"Try again. Correct answer: {correct}"

gr.Interface(
    fn=quiz_suffix,
    inputs=[
        gr.Textbox(label="Root word (e.g., 'kitap')"),
        gr.Textbox(label="Your answer (e.g., 'kitaplar')"),
        gr.Dropdown(choices=["Plural", "Past Tense", "Future"], label="Suffix Type")
    ],
    outputs="text"
).launch()