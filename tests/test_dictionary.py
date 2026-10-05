from dictionary import lookup_dictionary


def test_dictionary_finds_hada_adjective():
    entries = lookup_dictionary("우람하다")

    assert len(entries) >= 1
    assert entries[0]["headword"] == "우람하다"
    assert entries[0]["part_of_speech"] == "형용사"
    assert entries[0]["english_word"] == "bulky; brawny"


def test_dictionary_finds_derived_verb():
    entries = lookup_dictionary("상속되다")

    assert len(entries) >= 1
    assert entries[0]["headword"] == "상속되다"
    assert entries[0]["part_of_speech"] == "동사"
    assert entries[0]["english_word"] == "be inherited; be succeeded"


def test_dictionary_supports_multiple_senses():
    entries = lookup_dictionary("먹다")

    assert len(entries) > 1

    english_words = [
        entry["english_word"]
        for entry in entries
    ]

    assert "eat; have; consume; take" in english_words


def test_dictionary_returns_empty_list_for_unknown_word():
    entries = lookup_dictionary(
        "이단어는사전에절대로없을것이다"
    )

    assert entries == []

def test_dictionary_filters_by_part_of_speech():
    entries = lookup_dictionary(
        "먹다",
        "Verb"
    )

    assert len(entries) >= 1

    assert all(
        entry["part_of_speech"] == "동사"
        for entry in entries
    )