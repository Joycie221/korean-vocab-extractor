# Korean Vocabulary Extractor

A Korean text analysis and vocabulary extraction web application designed to transform authentic Korean text into contextualized vocabulary study material for language learners.

Rather than treating Korean words as simple whitespace-separated tokens, the application uses morphological analysis to identify vocabulary-bearing morphemes, normalize inflected forms, reconstruct derived words, and connect extracted vocabulary to the forms and sentences in which it originally appeared.

Extracted vocabulary includes part-of-speech information, frequency counts, encountered surface forms, sentence context, and English definitions retrieved from a local Korean lexical database.

## Features

- Korean morphological analysis using Kiwi
- Vocabulary extraction from Korean text
- Removal of grammatical particles, endings, and punctuation from vocabulary results
- Dictionary-form normalization for verbs and adjectives
- Reconstruction of derived verbs and adjectives such as:
  - `공부해요` → `공부하다`
  - `상속될` → `상속되다`
  - `우람했다` → `우람하다`
- Part-of-speech classification
- Vocabulary frequency counting
- Tracking of original surface forms
- Sentence-level context for every occurrence
- English dictionary glosses and definitions
- Support for multiple dictionary senses and homonyms
- Learner-oriented primary-definition selection
- Vocabulary search
- Part-of-speech filtering
- Filter-aware CSV export
- Automated regression testing

## How It Works

The application processes Korean text through several stages:

```text
Korean Text
    ↓
Kiwi Morphological Analysis
    ↓
Vocabulary Filtering
    ↓
Dictionary-Form Normalization
    ↓
Derived-Word Reconstruction
    ↓
Frequency and Context Tracking
    ↓
Local NIKL / SQLite Lookup
    ↓
Contextualized Vocabulary Study List
```

For example, a learner may encounter:

```text
어깨가 우람했다.
```

Kiwi separates the inflected form into morphological components. The application then reconstructs the learner-facing dictionary form:

```text
우람했다
    ↓
우람 + 하
    ↓
우람하다
```

The normalized form is used to retrieve English lexical information from the local dictionary database:

```text
우람하다
Adjective

bulky; brawny
Having a large build or size and strength.
```

The original encountered form (`우람했다`) and its source sentence remain attached to the vocabulary entry so that the learner can study both the dictionary form and its use in context.

## Dictionary Data

English definitions are retrieved locally rather than through a live web API.

The project uses textual lexical data from the National Institute of Korean Language's Korean Basic Dictionary and Korean-English learning dictionary resources.

The downloaded source data is transformed into a smaller application-specific SQLite database containing:

- Korean headword
- Homonym number
- Part of speech
- Korean definition
- English equivalent
- English definition

The source dictionary files contain many additional fields that are not required by this application. The import pipeline extracts and cleans only the information needed for vocabulary lookup.

The dataset used during development contains 76,833 source rows. The import process produces 71,948 usable English lexical records after entries without usable English lexical information are excluded.

An index on the Korean headword field provides efficient local lookup.

### Why the dictionary database is not included in Git

The raw dictionary downloads and generated SQLite database are intentionally excluded from version control:

```text
data/raw/
data/*.db
```

This keeps large generated and source-data files out of the repository and separates application code from external lexical data.

The database can be rebuilt locally using the import pipeline described below.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Joycie221/korean-vocab-extractor.git
cd korean-vocab-extractor
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The project uses packages including:

- Flask
- kiwipiepy
- pytest
- xlrd

## Dictionary Setup

The English-definition feature requires a locally generated dictionary database.

### 1. Obtain the dictionary data

