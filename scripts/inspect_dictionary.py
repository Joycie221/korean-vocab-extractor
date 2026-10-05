import xlrd


DICTIONARY_FILES = [
    "data/raw/1_30000_20260919.xls",
    "data/raw/2_30000_20260919.xls",
    "data/raw/3_16833_20260919.xls",
]

TEST_WORDS = {
    "먹다",
    "공부하다",
    "우람하다",
    "상속되다",
    "어울리다",
    "다산",
}


def search_dictionary():
    found_words = set()

    for file_path in DICTIONARY_FILES:
        print(f"\nSearching {file_path}...")

        workbook = xlrd.open_workbook(
            file_path,
            on_demand=True
        )

        sheet = workbook.sheet_by_index(0)

        headers = sheet.row_values(0)

        headword_col = headers.index("표제어")
        homonym_col = headers.index("동형어 번호")
        pos_col = headers.index("품사")
        korean_definition_col = headers.index("뜻풀이")
        english_word_col = headers.index("영어 대역어")
        english_definition_col = headers.index(
            "영어 대역어 뜻풀이"
        )

        for row_index in range(1, sheet.nrows):
            headword = sheet.cell_value(
                row_index,
                headword_col
            )

            if headword in TEST_WORDS:
                found_words.add(headword)

                print("\n------------------------------")
                print(f"HEADWORD: {headword}")
                print(
                    "HOMONYM:",
                    sheet.cell_value(
                        row_index,
                        homonym_col
                    )
                )
                print(
                    "POS:",
                    sheet.cell_value(
                        row_index,
                        pos_col
                    )
                )
                print(
                    "KOREAN DEFINITION:",
                    sheet.cell_value(
                        row_index,
                        korean_definition_col
                    )
                )
                print(
                    "ENGLISH WORD:",
                    sheet.cell_value(
                        row_index,
                        english_word_col
                    )
                )
                print(
                    "ENGLISH DEFINITION:",
                    sheet.cell_value(
                        row_index,
                        english_definition_col
                    )
                )

        workbook.release_resources()

    print("\n==============================")
    print("COVERAGE RESULTS")
    print("==============================")

    for word in TEST_WORDS:
        if word in found_words:
            print(f"✓ {word}")
        else:
            print(f"✗ {word}")


if __name__ == "__main__":
    search_dictionary()