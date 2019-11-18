import os
import json
import re
from nltk.stem import PorterStemmer
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


def beautiful_print_map(url_map):
    for key, value in url_map.items():
        print(key, value)


def write_doc_size_to_file(document_id, size):
    f = open("document_size.txt", "a+")
    f.write(str(document_id) + ' ' + str(size) + '\n')
    f.close()


def write_map_to_file():
    f = open("token_map.txt", "w")
    for key, value in token_map.items():
        f.write(key + '\t')
        f.write(json.dumps(value) + '\n')
    f.close()


def add_token_to_map(token_list: [], document_id: int):
    '''
    Here I treat token_map as a dict where key is token, and value is another dict (key is document id, and value is the
    frequencies correspond)
    :param token_list: list of tokens [str]
    :param document_id: int, document id from index in url map
    :return: None
    '''
    for token in token_list:
        if token not in token_map.keys():
            token_map[token] = {document_id: 1}
        elif document_id in token_map[token]:
            token_map[token][document_id] += 1
        else:
            token_map[token][document_id] = 1


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
                texts = soup.findAll(text=True)
                visible_texts = filter(tag_visible, texts)
                content = " ".join(t.strip() for t in visible_texts)
                print(content)

                # porter stemming
                token_list = porter_stem(content)
                # write_doc_size_to_file(index, len(token_list))
                # print(token_list)
                # add_token_to_map(token_list, index)
                index += 1



# beautiful_print_map(token_map)
# write_map_to_file()
