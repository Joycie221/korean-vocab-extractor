from dictionary import lookup_dictionary
from collections import Counter
from flask import Flask, render_template, request
from kiwipiepy import Kiwi

app = Flask(__name__)

kiwi = Kiwi()


VOCABULARY_TAGS = {
    "NNG",  # General noun
    "NNP",  # Proper noun
    "NP",   # Pronoun
    "VV",   # Verb
    "VA",   # Adjective
    "MAG",  # General adverb
}


def to_dictionary_form(form, tag):
    """Convert verb and adjective stems to a basic dictionary-style form."""

    if tag in {"VV", "VA"}:
        return form + "다"

    return form

POS_LABELS = {
    "NNG": "Noun",
    "NNP": "Proper Noun",
    "NP": "Pronoun",
    "VV": "Verb",
    "VA": "Adjective",
    "MAG": "Adverb",
}

def reconstruct_derived_word(tokens, index):
    """Reconstruct Korean words formed with derivational suffixes."""

    token = tokens[index]

    if index + 1 >= len(tokens):
        return None

    next_token = tokens[index + 1]

    # Noun + verbal derivational suffix
    # 공부 + 하 -> 공부하다
    # 상속 + 되 -> 상속되다
    if token.tag == "NNG" and next_token.tag == "XSV":
        return {
            "word": token.form + next_token.form + "다",
            "part_of_speech": "Verb",
        }

    # Root + adjectival derivational suffix
    # 우람 + 하 -> 우람하다
    if token.tag == "XR" and next_token.tag == "XSA":
        return {
            "word": token.form + next_token.form + "다",
            "part_of_speech": "Adjective",
        }

    return None


def extract_vocabulary(text):
    """Analyze Korean text and count vocabulary-bearing morphemes."""

    tokens = kiwi.tokenize(text)
    vocabulary = []
    index = 0

    while index < len(tokens):
        token = tokens[index]

        # Reconstruct words formed with derivational suffixes.
        # Examples:
        # 공부 + 하/XSV -> 공부하다 (Verb)
        # 상속 + 되/XSV -> 상속되다 (Verb)
        # 우람 + 하/XSA -> 우람하다 (Adjective)
        derived_word = reconstruct_derived_word(tokens, index)

        if derived_word:
            vocabulary.append(
                (
                    derived_word["word"],
                    derived_word["part_of_speech"],
                )
            )

            # Skip the root and derivational suffix because
            # they have already been combined into one word.
            index += 2
            continue

        # Handle ordinary vocabulary tokens.
        if token.tag in VOCABULARY_TAGS:
            word = to_dictionary_form(token.form, token.tag)
            part_of_speech = POS_LABELS[token.tag]

            vocabulary.append(
                (
                    word,
                    part_of_speech,
                )
            )

        index += 1

    frequencies = Counter(vocabulary)

    return frequencies.most_common()

def get_surface_form(sentence_text, token):
    """Return the original whitespace-delimited form containing a token."""

    start = token.start
    end = start

    while start > 0 and not sentence_text[start - 1].isspace():
        start -= 1

    while end < len(sentence_text) and not sentence_text[end].isspace():
        end += 1

    surface_form = sentence_text[start:end]

    return surface_form.rstrip(".,!?…“”‘’")

def extract_vocabulary_with_context(text):
    """Extract vocabulary with original forms, sentence context, and definitions."""

    results = {}

    sentences = kiwi.split_into_sents(text)

    for sentence in sentences:
        sentence_text = sentence.text
        tokens = kiwi.tokenize(sentence_text)

        index = 0

        while index < len(tokens):
            token = tokens[index]

            derived_word = reconstruct_derived_word(tokens, index)

            if derived_word:
                word = derived_word["word"]
                part_of_speech = derived_word["part_of_speech"]

                surface_form = get_surface_form(
                    sentence_text,
                    token
                )

                if word not in results:
                    results[word] = {
                        "word": word,
                        "part_of_speech": part_of_speech,
                        "frequency": 0,
                        "occurrences": [],
                        "definitions": lookup_dictionary(
                            word,
                            part_of_speech
                        ),
                    }

                results[word]["frequency"] += 1

                results[word]["occurrences"].append({
                    "surface_form": surface_form,
                    "sentence": sentence_text,
                })

                index += 2
                continue

            if token.tag in VOCABULARY_TAGS:
                word = to_dictionary_form(
                    token.form,
                    token.tag
                )

                part_of_speech = POS_LABELS[token.tag]

                surface_form = get_surface_form(
                    sentence_text,
                    token
                )

                if word not in results:
                    results[word] = {
                        "word": word,
                        "part_of_speech": part_of_speech,
                        "frequency": 0,
                        "occurrences": [],
                        "definitions": lookup_dictionary(
                            word,
                            part_of_speech
                        ),
                    }

                results[word]["frequency"] += 1

                results[word]["occurrences"].append({
                    "surface_form": surface_form,
                    "sentence": sentence_text,
                })

            index += 1

    return sorted(
        results.values(),
        key=lambda item: item["frequency"],
        reverse=True
    )

def calculate_statistics(vocab_list):
    """Calculate summary statistics for extracted vocabulary."""

    total_unique = len(vocab_list)

    total_occurrences = sum(
        item["frequency"]
        for item in vocab_list
    )

    parts_of_speech = Counter(
        item["part_of_speech"]
        for item in vocab_list
    )

    return {
        "unique_words": total_unique,
        "total_occurrences": total_occurrences,
        "parts_of_speech": dict(parts_of_speech),
    }

@app.route("/", methods=["GET", "POST"])
def index():
    vocab_list = []
    statistics = None
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("korean_text", "")

        if user_input.strip():
            vocab_list = extract_vocabulary_with_context(user_input)
            statistics = calculate_statistics(vocab_list)

    return render_template(
        "index.html",
        vocab_list=vocab_list,
        statistics=statistics,
        user_input=user_input,
    )

if __name__ == "__main__":
    app.run(debug=True)