Download the full Korean Basic Dictionary dataset from the
[National Institute of Korean Language's Full Dictionary Download page](https://krdict.korean.go.kr/download/downloadPopup).

Select **Excel Full Download (엑셀 전체 내려받기)**.

During development, this project used the September 2026 release of the dataset. After downloading and extracting the files, place the `.xls` files inside:

```text
data/raw/
```

The version used during development contained:

```text
data/raw/1_30000_20260919.xls
data/raw/2_30000_20260919.xls
data/raw/3_16833_20260919.xls
```

> **Note:** These filenames correspond to the dataset version used during development. If a newer download uses different filenames, update `DICTIONARY_FILES` in `scripts/import_dictionary.py` to match the downloaded files.

### 2. Inspect the source data

An inspection utility is included for examining the downloaded dictionary schema and testing specific headwords:

```bash
python scripts/inspect_dictionary.py
```

### 3. Build the SQLite database

Run:

```bash
python scripts/import_dictionary.py
```

This creates:

```text
data/dictionary.db
```

The generated database is ignored by Git and can be rebuilt from the source files when necessary.

### 4. Validate dictionary lookup

Run:

```bash
python scripts/check_dictionary_lookup.py
```

This performs diagnostic lookups against several Korean headwords used during development.

## Running the Application

Start the Flask development server:

```bash
python app.py
```

Then open the local address displayed by Flask in your browser.

Paste Korean text into the input field and select **Extract Vocabulary**.

The resulting vocabulary cards display:

- normalized dictionary form
- part of speech
- frequency
- primary English gloss
- English definition
- additional dictionary senses when available
- encountered surface forms
- original sentence context

Results can be searched, filtered by part of speech, and exported as CSV.

## Testing

The project uses `pytest` for automated regression testing.

Run the complete test suite with:

```bash
python -m pytest -v
```

The current test suite contains 21 automated tests covering behavior including:

- particle removal
- punctuation exclusion
- dictionary-form normalization
- adverb extraction
- `하다` verb reconstruction
- derived `되다` verb reconstruction
- derived `하다` adjective reconstruction
- frequency counting
- part-of-speech assignment
- sentence-context tracking
- original surface-form tracking
- vocabulary statistics
- dictionary retrieval
- multiple dictionary senses
- missing dictionary entries
- POS-aware dictionary lookup
- primary-definition selection
- integration of dictionary definitions with extracted vocabulary

## Design and Evaluation

Development followed an iterative test-and-evaluate process.

### From Tokenization to Morphological Analysis

Early versions of the extractor used simpler token-based processing. Korean's agglutinative morphology made whitespace tokenization insufficient for reliable learner-facing vocabulary extraction.

Kiwi was introduced to analyze Korean text morphologically, allowing grammatical particles and endings to be separated from vocabulary-bearing morphemes.

Custom normalization was then added to convert inflected verbs and adjectives into dictionary-style forms.

### Reconstructing Derived Vocabulary

Real-world Korean prose exposed cases that simple normalization did not handle correctly.

For example, forms such as:

```text
상속될
우람했다
```

revealed that derivational suffixes could cause meaningful vocabulary items to be split into components.

The extraction pipeline was generalized to reconstruct derived vocabulary:

```text
상속 + 되 → 상속되다
우람 + 하 → 우람하다
```

Regression tests were added for these cases to ensure that later changes would preserve the corrected behavior.

### Evaluating Authentic Korean Prose

The application was tested using Korean prose rather than only short artificial test sentences.

This evaluation exposed differences between grammatically analyzed forms, learner-facing vocabulary forms, and lexical dictionary entries. These cases guided improvements to normalization, derivational reconstruction, and dictionary integration.

### Handling Dictionary Homonyms and Multiple Senses

Dictionary integration introduced a separate information-quality problem: one Korean headword can correspond to multiple homonyms and many lexical senses.

For example, an initial lookup for:

```text
먹다
```

displayed the English meaning **"be deaf"** as the primary definition because it occurred first according to the dictionary's homonym ordering.

However, `먹다` also contains the common lexical sense:

```text
eat; have; consume; take
```

Rather than claiming to perform automatic contextual word-sense disambiguation, the application uses a learner-oriented heuristic for selecting a useful default lexical entry while preserving the remaining definitions for inspection.

This distinction is intentional: the application organizes lexical information for learners without claiming that it can always determine the exact intended sense from context.

## Known Limitations

### Word-Sense Disambiguation

The application does not currently perform contextual word-sense disambiguation.

When a word has multiple meanings, the system selects a learner-oriented primary dictionary entry using a heuristic. Additional definitions remain available in the interface.

The selected primary definition therefore should not be interpreted as a guarantee that the system has identified the exact contextual meaning.

### Morphological Analysis

Vocabulary extraction depends partly on Kiwi's morphological analysis.

Some words may receive a part-of-speech classification that differs from the most appropriate interpretation in a particular context.

For example, lexical resources and the morphological analyzer may occasionally disagree about whether a form should be treated as a common noun, proper noun, or another category.

### Derived and Compound Forms

The application currently reconstructs several important derivational patterns, but Korean morphology contains additional productive derivational, prefix, compound, and auxiliary constructions that may require further handling.

### Dictionary Coverage

Not every extracted vocabulary item is guaranteed to have a matching English dictionary entry.

Vocabulary without a matching entry remains usable in the application with its part of speech, frequency, encountered forms, and sentence context.

## Technologies

- Python
- Flask
- Kiwi / kiwipiepy
- SQLite
- xlrd
- pytest
- HTML
- CSS
- JavaScript
- Jinja

## Project Structure

```text
korean-vocab-extractor/
├── app.py
├── dictionary.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   └── dictionary.db
├── scripts/
│   ├── inspect_dictionary.py
│   ├── import_dictionary.py
│   └── check_dictionary_lookup.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── tests/
    ├── test_dictionary.py
    └── test_parser.py
```

The contents of `data/raw/` and the generated `data/dictionary.db` are intentionally excluded from version control.

## Data Attribution and Licensing

Dictionary text used by this project is derived from the **Korean Basic Dictionary (한국어기초사전)** and Korean-English learning dictionary resources provided by the **National Institute of Korean Language (국립국어원)**.

According to the Korean Basic Dictionary's copyright policy, materials on the site that are not separately marked otherwise are distributed under the **Creative Commons Attribution-ShareAlike 2.0 Korea (CC BY-SA 2.0 KR)** license.

Use of those materials requires attribution. Adapted materials must be distributed under the same license terms.

This project uses textual lexical data only. Multimedia materials such as images, video, audio, music, and pronunciation recordings may have separate licensing conditions and are not part of the local lexical database used by this application.

For the current terms and source dictionary, see the
[Korean Basic Dictionary](https://krdict.korean.go.kr/eng/mainAction?nation=eng)
and its
[copyright policy](https://krdict.korean.go.kr/eng/kboardPolicy/copyRightTermsInfo).

The full dictionary dataset used by the local import pipeline can be obtained from the
[National Institute of Korean Language's Full Dictionary Download page](https://krdict.korean.go.kr/download/downloadPopup).

## Future Work

Possible future extensions include:

- improved ranking of dictionary senses
- optional contextual word-sense disambiguation
- additional Korean derivational and compound-word reconstruction
- learner proficiency or vocabulary-level information
- flashcard or spaced-repetition export
- expanded lexical metadata
- additional evaluation using varied genres of authentic Korean text

These features are considered potential extensions rather than requirements for the current version.

## Purpose

Korean Vocabulary Extractor was created as an independent language-learning and information-processing project exploring how Korean morphological analysis, lexical data, contextual information, and interface design can be combined to transform authentic Korean text into structured study material.

The project emphasizes not only extracting words, but preserving the relationship between a learner-facing dictionary form and the language as it actually appeared in context.
