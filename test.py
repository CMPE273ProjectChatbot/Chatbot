import os
import time
from slackclient import SlackClient
import sqlite3
from textblob import TextBlob

request = "Where is class CMPE 220 taken?"
text = TextBlob(request)
list_tags = text.tags
list_pnoun = []
list_noun = []
for el in text.tags:
        if el[1] == "NNP" or el[1] == "NNPS":
            list_pnoun.append(el[0])
        elif el[1] == "CD":
             list_pnoun.append(el[0])
        else:
             list_noun.append(el[0])
noun = " ".join( list_noun)
proper_noun = " ".join(list_pnoun)
print proper_noun
noun = TextBlob(noun)
list_tags1 = noun.tags
print list_tags1