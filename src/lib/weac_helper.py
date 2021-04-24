import numpy as np
import os
import pandas as pd
import sys

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from weat_wefat.src.lib import weat
from gensim.models import KeyedVectors
import json

def get_weac_scores(emb_model1, emb_model2, keywords, other_words):

    emb1_vectors = np.array([emb_model1[word] for word in other_words])
    emb2_vectors = np.array([emb_model2[word] for word in other_words])
    
    word_dict = {}
    weac_object_dict = {}

    # instantiate class objects
    for i in range(len(keywords)):
        word = keywords[i]
        key1_vector = emb_model1[word]
        key2_vector = emb_model2[word]
        weac_object_dict[word] = weat.Weac(key1_vector, key2_vector, emb1_vectors, emb2_vectors)

    for word in keywords:
        word_dict[word] = weac_object_dict[word].effect_size(), weac_object_dict[word].p_value()

    return word_dict


def load_model(model):
    ny_model_path = 'data/us_corpus/ny_model.bin'
    tx_model_path = 'data/us_corpus/tx_model.bin'

    if model == 'ny':
        return KeyedVectors.load_word2vec_format(ny_model_path)
    if model == 'tx':
        return KeyedVectors.load_word2vec_format(tx_model_path)
    else: 
        raise ValueError('Did not match any models that are currently available')


def get_common_words(model1, model2):
    '''returns the common vocab words between two Word2Vec embeddings'''
    return [word for word in model1.wv.vocab.keys() if word in model2.wv.vocab.keys()]


def main():
    export_dir = 'data/us_corpus'

    if not os.path.isdir(export_dir):
        raise FileNotFoundError('Export path does not exist')

    ny_model = load_model('ny')
    tx_model = load_model('tx')
    keywords = ['covid', 'stay', 'home', 'media', 'quarantine', 'pandemic', 'gatherings', 'mask', 'face', 'government', 'conspiracy', 'vaccine', 'fascist', 'china', 'asian', 'biden']
    common_words = get_common_words(tx_model, ny_model)
    filtered_common_words = [word for word in common_words if word not in keywords]
    weac_scores = get_weac_scores(tx_model, ny_model, keywords, filtered_common_words)

    export_path = os.path.join(export_dir, 'weac_ny_tx_covid_tweets.json')
    i = 0
    while os.path.exists(f"{export_path}_{i}.json"):
        i += 1
    with open(f"{export_path}_{i}.json", 'w') as f:
        json.dump(weac_scores, f)

if __name__ == '__main__':
    main()



