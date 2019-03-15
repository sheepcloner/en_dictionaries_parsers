#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Parse RICHARD SOULE dictionary of synonyms located here: http://www.gutenberg.org/files/38390/38390-h/38390-h.htm
'''

import re
import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString

DEBUG = False

dict_file_name = '../resources/soule_dictionary.htm'
soule_dict_output_file = '../resources/soule_dict.json'

remove_parenth_content_regex = re.compile(r"(\(.*\)|\[.*\])") #match content in between parens or brackets
remove_parenth_regex = re.compile(r"[\(\)\xa0\xa0]") #remove left or right parens
remove_numbers_regex = re.compile(r"[0-9]")

def has_numbers(s):
    return bool(re.search(r'\d', s))

def get_word_tokens(raw_synonyms_string):
    raw_synonyms_string = remove_parenth_content_regex.sub('', raw_synonyms_string)
    raw_synonyms_string = remove_numbers_regex.sub('', raw_synonyms_string)
    raw_synonyms_string = remove_parenth_regex.sub('', raw_synonyms_string).strip()
    raw_synonyms_string = raw_synonyms_string.replace(".", "").lower()
    raw_synonyms = raw_synonyms_string.split(", ")

    synonyms = []
    for  s in raw_synonyms: #final cleanup of synonym tokens
        s = s.strip()
        if s:
            synonyms.append(s)
    synonyms = list(set(synonyms))
    
    return synonyms

soule_dict_file = open(dict_file_name, "r")
soule_dict_html = soule_dict_file.read() #read the html file as a big string
soule_dict_file.close()

soule_dict = dict()
soule_soup = BeautifulSoup(soule_dict_html, "html.parser")
dict_html_entries = soule_soup.select("dl")
i =-1
j=-1
for dict_entry in dict_html_entries: #provides the chapters in the dictionary (one chapter per letter)
    i = i+1
    j=-1
    previous_word = ''
    for entry_item in dict_entry.contents:
        j=j+1
        if DEBUG: print("Index %s,%s" %(i,j))
        #entry_item = dict_entry.contents[index] #this will either be a <dt> or <dd> element
        
        if type(entry_item) == NavigableString: #Not going to process string type children, move on to the next iteration
            continue
        
        synonyms = []
        antonyms = []
        
        if DEBUG: print("Processing: ", entry_item)
        
        if entry_item.name == 'dt': #this is a new word entry
            word = entry_item.b #the first bold entry in <dt> is the word itself
            word = word.extract().text.lower() #extract removes the item so all I am left with is text
            
            pos = entry_item.i
            if pos:
                pos = pos.extract().text #first italic tag is parts of speech
            
            raw_synonyms = entry_item.text
            
            #cleanup the synonyms string by removing parenthetical content and leftover parenthesis
            synonyms = get_word_tokens(raw_synonyms)
            
            if word in soule_dict: #word already exists
                soule_dict[word]["synonyms"].extend(synonyms)
                soule_dict[word]["synonyms"] = sorted(list(set(soule_dict[word]["synonyms"]))) #sorting is not always desired
            else:
                soule_dict[word] = dict()
                soule_dict[word]["synonyms"] = sorted(synonyms)
            
            previous_word = word
                
        elif entry_item.name == 'dd': #more synonyms for previous word
            if not previous_word:
                print("***********This is not supposed to happen: Previous word is blank and a <dd> was encountered")
                continue
            if previous_word in soule_dict: #word already exists
                raw_synonyms = entry_item.text
            
                #cleanup the synonyms string by removing parenthetical content and leftover parenthesis
                synonyms = get_word_tokens(raw_synonyms)
                soule_dict[previous_word]["synonyms"].extend(synonyms)
                soule_dict[previous_word]["synonyms"] = sorted(list(set(soule_dict[previous_word]["synonyms"])))
       
        if DEBUG: print(soule_dict[previous_word])


soule_dict_output_file = '../resources/soule_dict.json'
with open(soule_dict_output_file, 'w') as outfile:
    json.dump(soule_dict, outfile)
