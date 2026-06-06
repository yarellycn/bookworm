import math

class OwnTfidf():

    def __init__(self):
        self.Unique_Tokens = []
        self.word_idf_scores = {} #stokage score idf par mot

    def calcul_tf (self, tokens):
        tf_dict = {}
        words_nombers = len(tokens)
        
        #secu
        if words_nombers== 0:
            return tf_dict
        
        for word in tokens :
            #si le mot n'est pas présent je met +1 donc tous est à +1 si juste 1 fois 
            tf_dict[word]= tf_dict.get(word, 0) +1
        
        #normalisation 
        for word in tf_dict:
            tf_dict[word]= tf_dict[word]/words_nombers

        return tf_dict
    
    def calcul_idf(self, corpus):
        #calcul de l idf des mots sur l'esemble choisi
        size_corpus= len(corpus)
        df_dict= {}

        for tokens in corpus:
            unique = set(tokens)
            for word in unique :
                df_dict[word]= df_dict.get(word, 0)+1
            
        idf_dict = {}
        for word, df in df_dict.items():
            idf_dict[word]= math.log((1+size_corpus)/(1+df))+1

        return idf_dict
    
    def fit(self, corpus):
        self.word_idf_scores= self.calcul_idf(corpus=corpus)
        self.Unique_Tokens= sorted(list(self.word_idf_scores.keys()))

        matrice_tfidf = []

        for tokens in corpus:
            tf_corpus = self.calcul_tf(tokens=tokens) 

            matrice = []
            for token in self.Unique_Tokens:
                tf = tf_corpus.get(token,0)
                idf= self.word_idf_scores.get(token, 0)
                matrice.append(tf*idf)

            matrice_tfidf.append(matrice)
        return matrice_tfidf
    
 



