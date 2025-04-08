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
        ("bul", "bulacak", "Regular future form with -acak (Corrected: bul needs -acak)", "encontrará"), # Corrected based on vowel harmony
        ("iç", "içecek", "Future form with -ecek for front vowels", "beberá"), # Corrected: ç doesn't transform here
    ],
    "Present Continuous": [
        ("yaz", "yazıyor", "Regular present continuous form with -ıyor", "está escribiendo"),
        ("oku", "okuyor", "Regular present continuous form with -uyor", "está leyendo"),
        ("gel", "geliyor", "Regular present continuous form with -iyor", "está viniendo"),
        ("düşün", "düşünüyor", "ü → ünüyor transformation", "está pensando"),
        ("anla", "anlıyor", "a → ıyor transformation", "está entendiendo"),
        ("bul", "buluyor", "Regular present continuous form with -uyor", "está encontrando"),
        ("iç", "içiyor", "Regular present continuous form with -iyor", "está bebiendo"),
        # Added missing example for variety
        ("yap", "yapıyor", "Regular present continuous form with -ıyor", "está haciendo"),
    ],
    "Conditional": [
        ("yaz", "yazsa", "Regular conditional form with -sa (back vowel)", "si escribe"),
        ("oku", "okusa", "Regular conditional form with -sa (back vowel)", "si lee"),
        ("gel", "gelse", "Regular conditional form with -se (front vowel)", "si viene"),
        ("düşün", "düşünse", "Regular conditional form with -se (front vowel)", "si piensa"),
        ("anla", "anlasa", "Regular conditional form with -sa (back vowel)", "si entiende"), # Corrected based on vowel harmony
        ("bul", "bulsa", "Regular conditional form with -sa (back vowel)", "si encuentra"),
        ("iç", "içse", "Regular conditional form with -se (front vowel)", "si bebe"),
        # Added missing example for variety
        ("git", "gitse", "Regular conditional form with -se (front vowel)", "si va"),
    ],
    "Locative": [
        ("ev", "evde", "Locative case with -de (after voiced consonants, front vowel)", "en casa"),
        ("okul", "okulda", "Locative case with -da (after voiced consonants, back vowel)", "en la escuela"),
        ("masa", "masada", "Locative case with -da (after vowels, back vowel)", "en la mesa"),
        ("bahçe", "bahçede", "Locative case with -de (after vowels, front vowel)", "en el jardín"),
        ("sokak", "sokakta", "Locative case with -ta (after voiceless consonants [k], back vowel)", "en la calle"),
        ("oda", "odada", "Locative case with -da (after vowels, back vowel)", "en la habitación"),
        ("park", "parkta", "Locative case with -ta (after voiceless consonants [k], back vowel)", "en el parque"),
         # Added missing example for variety
        ("kitap", "kitapta", "Locative case with -ta (after voiceless consonants [p], back vowel)", "en el libro"),
    ],
    "Possessive (My)": [ # Renamed for clarity, as all examples are 1st person singular
        ("kitap", "kitabım", "Possessive form 'my' with -ım (after consonant, back vowel harmony)", "mi libro"),
        ("araba", "arabam", "Possessive form 'my' with -m (after vowel, back vowel harmony)", "mi coche"),
        ("ev", "evim", "Possessive form 'my' with -im (after consonant, front vowel harmony)", "mi casa"),
        ("kalem", "kalemim", "Possessive form 'my' with -im (after consonant, front vowel harmony)", "mi lápiz"),
        ("çanta", "çantam", "Possessive form 'my' with -m (after vowel, back vowel harmony)", "mi bolso"),
        ("telefon", "telefonum", "Possessive form 'my' with -um (after consonant, back rounded vowel harmony)", "mi teléfono"),
        ("bilgisayar", "bilgisayarım", "Possessive form 'my' with -ım (after consonant, back vowel harmony)", "mi computadora"),
        # Added missing example for variety
        ("göz", "gözüm", "Possessive form 'my' with -üm (after consonant, front rounded vowel harmony)", "mi ojo"),
    ],
}

def run_quiz(examples_dict):
    """Runs a quiz based on the provided dictionary of suffix examples."""
    score = 0
    all_questions = []

    # Prepare all questions from all categories
    for category, items in examples_dict.items():
        for base_word, correct_suffixed, explanation, _ in items: # Ignore spanish translation for the quiz logic
            # Add the question data as a tuple
            all_questions.append((category, base_word, correct_suffixed, explanation))

    # Shuffle all questions together for a mixed quiz
    random.shuffle(all_questions)

    total_questions = len(all_questions)

    print("--- Turkish Suffix Quiz ---")
    print(f"Let's test your knowledge on {len(examples_dict)} types of suffixes.")
    print("Enter the correct suffixed form for each word and category.")
    print("Type 'hint' for the rule, or 'quit' to exit.\n")

    question_number = 0
    for category, base_word, correct_suffixed, explanation in all_questions:
        question_number += 1
        attempts = 0
        while attempts < 2: # Allow one hint request
            prompt = f"Q{question_number}/{total_questions} ({category}): '{base_word}' -> ? "
            user_answer = input(prompt).strip() # Get input and remove leading/trailing spaces

            if user_answer.lower() == 'quit':
                print("\nExiting quiz.")
                return score, question_number -1 # Return current score and number answered

            if user_answer.lower() == 'hint':
                if attempts == 0:
                    print(f"   Hint: {explanation}")
                    attempts += 1 # Use up the hint attempt
                    continue # Ask the same question again
                else:
                    print("   You already used your hint for this question.")
                    continue # Ask again without counting as a new attempt

            # Compare answers (case-insensitive for user input flexibility, but exact case for correct answer)
            if user_answer.lower() == correct_suffixed.lower():
                 # Accept if lowercase matches, helpful for users forgetting Turkish i/İ distinction sometimes
                print(f"Correct! It's '{correct_suffixed}'.")
                score += 1
                break # Move to the next question
            else:
                print(f"Incorrect.")
                # On the final attempt (or if no hint was used)
                if attempts == 0: # Give feedback immediately if no hint was requested
                     print(f"   The correct answer is: {correct_suffixed}")
                     print(f"   Rule was: {explanation}")
                     break # Move to next question after incorrect guess without hint
                # If hint was used and still wrong
                elif attempts == 1:
                    print(f"   The correct answer is: {correct_suffixed}")
                    break # Move to next question after hint + incorrect guess


            print("-" * 15) # Separator between questions

    print("\n--- Quiz Finished ---")
    print(f"Your final score: {score} out of {question_number} questions attempted.")
    if question_number > 0:
        percentage = (score / question_number) * 100
        print(f"Percentage: {percentage:.2f}%")
    else:
        print("No questions were attempted.")

# --- Run the Quiz ---
if __name__ == "__main__":
    # Small corrections/additions were made to the original data for accuracy/variety
    # You can modify the suffix_examples dictionary above as needed.
    final_score, questions_done = run_quiz(suffix_examples)
    print("\nQuiz session ended.")