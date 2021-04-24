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
CONCAT_JSON_PATH = 'joined_tweets_run_apr18'
NO_CONCAT_JSON_PATH = 'tweets_run_apr18'
SAVE_MODEL_PATH = 'word_embeddings_run_apr18/models/'
CORPUS_STATS_PATH = 'word_embeddings_run_apr18/corpus_stats/'


def main():
    # decide whether to join json objects or not
    concatenate_json_objects = None
    dir_to_convert = get_directory_to_convert(concatenate_json_objects)

    process_raw_twitter_data(dir_to_convert)



def get_directory_to_convert(concat_files=None):
    '''
    Parameters:
    ------------
    concat_files : list, optional
        a list of lists of file_names of twitter raw json objects that need to be concatenated together. 
        Twitter raw pulls are regional and bounded by 25 mile radius, therefore its important to concatenate
        the tweets together to create one word embedding from a sub-population.
    '''
    if concat_files is not None: 
        for file_list in concat_files: 
            concatenate_twitter_json_objects(file_list, CONCAT_JSON_PATH)
        return CONCAT_JSON_PATH
    else: 
        return NO_CONCAT_JSON_PATH



def process_raw_twitter_data(dir_to_convert):
    '''
    main function to process the twarc2 raw tweet pulls, join them if necessary, process (clean) them, 
    and create word embeddings for them. 
    Parameters:
    ------------
    dir_to_convert : str
        the directory to run through and convert each JSON object of twitter pulls to word embeddings

    Returns 
    ------------
    Concatenated JSON objects (optional), .bin word embedding model, JSON object containing corpus stats
    '''
    files_in_directory = os.listdir(dir_to_convert)
    corpus_stats = {}
    for file in files_in_directory:
        state_county_id = _get_filename(file)
        read_json = read_json_corpus(os.path.join(dir_to_convert, file))

        if not os.path.getsize(os.path.join(dir_to_convert, file)) == 0:        
            cleaned_text = cleaning_tweet_text(read_json)
            model = create_model(cleaned_text)
            model.wv.save_word2vec_format(SAVE_MODEL_PATH + state_county_id + '_model.bin', binary=True)
            print('Successfully exported model.')
            get_corpus_stats(state_county_id, read_json, cleaned_text, model)
        else: 
            print('File is empty.. going to next one.')



def concatenate_twitter_json_objects(filenames, output_file_path):
    'concatenate twitter json objects since we have to combine several tweet raw pulls together'
    result = list()
    for f1 in filenames:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open(output_file_path, 'w') as output_file:
        json.dump(result, output_file)
    print('Successfully concatenated json objects as', output_file_path)



def cleaning_tweet_text(json_object):
    '''applies several cleaning functions to the a string object containing the twitter corpus'''
    unique_id_json_object = get_unique_tweets_only(json_object)
    text = _combined_full_text(unique_id_json_object)
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

    with open(SAVE_MODEL_PATH + id + '_corpus_stats.json', 'w') as file:
        json.dump(corpus_stats, file)
    print('Successfully exported corpus stats.')


def create_model(filtered_sentences):
    return gensim.models.Word2Vec(filtered_sentences, vector_size=300)

def get_unique_tweets_only(json_object):
    cleaned_object = {tweet['id']:tweet for tweet in json_object}.values()
    print('There were ', len(json_object), 'original tweets. After cleaning, there are ', len(cleaned_object), 'unique tweets left.')
    return cleaned_object

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