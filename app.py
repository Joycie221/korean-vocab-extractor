import string
from collections import Counter


def clean_text(text):
    """Remove punctuation from Korean text before tokenization."""

    punctuation = string.punctuation + "…“”‘’"

    cleaned_text = "".join(
        character for character in text
        if character not in punctuation
    )

    return cleaned_text


def extract_vocabulary(text):
    """Extract vocabulary tokens and rank them by frequency."""

    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    frequencies = Counter(words)

    return frequencies.most_common()


sample_text = """
이즈쿠는 영웅이다.
이즈쿠는 학생이다.
나는 이즈쿠를 좋아한다.
카츠키는 이즈쿠를 본다.
이즈쿠는 좋은 영웅이다.
"""

results = extract_vocabulary(sample_text)

for word, count in results:
    print(f"{word}: {count}")