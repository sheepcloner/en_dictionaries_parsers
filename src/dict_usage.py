#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Sample usage for SOULE and FALLOWS dictionaries
Demonstrates using a merger of both dictionaries
'''

import json

#merge both dictionaries into one
def combine_dictionaries(soule_dict, fallows_dict):
    words = list(set(soule_dict.keys() + fallows_dict.keys())) #get unique list of vocabulary words
    combined_dict = dict()

    for word in words:
        entry_keys = dict()
        if word in soule_dict and word in fallows_dict:
            entry_keys = list(set(soule_dict[word].keys() + fallows_dict[word].keys())) #get unique list of each word's keys
            combined_dict[word] = dict()
            for key in entry_keys:
                if key in soule_dict[word] and key in fallows_dict[word]:
                    combined_dict[word][key] = list(set(soule_dict[word][key] + fallows_dict[word][key])) #concat and make unique list of values from both dicts
                elif key not in soule_dict[word]:
                    combined_dict[word][key] = fallows_dict[word][key]
                else:
                    combined_dict[word][key] = soule_dict[word][key]

        elif word not in soule_dict:
            combined_dict[word] = fallows_dict[word]
        else:
            combined_dict[word] = soule_dict[word]

    return combined_dict

def get_word_dict_entry(vocab_word, soule_dict, fallows_dict, combined_dicts):
    if vocab_word in soule_dict:
        print("From Soule dictionary:\n", soule_dict[vocab_word])

    if vocab_word in fallows_dict:
        print("From Fallows dictionary:\n", fallows_dict[vocab_word])

    if vocab_word in combined_dicts:
        print("From Fallows & Soule dictionaries:\n", combined_dicts[vocab_word])


soule_dict_file = '../resources/soule_dict.json'
soule_dict = json.load(open(soule_dict_file, "r"))

fallows_dict_file = '../resources/fallows_dict.json'
fallows_dict = json.load(open(fallows_dict_file, "r"))

combined_dicts = combine_dictionaries(soule_dict, fallows_dict)

vocab_word = "lively"
get_word_dict_entry(vocab_word, soule_dict, fallows_dict, combined_dicts)