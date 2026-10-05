from collections import Counter
from kiwipiepy import Kiwi


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


def extract_vocabulary(text):
    """Analyze Korean text and count vocabulary-bearing morphemes."""

    tokens = kiwi.tokenize(text)

    vocabulary = []

    for token in tokens:
        if token.tag in VOCABULARY_TAGS:
            word = to_dictionary_form(token.form, token.tag)
            vocabulary.append(word)

    frequencies = Counter(vocabulary)

    return frequencies.most_common()


if __name__ == "__main__":
    sample_text = """
    친구가 학교에서 밥을 먹었어요.
    저는 한국어를 열심히 공부하고 있어요.
    """

    results = extract_vocabulary(sample_text)

    for word, count in results:
        print(f"{word}: {count}")