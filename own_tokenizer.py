import re
import string

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer


class OwnTokenizer:
    """Custom tokenizer with options for stopwords, punctuation, and normalization."""

    def __init__(self, data, lang="english"):
        self.data = data
        self.lang = lang.lower()
        self.stop_words = set(stopwords.words(self.lang))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def tokenize_words(self, lower=False):
        """Split text into word tokens."""
        if not self.data:
            return []

        data = self.data.lower() if lower else self.data
        # return re.findall(r'\w+', data)  # problem avec les _
        return re.findall(r"[a-zA-Z0-9]+", data)  # voir pour mettre les accents fr

    def tokenize_sentences(self, lower=False):
        """Split text into sentence tokens."""
        if not self.data:
            return []

        data = self.data.lower() if lower else self.data
        return re.split(r"(?<=[.!?])\s+", data)

    def remove_stopwords(self, tokens):
        """Remove stopwords from tokens."""
        return [token for token in tokens if token not in self.stop_words]

    def remove_punctuation(self, tokens):
        """Remove punctuation tokens."""
        return [token for token in tokens if token not in string.punctuation]

    def normalize(self, tokens, method=None):
        """Normalize tokens using stemming or lemmatization."""
        if method == "stem":
            return [self.stemmer.stem(token) for token in tokens]

        if method == "lemma":
            return [self.lemmatizer.lemmatize(token) for token in tokens]

        return tokens

    def tokenize(
        self, sentence=False, punct=True, lower=False, stopword=True, normalization=None
    ):
        """Return tokens according to the selected options."""
        if sentence:
            return self.tokenize_sentences(lower)

        tokens = self.tokenize_words(lower)

        if stopword:
            tokens = self.remove_stopwords(tokens)

        if punct:
            tokens = self.remove_punctuation(tokens)

        if normalization:
            tokens = self.normalize(tokens, method=normalization)

        return tokens
