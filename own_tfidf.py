import math

class OwnTfidf():

    def __init__(self):
        self.Unique_Tokens = []
        self.idf_scores = {}

    def calcul_tf (self, tokens):
        tf_dict = {}
        words_nombers = len(tokens)

