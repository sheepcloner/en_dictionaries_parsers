#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Parse Samuel Fallows synonyms and antonyms dictionary located here: http://www.gutenberg.org/files/51155/51155-0.txt
For simplicity, I manually grabbed the dictionary section and placed it in the file referenced in the code
'''

import re
from pprint import pprint
import json

DEBUG = False

dict_file_name = '../resources/fallows_raw_dict.txt'
fallows_dict_output_file = '../resources/fallows_dict.json'

keyword_pattern = re.compile(r'^KEY: ([a-zA-Z]+)\s*')
alpha_pattern = re.compile(r'([a-zA-Z]+)')

#parse the given comma separated string and pull out only words that have alpha characters
def parse_words(words_string):
    parsed_words = []
    words = words_string.split(", ")
    for w in words:
        m = alpha_pattern.match(w)

        if m and m.group(1):
            parsed_words.append(m.group(1).lower())
        else:
            if DEBUG: print("skipping word: ", w)
    return parsed_words

#generates a dictionary based on parsing FALLOWS dictionary pattern. Returns dictionary where vocabulary word is the key
def generate_dictionary(dict_file_name):
    fallows_dict = dict()
    with open(dict_file_name, "r") as dict_file:
        dict_block = ""
        for line in dict_file:
            line = line.strip()
            if line.startswith("="): #reached the end of a definition block, need to back trace
                dict_block_list = dict_block.split(".\n")
                if len(dict_block_list) < 3:
                    if DEBUG: print("Skipping dictionary block because of incorrect number of lines, expected minimum 3, found %s: "%len(dict_block_list), dict_block_list)
                else:
                    #parse the dictionary block
                    keyword = ""
                    synonyms = []
                    antonyms = []
    
                    if DEBUG: print("*******", dict_block_list)
                    m = keyword_pattern.match(dict_block_list[0])
                    if m and m.group(1):
                        keyword = m.group(1)
                        keyword = keyword.lower()
                    else:
                        if DEBUG: print("Skipping dictionary block because of malformed KEY: ", dict_block_list)
                        dict_block = "" #prepare for next dictionary block
                        continue
                    
                    #synonyms and antonyms could swap places easily so need to check for them in remaining entries
                    if dict_block_list[1].startswith("SYN: "):
                        synonyms = parse_words(dict_block_list[1].replace("SYN: ", ""))
                    if dict_block_list[1].startswith("ANT: "):
                        antonyms = parse_words(dict_block_list[1].replace("ANT: ", ""))
                        
                    if len(dict_block_list) > 2 and dict_block_list[2].startswith("SYN: "):
                        synonyms = parse_words(dict_block_list[2].replace("SYN: ", ""))
                    if len(dict_block_list) > 2 and dict_block_list[2].startswith("ANT: "):
                        antonyms = parse_words(dict_block_list[2].replace("ANT: ", ""))
                     
                    fallows_dict[keyword] = {"synonyms": synonyms, "antonyms" : antonyms}
                    
                dict_block = "" #prepare for next dictionary block
            else:
                dict_block = dict_block + line #still in the same dictionary block
                if line.endswith("."):
                    dict_block = dict_block + "\n"

    return fallows_dict

#Store the dictionary to given file. Output will be json
def store_dictionary(fallows_dict, fallows_dict_output_file):
    with open(fallows_dict_output_file, 'w') as outfile:
        json.dump(fallows_dict, outfile)
    return

fallows_dict = generate_dictionary(dict_file_name)
if DEBUG: pprint(fallows_dict)
store_dictionary(fallows_dict, fallows_dict_output_file)