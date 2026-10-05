from app import extract_vocabulary


def vocabulary_as_dict(text):
    """Convert extractor results to a dictionary for easier testing."""
    return dict(extract_vocabulary(text))


def test_removes_subject_particle():
    results = vocabulary_as_dict("친구가 왔어요.")

    assert "친구" in results
    assert "친구가" not in results


def test_combines_noun_forms():
    results = vocabulary_as_dict("친구가 친구를 만났어요.")

    assert results["친구"] == 2


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

    assert results["공부하다"] == 3