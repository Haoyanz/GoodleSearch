import os
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def porter_stem(content):
    stem_list = []
    ps = PorterStemmer()
    words = word_tokenize(content)
    for word in words:
        stem_list.append(ps.stem(word))
    return stem_list


id_url_map = {}
index = 1
for root, dirs, files in os.walk('./DEV'):
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(root, file), 'r') as json_file:
                json_obj = json.load(json_file)
                id_url_map[index] = json_obj['url']
                index += 1

print(id_url_map)