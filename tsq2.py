import gradio as gr
import random

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


def get_new_question(suffix_type):
    examples = suffix_examples.get(suffix_type, [])
    if examples:
        example = random.choice(examples)
        return {
            root_word: example[0],
            correct_answer: example[1],
            explanation: example[2],
            result: ""
        }
    return {
        root_word: "",
        correct_answer: "",
        explanation: "",
        result: "Please select a valid suffix type"
    }

def check_answer(user_input, correct, explanation):
    user_input = user_input.strip()
    if user_input == correct:
        return "Correct! 🎉", explanation
    else:
        return f"Incorrect ❌. Correct answer: {correct}", explanation

with gr.Blocks(title="Turkish Suffix Quiz", theme="soft") as demo:
    gr.Markdown("# 🇹🇷 Turkish Suffix Quiz")
    gr.Markdown("Practice Turkish suffixation rules for plurals, past tense, and future forms.")
    
    with gr.Row():
        suffix_type = gr.Dropdown(
            choices=["Plural", "Past Tense", "Future"],
            label="Select Suffix Type",
            value="Plural"
        )
        new_btn = gr.Button("New Question 🔄")
    
    root_word = gr.Textbox(label="Root Word", interactive=False)
    user_answer = gr.Textbox(label="Your Answer", placeholder="Type the suffixed form here...")
    submit_btn = gr.Button("Submit Answer ✅")
    
    with gr.Row():
        result = gr.Textbox(label="Result", interactive=False)
        explanation = gr.Textbox(label="Explanation", interactive=False)
    
    correct_answer = gr.State()
    
    suffix_type.change(
        get_new_question,
        inputs=[suffix_type],
        outputs=[root_word, correct_answer, explanation, result]
    )
    
    new_btn.click(
        get_new_question,
        inputs=[suffix_type],
        outputs=[root_word, correct_answer, explanation, result]
    )
    
    submit_btn.click(
        check_answer,
        inputs=[user_answer, correct_answer, explanation],
        outputs=[result, explanation]
    )
    
    user_answer.submit(
        check_answer,
        inputs=[user_answer, correct_answer, explanation],
        outputs=[result, explanation]
    )

demo.launch()