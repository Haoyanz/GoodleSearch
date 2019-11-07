import os
import json
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def porter_stem(content):
    ps = PorterStemmer()
    content = (str(content)).lower()
    words = []
    words.extend(re.findall("[a-z0-9]+", content))
    for word in words:
        ps.stem(word)
    return words


id_url_map = {}
token_map = {}
index = 1
for root, dirs, files in os.walk('./DEV'):
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(root, file), 'r') as json_file:
                # add url to dictionary
                json_obj = json.load(json_file)
                id_url_map[index] = json_obj['url']
                # parse html for content as a whole string
                soup = BeautifulSoup(json_obj['content'], 'html.parser')
                texts = soup.findAll(text = True)
                visible_texts = filter(tag_visible, texts)
                content = " ".join(t.strip() for t in visible_texts)
                # porter stemming
                token_list = porter_stem(content)
                print (token_list)
                index += 1

print(id_url_map)