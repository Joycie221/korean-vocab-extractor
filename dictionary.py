import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_ROOT / "data" / "dictionary.db"

POS_MAPPING = {
    "Noun": "명사",
    "Proper Noun": "명사",
    "Pronoun": "대명사",
    "Verb": "동사",
    "Adjective": "형용사",
    "Adverb": "부사",
}

def lookup_dictionary(word, part_of_speech=None):
    """Return dictionary entries matching a Korean headword and optional POS."""

    if not DATABASE_PATH.exists():
        return []

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        query = """
            SELECT
                headword,
                homonym_number,
                part_of_speech,
                korean_definition,
                english_word,
                english_definition
            FROM dictionary_entries
            WHERE headword = ?
        """

        parameters = [word]

        if part_of_speech:
            nikl_pos = POS_MAPPING.get(part_of_speech)

            if nikl_pos:
                query += " AND part_of_speech = ?"
                parameters.append(nikl_pos)

        query += " ORDER BY homonym_number, id"

        cursor = connection.execute(
            query,
            parameters
        )

        rows = cursor.fetchall()

        return [
            {
                "headword": row["headword"],
                "homonym_number": row["homonym_number"],
                "part_of_speech": row["part_of_speech"],
                "korean_definition": row["korean_definition"],
                "english_word": row["english_word"],
                "english_definition": row["english_definition"],
            }
            for row in rows
        ]

    finally:
        connection.close()

def select_primary_definition(entries):
    """Choose the most useful primary definition from dictionary entries."""

    if not entries:
        return None

    # Prefer entries without a numbered homonym distinction.
    default_entries = [
        entry
        for entry in entries
        if entry["homonym_number"] == 0
    ]

    if default_entries:
        return default_entries[0]

    # Otherwise, prefer the homonym that has the most senses.
    homonym_counts = {}

    for entry in entries:
        homonym_number = entry["homonym_number"]

        homonym_counts[homonym_number] = (
            homonym_counts.get(homonym_number, 0) + 1
        )

    preferred_homonym = max(
        homonym_counts,
        key=homonym_counts.get
    )

    return next(
        entry
        for entry in entries
        if entry["homonym_number"] == preferred_homonym
    )