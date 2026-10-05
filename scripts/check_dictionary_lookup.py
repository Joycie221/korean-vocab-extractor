import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "dictionary.db"

TEST_WORDS = [
    "먹다",
    "공부하다",
    "우람하다",
    "상속되다",
    "어울리다",
    "다산",
]


def lookup_word(connection, word):
    """Look up all dictionary entries for a Korean headword."""

    cursor = connection.execute(
        """
        SELECT
            headword,
            homonym_number,
            part_of_speech,
            korean_definition,
            english_word,
            english_definition
        FROM dictionary_entries
        WHERE headword = ?
        ORDER BY homonym_number, id
        """,
        (word,),
    )

    return cursor.fetchall()


def main():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        for word in TEST_WORDS:
            entries = lookup_word(connection, word)

            print("\n==============================")
            print(f"{word}: {len(entries)} entries")
            print("==============================")

            for entry in entries:
                (
                    headword,
                    homonym_number,
                    part_of_speech,
                    korean_definition,
                    english_word,
                    english_definition,
                ) = entry

                print(f"\nHeadword: {headword}")
                print(f"Homonym: {homonym_number}")
                print(f"POS: {part_of_speech}")
                print(f"English: {english_word}")
                print(f"Definition: {english_definition}")
                print(
                    f"Korean definition: "
                    f"{korean_definition}"
                )

    finally:
        connection.close()


if __name__ == "__main__":
    main()