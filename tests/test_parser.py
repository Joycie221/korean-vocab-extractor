from app import extract_vocabulary


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
    from app import extract_vocabulary_with_context

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
    from app import extract_vocabulary_with_context

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