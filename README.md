# Bookworm

Bookworm is a lightweight command-line NLP application. It analyzes books from Project Gutenberg and provides lexical statistics, topic modeling, named entity recognition, summarization, similarity recommendations, and complete book cards.

The project follows a clean architecture and caches results to avoid unnecessary recomputation.


## Features

### Lexical Diversity Analysis

Computes lexical statistics for a book.

```bash
python bookworm.py --lexdiv <ID>
```

Returns:

```json
{
  "tok": 12345,
  "typ": 4567,
  "hap": 2345,
  "ttr": 0.37,
  "mwl": 4.82,
  "mwf": 2.70
}
```

### Topic Modeling

Extracts the top 10 topic words for each section of a book.

```bash
python bookworm.py --topics <ID>
```

Returns:

```json
{
  "1": ["word1", "word2", "word3"],
  "2": ["word1", "word2", "word3"]
}
```

### Named Entity Recognition

Extracts characters and locations from the book.

```bash
python bookworm.py --entities <ID>
```

Returns:

```json
{
  "characters": ["Alice", "Queen"],
  "locations": ["London", "England"]
}
```

### Book Summarization

Generates a short summary of the book.

```bash
python bookworm.py --summarize <ID>
```

Returns:

```text
A short summary of the book.
```

### Book Similarity

Recommends similar books from a predefined collection.

```bash
python bookworm.py --similar <ID>
```

Returns:

```json
[
  "title1",
  "title2",
  "title3",
  "title4",
  "title5"
]
```

### Book Card Generation

Generates a complete overview of a book.

```bash
python bookworm.py --card <ID>
```

Returns:

```json
{
  "info": {
    "id": "11",
    "title": "Alice's Adventures in Wonderland",
    "authors": "Lewis Carroll",
    "bookshelves": "Children's Literature"
  },
  "lexdiv": {},
  "topics": {},
  "entities": {},
  "summary": "...",
  "similar": []
}
```

## Architecture

The project is organized around independent modules.

* `bookworm.py`: CLI entry point and action dispatcher
* `tools.py`: book download, reading, cleaning, tokenization helpers
* `cache.py`: cache management
* `lexical_diversity.py`: lexical statistics
* `topic_modeling.py`: topic extraction
* `entities.py`: named entity recognition
* `summarize.py`: book summarization
* `similar.py`: book similarity search
* `card.py`: complete book card generation
* `own_tokenizer.py`: custom tokenizer
* `own_tfidf.py`: custom TF-IDF implementation
* `evaluate.py`: result comparison utilities

## NLP Pipeline

The general processing pipeline is:

```text
Book ID
  -> Download from Project Gutenberg
  -> Store locally
  -> Remove Gutenberg header/footer
  -> Tokenize text
  -> Apply selected NLP task
  -> Cache result
  -> Return CLI output
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Bookworm
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download required NLTK resources:

```python
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")
nltk.download("stopwords")
nltk.download("wordnet")
```

## Dependencies

Main dependencies include:

* `nltk`
* `scikit-learn`
* `numpy`
* `sumy`
* `spacy`
* `requests`
* `networkx`
* `matplotlib`


## Usage

### Lexical Diversity

```bash
python bookworm.py --lexdiv 11
```

### Topic Modeling

```bash
python bookworm.py --topics 11
```

Using the custom TF-IDF implementation:

```bash
python bookworm.py --topics 11 --own
```

### Named Entity Recognition

```bash
python bookworm.py --entities 11
```

### Summarization

```bash
python bookworm.py --summarize 11
```

### Similarity Search

```bash
python bookworm.py --similar 11
```

Using the custom TF-IDF implementation:

```bash
python bookworm.py --similar 11 --own
```

### Book Card

```bash
python bookworm.py --card 11
```


## Project Structure

```text
Bookworm/
├── bookworm.py
├── cache.py
├── card.py
├── entities.py
├── evaluate.py
├── lexical_diversity.py
├── own_tfidf.py
├── own_tokenizer.py
├── requirements.txt
├── similar.py
├── summarize.py
├── tools.py
├── topic_modeling.py
├── notebook.ipynb
└── data/
    ├── books/
    ├── cache/
    └── rdf/
```


## Limitations

* The application depends on Project Gutenberg text formatting.
* Chapter detection may vary depending on the structure of each book.
* NLTK named entity recognition may produce false positives.
* Summaries are extractive, meaning they reuse existing sentences from the text.
* Similarity search is limited to the predefined book collection.
* The custom tokenizer currently focuses mainly on English text.

## Future Improvements

Potential improvements include:

* Better multilingual support
* More robust chapter and section detection
* Improved named entity filtering
* Larger recommendation corpus
* Unit tests for each module

## Authors

- BERGER, Yarelly
- GARDEY, Cyrille