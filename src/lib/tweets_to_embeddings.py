import numpy as np
import os
import pandas as pd
import sys
import re
import emoji
import json
import gensim
from gensim.models import Word2Vec, KeyedVectors  
# module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
# if module_path not in sys.path:
#     sys.path.append(module_path)



def main():
    directory_to_convert = 'embeddings_run_apr18'
    files_in_directory = os.listdir(directory_to_convert)
    corpus_stats = {}
    for file in files_in_directory:
        state_county_id = _get_filename(file)
        read_json = read_json_corpus(os.path.join(directory_to_convert, file))
        if not os.path.getsize(os.path.join(directory_to_convert, file)) == 0:        
            cleaned_text = cleaning_tweet_text(read_json)
            model = create_model(cleaned_text)
            model.wv.save_word2vec_format('word_embeddings_twitter_1/' + state_county_id + '_model.bin', binary=True)
            print('Successfully exported model.')

            get_corpus_stats(state_county_id, read_json, cleaned_text, model)
        else: 
            print('File is empty.. going to next one.')



def cleaning_tweet_text(json_object):
    '''applies several cleaning functions to the a string object containing the twitter corpus'''
    text = _combined_full_text(json_object)
    text = _delete_links(text)
    text = _delete_emojies(text)
    text = _delete_hashtags(text)
    text = _delete_new_line_chars(text)
    text = _delete_multiple_spaces(text)
    text = _delete_mentions(text)
    text = _replace_amp(text)
    text = _split_string_to_list_sentences(text)
    return text



def read_json_corpus(corpus_path):
    'reads the given path as json object'
    print('Reading the following file: ', corpus_path)
    tweet_data = []
    with open(corpus_path, 'r') as data:
        for line in data: 
            tweet_data.append(json.loads(line))
    return tweet_data


def get_corpus_stats(id, json_tweets, filtered_text, model):
    corpus_stats = {}
    corpus_stats['id'] = id
    corpus_stats['n_tweets'] = len(json_tweets)
    corpus_stats['n_sentences'] = len(filtered_text)
    corpus_stats['n_words'] = len([word for sentence in filtered_text for word in sentence])
    corpus_stats['n_unique_words'] = len(model.wv)
    corpus_stats['tweet_id'] = _get_tweet_ids(json_tweets)
    corpus_stats['vocab'] = list(model.wv.key_to_index.keys())

    with open('word_embeddings_twitter_1/' + id + '_corpus_stats.json', 'w') as file:
        json.dump(corpus_stats, file)
    print('Successfully exported corpus stats.')


def create_model(filtered_sentences):
    return gensim.models.Word2Vec(filtered_sentences, vector_size=300)

def _get_tweet_ids(json_object):
    'get the tweet ids for twitter json object'
    return [tweet['id'] for tweet in json_object]

def _get_filename(file_path):
    return file_path

def _combined_full_text(json_object):
    'combines the text field of each tweet in the json object, lowercases it and returns it as a string'
    corpus = [tweet['text'] for tweet in json_object]
    corpus = ' '.join(corpus).lower()
    return corpus

def _delete_links(text): 
    return re.sub(r'http\S+', '', text)

def _delete_hashtags(text):
    return re.sub(r'#(\w+)', '', text)

def _delete_mentions(text):
    return re.sub(r'@(\w+)', '', text)

def _delete_emojies(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text

def _delete_new_line_chars(text):
    return " ".join(text.splitlines())

def _delete_multiple_spaces(text):
    return " ".join(text.split())

def _replace_amp(text):
    return text.replace('&amp', '&')

def _split_string_to_list_sentences(filtered):
    '''split strings to a list of sentences'''
    new_text = [text.split() for text in filtered.split('.')]
    # to delete any empty lists in nested list
    new_text = [text for text in new_text if text != []]
    return new_text


if __name__ == '__main__':
    main()