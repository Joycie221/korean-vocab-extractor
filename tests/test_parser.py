from app import (
    extract_vocabulary,
    extract_vocabulary_with_context,
    calculate_statistics,
)


def vocabulary_as_dict(text):
    """Convert extractor results to a dictionary keyed by vocabulary word."""

    return {
        word: {
            "part_of_speech": part_of_speech,
            "frequency": count,
        }
        for (word, part_of_speech), count in extract_vocabulary(text)
    }


def test_removes_subject_particle():
    results = vocabulary_as_dict("친구가 왔어요.")

    assert "친구" in results
    assert "친구가" not in results


def test_combines_noun_forms():
    results = vocabulary_as_dict("친구가 친구를 만났어요.")

    assert results["친구"]["frequency"] == 2


def test_converts_verb_to_dictionary_form():
    results = vocabulary_as_dict("밥을 먹었어요.")

    assert "먹다" in results
    assert "먹었어요" not in results


def test_excludes_punctuation():
    results = vocabulary_as_dict("학교에 갔어요!")

    assert "!" not in results


def test_extracts_adverb():
    results = vocabulary_as_dict("한국어를 열심히 공부해요.")

    assert "열심히" in results


def test_reconstructs_hada_verb():
    examples = [
        "한국어를 공부해요.",
        "어제 한국어를 공부했어요.",
        "매일 한국어를 공부하고 있어요.",
        "한국어를 공부한다.",
    ]

    for text in examples:
        results = vocabulary_as_dict(text)

        assert "공부하다" in results
        assert "공부" not in results


def test_counts_hada_forms_together():
    results = vocabulary_as_dict(
        "저는 한국어를 공부해요. "
        "어제도 공부했어요. "
        "오늘도 공부하고 있어요."
    )

    assert results["공부하다"]["frequency"] == 3


def test_assigns_part_of_speech():
    results = vocabulary_as_dict(
        "친구가 밥을 먹었어요. 한국어를 열심히 공부해요."
    )

    assert results["친구"]["part_of_speech"] == "Noun"
    assert results["먹다"]["part_of_speech"] == "Verb"
    assert results["열심히"]["part_of_speech"] == "Adverb"
    assert results["공부하다"]["part_of_speech"] == "Verb"


def test_tracks_sentence_context():
    results = extract_vocabulary_with_context(
        "저는 한국어를 공부해요. "
        "어제도 공부했어요. "
        "오늘도 공부하고 있어요."
    )

    study = next(
        item for item in results
        if item["word"] == "공부하다"
    )

    assert study["frequency"] == 3
    assert len(study["occurrences"]) == 3

    assert study["occurrences"][0]["sentence"] == \
        "저는 한국어를 공부해요."

    assert study["occurrences"][1]["sentence"] == \
        "어제도 공부했어요."

    assert study["occurrences"][2]["sentence"] == \
        "오늘도 공부하고 있어요."


def test_tracks_original_surface_forms():
    results = extract_vocabulary_with_context(
        "저는 한국어를 공부해요. "
        "어제도 공부했어요. "
        "오늘도 공부하고 있어요."
    )

    study = next(
        item for item in results
        if item["word"] == "공부하다"
    )

    surface_forms = [
        occurrence["surface_form"]
        for occurrence in study["occurrences"]
    ]

    assert surface_forms == [
        "공부해요",
        "공부했어요",
        "공부하고",
    ]


def test_calculates_vocabulary_statistics():
    vocab_list = extract_vocabulary_with_context(
        "저는 한국어를 공부해요. "
        "어제도 공부했어요. "
        "오늘도 공부하고 있어요."
    )

    statistics = calculate_statistics(vocab_list)

    assert statistics["unique_words"] == 5
    assert statistics["total_occurrences"] == 7

    assert statistics["parts_of_speech"]["Verb"] == 1
    assert statistics["parts_of_speech"]["Pronoun"] == 1
    assert statistics["parts_of_speech"]["Proper Noun"] == 1
    assert statistics["parts_of_speech"]["Noun"] == 2

def test_reconstructs_doeda_verb():
    results = vocabulary_as_dict(
        "재산이 남편에게 상속될 예정이었다."
    )

    assert "상속되다" in results
    assert "상속" not in results
    assert results["상속되다"]["part_of_speech"] == "Verb"


def test_reconstructs_hada_adjective():
    results = vocabulary_as_dict(
        "어깨가 우람했다."
    )

    assert "우람하다" in results
    assert "우람" not in results
    assert results["우람하다"]["part_of_speech"] == "Adjective"

def test_attaches_dictionary_definitions():
    results = extract_vocabulary_with_context(
        "어깨가 우람했다."
    )

    study_word = next(
        item for item in results
        if item["word"] == "우람하다"
    )

    definitions = study_word["definitions"]

    assert len(definitions) >= 1
    assert definitions[0]["english_word"] == "bulky; brawny"
    assert (
        definitions[0]["english_definition"]
        == "Having a large build or size and strength."
    )

def test_attaches_primary_dictionary_definition():
    results = extract_vocabulary_with_context(
        "밥을 먹었어요."
    )

    eat = next(
        item for item in results
        if item["word"] == "먹다"
    )

    assert eat["primary_definition"] is not None
    assert (
        eat["primary_definition"]["english_word"]
        == "eat; have; consume; take"
    )