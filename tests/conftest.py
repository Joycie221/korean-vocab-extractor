import sqlite3

import pytest

import dictionary


@pytest.fixture(autouse=True)
def test_dictionary_database(tmp_path, monkeypatch):
    """Create a small temporary dictionary database for each test."""

    database_path = tmp_path / "dictionary.db"

    connection = sqlite3.connect(database_path)

    connection.execute(
        """
        CREATE TABLE dictionary_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headword TEXT NOT NULL,
            homonym_number INTEGER,
            part_of_speech TEXT,
            korean_definition TEXT,
            english_word TEXT,
            english_definition TEXT
        )
        """
    )

    test_entries = [
        (
            "우람하다",
            0,
            "형용사",
            "체격이나 크기가 크고 튼튼하다.",
            "bulky; brawny",
            "Having a large build or size and strength.",
        ),
        (
            "우람하다",
            0,
            "형용사",
            "소리 등이 매우 크고 힘차다.",
            "loud and strong",
            "A sound, etc., being loud and powerful.",
        ),
        (
            "상속되다",
            0,
            "동사",
            "사람이 죽은 후에 재산 등이 다른 사람에게 넘겨지다.",
            "be inherited; be succeeded",
            "For someone's property to be given or taken over after his/her death.",
        ),
        (
            "먹다",
            1,
            "동사",
            "귀가 잘 들리지 않게 되다.",
            "be deaf",
            "To become unable to hear well.",
        ),
        (
            "먹다",
            2,
            "동사",
            "음식을 입에 넣어 삼키다.",
            "eat; have; consume; take",
            "To put food into one's mouth and take it in one's stomach.",
        ),
        (
            "먹다",
            2,
            "동사",
            "물을 마시다.",
            "drink",
            "To drink something.",
        ),
        (
            "먹다",
            2,
            "동사",
            "어떤 마음이나 감정을 품다.",
            "have; bear",
            "To have a certain thought or feeling.",
        ),
    ]

    connection.executemany(
        """
        INSERT INTO dictionary_entries (
            headword,
            homonym_number,
            part_of_speech,
            korean_definition,
            english_word,
            english_definition
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        test_entries,
    )

    connection.commit()
    connection.close()

    monkeypatch.setattr(
        dictionary,
        "DATABASE_PATH",
        database_path,
    )