import math


class OwnTfidf:
    """Custom TF-IDF vectorizer."""

    def __init__(self):
        self.unique_tokens = []
        self.word_idf_scores = {}  # Stockage des scores IDF par mot.

    def calculate_tf(self, tokens):
        """Calculate term frequency scores for a list of tokens."""
        tf_scores = {}
        word_count = len(tokens)

        # Sécurité : éviter une division par zéro.
        if word_count == 0:
            return tf_scores

        for word in tokens:
            # si le mot n'est pas présent je met +1 donc tous est à +1 si juste 1 fois
            tf_scores[word] = tf_scores.get(word, 0) + 1

        # Normaliser par le nombre total de mots.
        for word in tf_scores:
            tf_scores[word] = tf_scores[word] / word_count

        return tf_scores

    def calculate_idf(self, corpus):
        """Calculate inverse document frequency scores for a corpus."""
        corpus_size = len(corpus)
        document_frequencies = {}

        for tokens in corpus:
            unique_tokens = set(tokens)
            for word in unique_tokens:
                document_frequencies[word] = document_frequencies.get(word, 0) + 1

        idf_scores = {}
        for word, document_frequency in document_frequencies.items():
            idf_scores[word] = (
                math.log((1 + corpus_size) / (1 + document_frequency)) + 1
            )

        return idf_scores

    def fit(self, corpus):
        """Fit the vectorizer and return the TF-IDF matrix."""
        self.word_idf_scores = self.calculate_idf(corpus=corpus)
        self.unique_tokens = sorted(self.word_idf_scores.keys())

        tfidf_matrix = []

        for tokens in corpus:
            tf_scores = self.calculate_tf(tokens=tokens)
            row = []

            for token in self.unique_tokens:
                tf = tf_scores.get(token, 0)
                idf = self.word_idf_scores.get(token, 0)
                row.append(tf * idf)

            tfidf_matrix.append(row)

        return tfidf_matrix

    def get_feature_name_out(self):
        """Return the vocabulary learned during fitting."""
        return self.unique_tokens
