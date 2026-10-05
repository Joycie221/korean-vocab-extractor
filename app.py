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


def extract_vocabulary(text):
    """Analyze Korean text and count vocabulary-bearing morphemes."""

    tokens = kiwi.tokenize(text)

    vocabulary = []
    index = 0

    while index < len(tokens):
        token = tokens[index]

        # Reconstruct 하다 verbs such as 공부하다:
        # 공부/NNG + 하/XSV -> 공부하다
        if (
            token.tag == "NNG"
            and index + 1 < len(tokens)
            and tokens[index + 1].tag == "XSV"
            and tokens[index + 1].form == "하"
        ):
            vocabulary.append((token.form + "하다", "Verb"))
            index += 2
            continue

        if token.tag in VOCABULARY_TAGS:
            word = to_dictionary_form(token.form, token.tag)
            pos = POS_LABELS[token.tag]
            
            vocabulary.append((word, pos))

        index += 1

    frequencies = Counter(vocabulary)

    return frequencies.most_common()

@app.route("/", methods=["GET", "POST"])
def index():
    vocab_list = []
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("korean_text", "")

        if user_input.strip():
            vocab_list = extract_vocabulary(user_input)

    return render_template(
        "index.html",
        vocab_list=vocab_list,
        user_input=user_input
    )

if __name__ == "__main__":
    app.run(debug=True)