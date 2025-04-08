import gradio as gr
import random
from datetime import datetime

suffix_examples = {
    "Plural": [
        ("kitap", "kitaplar", "After back vowels (a, ı, o, u) use '-lar'"),
        ("defter", "defterler", "After front vowels (e, i, ö, ü) use '-ler'"),
        ("kalem", "kalemler", "After front vowels (e, i, ö, ü) use '-ler'"),
        ("araba", "arabalar", "After back vowels (a, ı, o, u) use '-lar'"),
        ("ev", "evler", "After front vowels (e, i, ö, ü) use '-ler'"),
        ("çiçek", "çiçekler", "After front vowels (e, i, ö, ü) use '-ler'"),
        ("masa", "masalar", "After back vowels (a, ı, o, u) use '-lar'"),
        ("kız", "kızlar", "After back vowels (a, ı, o, u) use '-lar'"),
    ],
    "Past Tense": [
        ("git", "gitti", "Double consonant after short vowels (i)"),
        ("gel", "geldi", "Regular past tense formation"),
        ("oku", "okudu", "u → udu transformation for back vowels"),
        ("yaz", "yazdı", "z → zd transformation"),
        ("düşün", "düşündü", "n → nd transformation"),
        ("anla", "anladı", "a → ad transformation"),
        ("bul", "buldu", "Regular past tense formation"),
        ("iç", "içti", "ç → çti transformation"),
    ],
    "Future": [
        ("yaz", "yazacak", "Regular future form with -acak"),
        ("oku", "okuyacak", "u becomes uy before vowel (y buffer)"),
        ("başla", "başlayacak", "Consonant mutation l → y before vowel"),
        ("gel", "gelecek", "Future form with -ecek for front vowels"),
        ("düşün", "düşünecek", "ü → ünecek transformation"),
        ("anla", "anlayacak", "a → aya before vowel"),
        ("bul", "bulecek", "Regular future form with -ecek"),
        ("iç", "içecek", "ç → çecek transformation"),
    ],
    "Present Continuous": [
        ("yaz", "yazıyor", "Regular present continuous form with -ıyor"),
        ("oku", "okuyor", "Regular present continuous form with -uyor"),
        ("gel", "geliyor", "Regular present continuous form with -iyor"),
        ("düşün", "düşünüyor", "ü → ünüyor transformation"),
        ("anla", "anlıyor", "a → ıyor transformation"),
        ("bul", "buluyor", "Regular present continuous form with -uyor"),
        ("iç", "içiyor", "Regular present continuous form with -iyor"),
    ],
    "Conditional": [
        ("yaz", "yazsa", "Regular conditional form with -sa"),
        ("oku", "okusa", "Regular conditional form with -sa"),
        ("gel", "gelse", "Regular conditional form with -se"),
        ("düşün", "düşünse", "Regular conditional form with -se"),
        ("anla", "anlarsa", "Regular conditional form with -sa"),
        ("bul", "bulsa", "Regular conditional form with -sa"),
        ("iç", "içse", "Regular conditional form with -se"),
    ],
    "Locative": [
        ("ev", "evde", "Locative case with -de"),
        ("okul", "okulda", "Locative case with -da"),
        ("masa", "masada", "Locative case with -da"),
        ("bahçe", "bahçede", "Locative case with -de"),
        ("sokak", "sokakta", "Locative case with -ta"),
        ("oda", "odada", "Locative case with -da"),
        ("park", "parkta", "Locative case with -ta"),
    ],
    "Possessive": [
        ("kitap", "kitabım", "Possessive form with -ım"),
        ("araba", "arabam", "Possessive form with -m"),
        ("ev", "evim", "Possessive form with -im"),
        ("kalem", "kalemim", "Possessive form with -im"),
        ("çanta", "çantam", "Possessive form with -m"),
        ("telefon", "telefonum", "Possessive form with -um"),
        ("bilgisayar", "bilgisayarım", "Possessive form with -ım"),
    ],
}

class QuizState:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.streak = 0
        self.correct_count = 0
        self.total_attempts = 0
        self.start_time = datetime.now()
        self.question_history = []

quiz_state = QuizState()

def get_new_question(suffix_type):
    examples = suffix_examples.get(suffix_type, [])
    if not examples:
        return [gr.update(value="")] * 3 + [gr.update(value="⚠️ Invalid suffix type")] + [gr.update(visible=False), gr.update(value="")]
    
    example = random.choice(examples)
    quiz_state.question_history.append(example)
    return [
        gr.update(value=example[0]),  # root_word
        gr.update(value=example[1]),  # correct_answer
        gr.update(value=example[2]),  # explanation
        gr.update(value=""),          # result
        gr.update(visible=False),     # feedback_box
        gr.update(value="")           # user_answer
    ]

def check_answer(user_input, correct, explanation):
    user_input = user_input.strip()
    quiz_state.total_attempts += 1
    
    if user_input == correct:
        quiz_state.correct_count += 1
        quiz_state.streak += 1
        return [
            gr.Markdown.update(value="🎉 Correct! Well done!", visible=True),
            gr.Textbox.update(value=explanation),
            gr.update(value=f"📊 Correct: {quiz_state.correct_count} | Attempts: {quiz_state.total_attempts}"),
            gr.Column.update(visible=True, variant="success"),
            gr.Slider.update(visible=True)
        ]
    else:
        quiz_state.streak = 0
        return [
            gr.Markdown.update(value=f"❌ Incorrect. Correct: {correct}", visible=True),
            gr.Textbox.update(value=explanation),
            gr.update(value=f"📊 Correct: {quiz_state.correct_count} | Attempts: {quiz_state.total_attempts}"),
            gr.Column.update(visible=True, variant="danger"),
            gr.Slider.update(visible=True)
        ]

with gr.Blocks(title="Turkish Suffix Master", theme="soft") as demo:
    root_word = gr.Textbox(label="Root Word")
    correct_answer = gr.State()
    explanation = gr.Textbox(visible=False)
    result = gr.Markdown(visible=False)
    user_answer = gr.Textbox(label="Your Answer")
    feedback_box = gr.Column(visible=False)
    progress_bar = gr.Slider(visible=False)
    
    with gr.Row():
        suffix_type = gr.Dropdown(list(suffix_examples.keys()), label="Suffix Type", value="Plural")
        new_btn = gr.Button("New Question")
        stats_display = gr.Textbox(label="Stats")

    new_btn.click(
        get_new_question,
        inputs=[suffix_type],
        outputs=[root_word, correct_answer, explanation, result, feedback_box, user_answer]
    )
    
    user_answer.submit(
        check_answer,
        inputs=[user_answer, correct_answer, explanation],
        outputs=[result, explanation, stats_display, feedback_box, progress_bar]
    )

demo.launch()