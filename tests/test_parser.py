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