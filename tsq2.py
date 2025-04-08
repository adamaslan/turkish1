import gradio as gr
import random

suffix_examples = {
    "Plural": [
        ("kitap", "kitaplar", "After back vowels (a, ı, o, u) use '-lar'", "libros"),
        ("defter", "defterler", "After front vowels (e, i, ö, ü) use '-ler'", "cuadernos"),
        ("kalem", "kalemler", "After front vowels (e, i, ö, ü) use '-ler'", "lápices"),
        ("araba", "arabalar", "After back vowels (a, ı, o, u) use '-lar'", "coches"),
        ("ev", "evler", "After front vowels (e, i, ö, ü) use '-ler'", "casas"),
        ("çiçek", "çiçekler", "After front vowels (e, i, ö, ü) use '-ler'", "flores"),
        ("masa", "masalar", "After back vowels (a, ı, o, u) use '-lar'", "mesas"),
        ("kız", "kızlar", "After back vowels (a, ı, o, u) use '-lar'", "chicas"),
    ],
    "Past Tense": [
        ("git", "gitti", "Double consonant after short vowels (i)", "fue"),
        ("gel", "geldi", "Regular past tense formation", "vino"),
        ("oku", "okudu", "u → udu transformation for back vowels", "leyó"),
        ("yaz", "yazdı", "z → zd transformation", "escribió"),
        ("düşün", "düşündü", "n → nd transformation", "pensó"),
        ("anla", "anladı", "a → ad transformation", "entendió"),
        ("bul", "buldu", "Regular past tense formation", "encontró"),
        ("iç", "içti", "ç → çti transformation", "bebió"),
    ],
    "Future": [
        ("yaz", "yazacak", "Regular future form with -acak", "escribirá"),
        ("oku", "okuyacak", "u becomes uy before vowel (y buffer)", "leerá"),
        ("başla", "başlayacak", "Consonant mutation l → y before vowel", "empezará"),
        ("gel", "gelecek", "Future form with -ecek for front vowels", "vendrá"),
        ("düşün", "düşünecek", "ü → ünecek transformation", "pensará"),
        ("anla", "anlayacak", "a → aya before vowel", "entenderá"),
        ("bul", "bulecek", "Regular future form with -ecek", "encontrará"),
        ("iç", "içecek", "ç → çecek transformation", "beberá"),
    ],
    "Present Continuous": [
        ("yaz", "yazıyor", "Regular present continuous form with -ıyor", "está escribiendo"),
        ("oku", "okuyor", "Regular present continuous form with -uyor", "está leyendo"),
        ("gel", "geliyor", "Regular present continuous form with -iyor", "está viniendo"),
        ("düşün", "düşünüyor", "ü → ünüyor transformation", "está pensando"),
        ("anla", "anlıyor", "a → ıyor transformation", "está entendiendo"),
        ("bul", "buluyor", "Regular present continuous form with -uyor", "está encontrando"),
        ("iç", "içiyor", "Regular present continuous form with -iyor", "está bebiendo"),
    ],
    "Conditional": [
        ("yaz", "yazsa", "Regular conditional form with -sa", "si escribe"),
        ("oku", "okusa", "Regular conditional form with -sa", "si lee"),
        ("gel", "gelse", "Regular conditional form with -se", "si viene"),
        ("düşün", "düşünse", "Regular conditional form with -se", "si piensa"),
        ("anla", "anlarsa", "Regular conditional form with -sa", "si entiende"),
        ("bul", "bulsa", "Regular conditional form with -sa", "si encuentra"),
        ("iç", "içse", "Regular conditional form with -se", "si bebe"),
    ],
    "Locative": [
        ("ev", "evde", "Locative case with -de", "en casa"),
        ("okul", "okulda", "Locative case with -da", "en la escuela"),
        ("masa", "masada", "Locative case with -da", "en la mesa"),
        ("bahçe", "bahçede", "Locative case with -de", "en el jardín"),
        ("sokak", "sokakta", "Locative case with -ta", "en la calle"),
        ("oda", "odada", "Locative case with -da", "en la habitación"),
        ("park", "parkta", "Locative case with -ta", "en el parque"),
    ],
    "Possessive": [
        ("kitap", "kitabım", "Possessive form with -ım", "mi libro"),
        ("araba", "arabam", "Possessive form with -m", "mi coche"),
        ("ev", "evim", "Possessive form with -im", "mi casa"),
        ("kalem", "kalemim", "Possessive form with -im", "mi lápiz"),
        ("çanta", "çantam", "Possessive form with -m", "mi bolso"),
        ("telefon", "telefonum", "Possessive form with -um", "mi teléfono"),
        ("bilgisayar", "bilgisayarım", "Possessive form with -ım", "mi computadora"),
    ],
}

def get_new_question(suffix_type):
    examples = suffix_examples.get(suffix_type, [])
    if examples:
        example = random.choice(examples)
        return {
            "root_word": example[0],
            "spanish_translation": example[3],
            "correct_answer": example[1],
            "explanation": example[2],
            "result": ""
        }
    return {
        "root_word": "",
        "spanish_translation": "",
        "correct_answer": "",
        "explanation": "",
        "result": "Please select a valid suffix type"
    }

def check_answer(user_input, correct, explanation):
    user_input = user_input.strip()
    if user_input == correct:
        return "Correct! 🎉", explanation
    else:
        return f"Incorrect ❌. Correct answer: {correct}", explanation

with gr.Blocks(title="Turkish Suffix Quiz", theme="soft") as demo:
    gr.Markdown("# 🇹🇷 Turkish Suffix Quiz")
    gr.Markdown("Practice Turkish suffixation rules with Spanish translations")
    
    with gr.Row():
        suffix_type = gr.Dropdown(
            choices=["Plural", "Past Tense", "Future", "Present Continuous", 
                    "Conditional", "Locative", "Possessive"],
            label="Select Suffix Type",
            value="Plural"
        )
        new_btn = gr.Button("New Question 🔄")
    
    with gr.Row():
        root_word = gr.Textbox(label="Root Word", interactive=False)
        spanish_translation = gr.Textbox(label="Spanish Translation", interactive=False)
    
    user_answer = gr.Textbox(label="Your Answer (Turkish)", placeholder="Type the suffixed form here...")
    submit_btn = gr.Button("Submit Answer ✅")
    
    with gr.Row():
        result = gr.Textbox(label="Result", interactive=False)
        explanation = gr.Textbox(label="Explanation", interactive=False)
    
    correct_answer = gr.State()
    
    suffix_type.change(
        get_new_question,
        inputs=[suffix_type],
        outputs=[root_word, spanish_translation, correct_answer, explanation, result]
    )
    
    new_btn.click(
        get_new_question,
        inputs=[suffix_type],
        outputs=[root_word, spanish_translation, correct_answer, explanation, result]
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