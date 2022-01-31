# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import re
import nltk
#import multiprocessing
from gensim.models import Word2Vec
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

import matplotlib.pyplot as plt

data = pd.read_csv("floop_data_15k.csv")

data.shape

#data.head()

#data.info()
#To remove special characters and punctuation from our dataset
from string import punctuation

punctuations = punctuation

def solution(sentence):
    for p in punctuations:
        sentence = sentence.replace(p, '')
    return sentence

x = data["Field1"].apply(solution)
pattern = "[^a-zA-Z0-9]"
x_cleaned = [re.sub(pattern," ",text) for text in x]

x_lowered = [text.lower() for text in x_cleaned]
x_lowered

x_lowered[0]

nltk.download('punkt')

x_tokenized = [nltk.word_tokenize(text) for text in x_lowered]

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemma = WordNetLemmatizer()

x_lemmatized = [[lemma.lemmatize(word) for word in text] for text in x_tokenized]

print(x_lemmatized[0])

#cores = multiprocessing.cpu_count()

#cores

# For classification data whether good or bad.

w2v_model = Word2Vec(min_count=20,
                     window=2,
                     size=300,
                     sample=6e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20,
                     workers= 1 )

t = time()

w2v_model.build_vocab(x_lemmatized, progress_per=10000)

print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

t = time()

w2v_model.train(x_lemmatized, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

w2v_model.init_sims(replace=True)

w2v_model.save("word2vec11.model")

word_vectors = Word2Vec.load("/content/word2vec11.model").wv
model = KMeans(n_clusters=2, max_iter=1000, random_state=True, n_init=50).fit(X=word_vectors.vectors.astype('double'))
positive_cluster_center = model.cluster_centers_[0]
negative_cluster_center = model.cluster_centers_[1]

model.cluster_centers_

def cast_vector(row):
    return np.array(list(map(lambda x: x.astype('double'), row)))

words = pd.DataFrame(word_vectors.vocab.keys())
words.columns = ['words']
words['vectors'] = words.words.apply(lambda x: word_vectors[f'{x}'])
words['vectorsmean'] = words.vectors.apply(lambda x: x.mean())
words['vectors_typed'] = words.vectors.apply(cast_vector)
words['cluster'] = words.vectors_typed.apply(lambda x: model.predict([np.array(x, dtype=np.double)]))
words.cluster = words.cluster.apply(lambda x: x[0])
words['cluster_value'] = [1 if i==0 else -1 for i in words.cluster]
words['closeness_score'] = words.apply(lambda x: 1/(model.transform([x.vectors]).min()), axis=1)
words['sentiment_coeff'] = words.closeness_score * words.cluster_value

words.head(10)

u_labels = np.unique(words['cluster'])

words['vectorsmean'] = words.vectors.apply(lambda x: x.mean())

words['vectorsmean'][0]

len(words["vectors"][1])

words.head(10)

# FOr plotting 

colors = {1: 'black', -1: 'Red'}
plt.scatter(words['sentiment_coeff'] , words['vectorsmean'] , c=words['cluster_value'].map(colors))

plt.show()