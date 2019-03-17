# en_dictionaries_parsers
Parsers for multiple english dictionaries to provider synonyms and antonyms per word

While working on Natural Language Processing (NLP) solutions, I ran into scarity of synonyms and antonyms resources out there.
I looked  around and found some in project [Gutenberg](https://www.gutenberg.org/), but no parsers for them.
I created a parser for two of them that I found most useful:
- Samuel Fallows of synonyms and antonyms dictionary located [here](http://www.gutenberg.org/files/51155/51155-0.txt)
- Richard Soule dictionary of synonyms located [here](http://www.gutenberg.org/files/38390/38390-h/38390-h.htm) 

In the `resources` foldr you will find the raw dictionary files as well as the output of my parser (my output is in _json_ format.)
In the `src` folder you will find both parsers along with sample usage.
In `src/dict_usage.py` I show how to combine both dictionaries and use them to lookup synonyms and antonyms.

The dictionary structure:
- Vocabulary words are the keys
- The value is a dictionary that has an entry for _synonyms_ and another fo _antonyms_

Below is a sample entry for the word `lively`:

```
{  
   'synonyms':[  
      'full of life',
      'joyous',
      'impassioned',
      'blithesome',
      'bright',
      'sprightly',
      'supple',
      'vivid',
      'spry',
      'agile',
      'buxom',
      'sparkling',
      'eager',
      'glowing',
      'airy',
      'smart',
      'vigorous',
      'forcible',
      'gay',
      'brisk',
      'debonair',
      'alert',
      'nimble',
      'active',
      'dapper',
      'strong',
      'frolicsome',
      'brilliant',
      'piquant',
      'vivacious',
      'racy',
      'spirited',
      'keen',
      'blithe',
      'nervous',
      'buoyant',
      'quick',
      'animated',
      'stirring'
   ],
   'antonyms':[  
      'lifeless',
      'torpid',
      'dull',
      'inanimate',
      'indifferent',
      'listless'
   ]
}
```

Refer to [dictionary usage code](src/dict_usage.py) for how to use these dictionaries.

*Future items*:
- Account for Part of speech (POS)
- Create a graph that connects all the words together with synonyms and antonyms relationship