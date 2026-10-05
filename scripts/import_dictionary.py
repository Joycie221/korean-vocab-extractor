import sqlite3
from pathlib import Path

import xlrd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DATABASE_PATH = PROJECT_ROOT / "data" / "dictionary.db"

DICTIONARY_FILES = [
    RAW_DATA_DIR / "1_30000_20260919.xls",
    RAW_DATA_DIR / "2_30000_20260919.xls",
    RAW_DATA_DIR / "3_16833_20260919.xls",
]


def create_database():
    """Create a fresh SQLite database for NIKL dictionary data."""

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    connection = sqlite3.connect(DATABASE_PATH)

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

    connection.execute(
        """
        CREATE INDEX idx_dictionary_headword
        ON dictionary_entries (headword)
        """
    )

    return connection


def clean_text(value):
    """Convert spreadsheet values into clean strings or None."""

    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    return text


def import_dictionary_file(connection, file_path):
    """Import useful lexical entries from one NIKL spreadsheet."""

    workbook = xlrd.open_workbook(
        file_path,
        on_demand=True
    )

    sheet = workbook.sheet_by_index(0)
    headers = sheet.row_values(0)

    columns = {
        "headword": headers.index("표제어"),
        "homonym_number": headers.index("동형어 번호"),
        "part_of_speech": headers.index("품사"),
        "korean_definition": headers.index("뜻풀이"),
        "english_word": headers.index("영어 대역어"),
        "english_definition": headers.index(
            "영어 대역어 뜻풀이"
        ),
    }

    examined = 0
    imported = 0
    skipped = 0

    for row_index in range(1, sheet.nrows):
        examined += 1

        headword = clean_text(
            sheet.cell_value(
                row_index,
                columns["headword"]
            )
        )

        part_of_speech = clean_text(
            sheet.cell_value(
                row_index,
                columns["part_of_speech"]
            )
        )

        korean_definition = clean_text(
            sheet.cell_value(
                row_index,
                columns["korean_definition"]
            )
        )

        english_word = clean_text(
            sheet.cell_value(
                row_index,
                columns["english_word"]
            )
        )

        english_definition = clean_text(
            sheet.cell_value(
                row_index,
                columns["english_definition"]
            )
        )

        homonym_value = sheet.cell_value(
            row_index,
            columns["homonym_number"]
        )

        if homonym_value == "":
            homonym_number = None
        else:
            homonym_number = int(homonym_value)

        # We need a headword and at least some English lexical
        # information for this application's dictionary feature.
        if not headword or not (
            english_word or english_definition
        ):
            skipped += 1
            continue

        connection.execute(
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
            (
                headword,
                homonym_number,
                part_of_speech,
                korean_definition,
                english_word,
                english_definition,
            ),
        )

        imported += 1

    workbook.release_resources()

    return examined, imported, skipped


def import_dictionary():
    """Build the local SQLite dictionary from NIKL source files."""

    connection = create_database()

    total_examined = 0
    total_imported = 0
    total_skipped = 0

    try:
        for file_path in DICTIONARY_FILES:
            print(f"\nImporting {file_path.name}...")

            examined, imported, skipped = (
                import_dictionary_file(
                    connection,
                    file_path
                )
            )

            total_examined += examined
            total_imported += imported
            total_skipped += skipped

            print(f"  Examined: {examined:,}")
            print(f"  Imported: {imported:,}")
            print(f"  Skipped:  {skipped:,}")

        connection.commit()

    finally:
        connection.close()

    print("\n==============================")
    print("IMPORT COMPLETE")
    print("==============================")
    print(f"Rows examined: {total_examined:,}")
    print(f"Rows imported: {total_imported:,}")
    print(f"Rows skipped:  {total_skipped:,}")
    print(f"Database: {DATABASE_PATH}")


if __name__ == "__main__":
    import_dictionary()