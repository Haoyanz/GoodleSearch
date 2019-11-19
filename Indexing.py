import os
import json
import re
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
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


def get_tf_idf():
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    f = open("tf-dif.txt", "w")
    for i in range(len(weight)):
        f.write("-----------Document: " + str(i + 1) + " tf - idf" + '-----------\n')
        for j in range(len(word)):
            if weight[i][j] != 0:
                f.write(str(word[j]) + ' ' + str(weight[i][j]) + '\n')
    f.close()


id_url_map = {}
token_map = {}
# index = 1
corpus = []
for root, dirs, files in os.walk('./DEV'):
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(root, file), 'r') as json_file:
                # add url to dictionary
                json_obj = json.load(json_file)
                # id_url_map[index] = json_obj['url']
                # parse html for content as a whole string
                soup = BeautifulSoup(json_obj['content'], 'html.parser')
                texts = soup.findAll(text=True)
                visible_texts = filter(tag_visible, texts)
                content = " ".join(t.strip() for t in visible_texts)
                corpus.append(content)

                # porter stemming
                # token_list = porter_stem(content)
                # write_doc_size_to_file(index, len(token_list))
                # print(token_list)
                # add_token_to_map(token_list, index)
                # index += 1
# f = open("url_id.txt", "w")
# for key, value in id_url_map.items():
#     f.write(str(key) + " " + value + '\n')
get_tf_idf()
# beautiful_print_map(token_map)
# write_map_to_file()
