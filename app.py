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
    """Extract vocabulary tokens from Korean text and count their frequency."""

    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    frequencies = Counter(words)

    return frequencies


sample_text = """
안녕하세요! 요즘 한국어를 열심히 공부하고 있어요.
한국 드라마가 정말 재미있어요.
드라마를 보면서 단어를 공부해요.
"""

results = extract_vocabulary(sample_text)

for word, count in results.items():
    print(f"{word}: {count}")