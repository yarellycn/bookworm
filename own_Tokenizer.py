import string, re
from nltk.stem import PorterStemmer, WordNetLemmatizer
# from nltk.tag import pos_tag
from nltk.corpus import stopwords

class OwnTokenizer():
    """ This class is for tokenize , you can fin many option for cut your text in words ou sentence and removed usless word or punctuation"""

    def __init__(self, data, lang= "english"):
        self.data= data
        self.lang= lang.lower()
        self.stop_words= set(stopwords.words(self.lang))


    def tok_word_brut(self, lower= False):
        if not self.data :
            return []
        if lower :
           data = self.data.lower(self)
           return re.findall(r'\w+', data) 
        return re.findall(r'\w+', data) 
    
    def tok_sentence_brut(self, lower= False):

        if not self.data :
            return []
        if lower:
            data = self.data.lower()
            return re.split(r'(?<=[.!?])\s+', data) 
        return re.split(r'(?<=[.!?])\s+', data) 

    def remover_stopword(self,tokens ):
        return [token for token in tokens if token not in self.stop_words]

    def remover_punctuation (self, tokens):
        return [token for token in tokens if token not in string.punctuation]
    
    def normalize(self , tokens, method=None):
        if method == "stem":
            return [self.stemmer.stem(tokens) for token in tokens]
        if method == "lemma":
            return [self.stemmer.lemmatize(token) for token in tokens]
        return tokens

    def tokenize(self, sentence= False, punct = True, lower=False ,stopword=True , normalization=None):
        """ Select your custome tokenize """
                
        if sentence :
            tokens = self.tok_sentence_brut(self.data, lower)
        else :
            tokens = self.tok_word_brut(self.data, lower)
        
        if stopword:
            tokens =self.remover_stopword(tokens= tokens)
        
        if punct:
            tokens= self.remover_punctuation(tokens=tokens)
        
        if normalization and not sentence:
            tokens = self.normalize(tokens=tokens, method=normalization)

        return tokens
