import pickle
import sys
import os

import gensim.downloader as api
import numpy as np

from fasttext import FastText
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator, TransformerMixin

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from config import path_to_fast_text_model

# Loads pre-trained word embedings model:
word2vec_model = api.load("word2vec-google-news-300") # model trained on lower case words, use lower case tokens

# Load the pre-trained FastText model
fast_model = FastText.load_model(path_to_fast_text_model)

# Count based and frequency methods
tfidf_vect = TfidfVectorizer()
count_vect = CountVectorizer()

# Extra parameters to fine tune for vectorization methods, used with pipeline

# TfidfVectorizer
parameters_tfidf = {
'tfidf__max_df': (0.5, 0.75, 1.0),   
'tfidf__max_features': (None, 5000, 10000, 50000),
'tfidf__ngram_range': ((1, 1), (1, 2), (1,3),),  
'tfidf__use_idf': (True, False),
'tfidf__norm': ('l1', 'l2', None),
'tfidf__sublinear_tf' : (True, False),
}

# CountVectorizer
parameters_count = {
'count_vect__max_df': (0.5, 0.75, 1.0),   
'count_vect__max_features': (None, 5000, 10000, 50000),
'count_vect__ngram_range': ((1, 1), (1, 2), (1,3),),  
}

# one hot encoding won't be used as it uses to much memoery, making it suboptimal

# Pretrained word embedings

# word2vec
# downloading pretrained word2vec model
word2vec_model_download = word2vec_model

class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, word2vec):
        self.word2vec = word2vec

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # gets the token that are in the model
        document_embeddings = [np.mean([self.word2vec[token] for token in document if token in self.word2vec], axis=0) 
                               for document in X]

        return np.array(document_embeddings)
    
    def __name__(self):
        return "Word2VecVectorizer"  
    
class FastTextVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, fast_text):
        self.fast_text = fast_text

    def fit(self, X, y=None):
        # There is no reason for fittting as we are using a pretrained model, can be modified
        return self

    def transform(self, X):
        # gets the token that are in the model
        document_embeddings = [np.mean([self.fast_text[token] for token in document if token in self.fast_text], axis=0) 
                               for document in X]
        
        return np.array(document_embeddings)
    
    def __name__(self):
        return "FastTextVectorizer"
